import time
from .state import streams

def generate_mjpeg(source_id: str):
    while True:
        state = streams.get(source_id)

        if state is None or not state["running"]:
            break

        with state["lock"]:
            frame = state.get("latest_frame")

        if frame:
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        time.sleep(0.03)