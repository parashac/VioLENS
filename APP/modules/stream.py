import cv2
import time
import threading
import collections
import numpy as np

from .state import streams
from .preprocessing import preprocess_clip
from .model import model
from .alert import send_alert

FRAMES = 30
CLASSES = ["Non-Violent", "Violent"]
CONFIDENCE_THRESHOLD = 0.65


def stream_worker(source_id: str, source):
    state = streams[source_id]
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        state["result"] = {"error": f"Cannot open source: {source}"}
        state["running"] = False
        return

    state["cap"] = cap

    frame_buffer = collections.deque(maxlen=FRAMES)
    state["frame_buffer"] = frame_buffer
    state["infer_event"] = threading.Event()

    t_reader = threading.Thread(target=frame_reader, args=(source_id, source), daemon=True)
    t_infer = threading.Thread(target=inference_worker, args=(source_id,), daemon=True)

    t_reader.start()
    t_infer.start()


def frame_reader(source_id: str, source):
    state = streams[source_id]
    cap = state["cap"]
    frame_buffer = state["frame_buffer"]
    infer_event = state["infer_event"]

    new_frames = 0

    while state["running"]:
        ret, frame = cap.read()

        if not ret:
            time.sleep(1)
            cap.release()
            cap = cv2.VideoCapture(source)
            state["cap"] = cap
            continue

        frame_buffer.append(frame.copy())
        new_frames += 1

        if new_frames >= FRAMES and not infer_event.is_set():
            infer_event.set()
            new_frames = 0

        result = state.get("result", {})
        display = frame.copy()

        if result and "label" in result:
            lbl = result["label"]
            conf = result["confidence"]
            color = (0,0,220) if lbl == "Violent" else (0,200,0)

            overlay = display.copy()
            cv2.rectangle(overlay, (0,0), (display.shape[1], 60), color, -1)
            cv2.addWeighted(overlay, 0.45, display, 0.55, 0, display)

            cv2.putText(display, f"{lbl} {conf}%", (12,42),
                        cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)

        _, jpeg = cv2.imencode(".jpg", display)

        with state["lock"]:
            state["latest_frame"] = jpeg.tobytes()

        time.sleep(0.001)

    cap.release()


def inference_worker(source_id: str):
    state = streams[source_id]
    frame_buffer = state["frame_buffer"]
    infer_event = state["infer_event"]

    while state["running"]:
        triggered = infer_event.wait(timeout=2)
        infer_event.clear()

        if not triggered:
            continue

        clip_frames = list(frame_buffer)

        if len(clip_frames) < FRAMES:
            continue

        clip = preprocess_clip(clip_frames)
        preds = model.predict(clip, verbose=0)[0]

        idx = int(np.argmax(preds))
        confidence = float(preds[idx])

        label = CLASSES[idx] if confidence >= CONFIDENCE_THRESHOLD else "Uncertain"

        with state["lock"]:
            state["result"] = {
                "label": label,
                "confidence": round(confidence * 100, 1),
                "violent_prob": round(float(preds[1]) * 100, 1),
                "nonviolent_prob": round(float(preds[0]) * 100, 1),
            }
        
        if label == "Violent":
            send_alert(source_id)

        