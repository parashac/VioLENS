from flask import Flask, render_template, Response, jsonify, request
import threading

from modules.state import streams, stop_source
from modules.stream import stream_worker
from modules.mjpeg import generate_mjpeg

app = Flask(__name__)

# ---------------------------
# Homepage
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------
# Start RTSP / CCTV Stream
# ---------------------------
@app.route("/start_rtsp", methods=["POST"])
def start_rtsp():
    rtsp_url = request.json.get("rtsp_url", "").strip()
    if not rtsp_url:
        return jsonify({"error": "No RTSP URL provided"}), 400

    source_id = "rtsp_0"
    stop_source(source_id)

    streams[source_id] = {
        "cap": None,
        "latest_frame": None,
        "result": {},
        "lock": threading.Lock(),
        "running": True,
        "source": rtsp_url,
    }

    threading.Thread(target=stream_worker, args=(source_id, rtsp_url), daemon=True).start()
    return jsonify({"status": "started", "source_id": source_id})


# ---------------------------
# Stop RTSP / CCTV Stream
# ---------------------------
@app.route("/stop_rtsp", methods=["POST"])
def stop_rtsp():
    stop_source("rtsp_0")
    return jsonify({"status": "stopped"})


# ---------------------------
# Start Webcam Stream
# ---------------------------
@app.route("/start_webcam", methods=["POST"])
def start_webcam():
    # request.json may be None if no body / wrong Content-Type is sent
    body = request.get_json(silent=True) or {}
    cam_index = body.get("cam_index", 0)
    try:
        cam_index = int(cam_index)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid camera index"}), 400

    # Must match the source_id the frontend uses: /video_feed/webcam & /result/webcam
    source_id = "webcam"
    stop_source(source_id)

    streams[source_id] = {
        "cap": None,
        "latest_frame": None,
        "result": {},
        "lock": threading.Lock(),
        "running": True,
        "source": cam_index,
    }

    threading.Thread(target=stream_worker, args=(source_id, cam_index), daemon=True).start()
    return jsonify({"status": "started", "source_id": source_id})


# ---------------------------
# Stop Webcam Stream
# ---------------------------
@app.route("/stop_webcam", methods=["POST"])
def stop_webcam():
    stop_source("webcam")          # must match source_id above
    return jsonify({"status": "stopped"})


# ---------------------------
# Video feed (MJPEG)
# ---------------------------
@app.route("/video_feed/<source_id>")
def video_feed(source_id):
    if source_id not in streams:
        return "Stream not found", 404
    return Response(generate_mjpeg(source_id),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# ---------------------------
# Get latest detection result
# ---------------------------
@app.route("/result/<source_id>")
def get_result(source_id):
    state = streams.get(source_id)
    if not state:
        return jsonify({"error": "No active stream"}), 404

    with state["lock"]:
        return jsonify(state.get("result", {}))


# ---------------------------
# Run Flask App
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)