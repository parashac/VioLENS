import time

streams = {}

def stop_source(source_id: str):
    if source_id in streams:
        streams[source_id]["running"] = False
        time.sleep(0.3)
        del streams[source_id]