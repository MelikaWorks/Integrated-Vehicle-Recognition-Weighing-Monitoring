"""Selected historical excerpts from app.py; web pilot 1.0.3.
Imports, app initialization, model assets and other logic intentionally omitted.
Documentation only; not a runnable application.
"""

def video_feed():
    def generate():
        while True:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                   camera.jpeg() + b"\r\n")
            time.sleep(0.09)
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def api_save_result(index):
    if index < 0 or index >= FRAME_COUNT:
        return jsonify(ok=False, message="شماره نتیجه نامعتبر است."), 404
    data = request.get_json(silent=True) or {}
    expected_code = str(data.get("towzin_code", "")).strip()
    with state.lock:
        item = state.results[index]
    if item is None or item["parts"] is None:
        return jsonify(ok=False, message="این نتیجه برای ثبت معتبر نیست."), 400
    try:
        saved = commit_plate(
            expected_code, item["parts"], item["crop"], item["frame"], "web_camera")
        state.clear()
        with state.lock:
            state.status = f"ثبت شد | توزین {saved.towzin_code} | {saved.car_pelak}"
        return jsonify(ok=True, record=weighing_json(saved), status=state.status)
    except Exception as exc:
        logger.error("Saving detected plate failed", exc_info=True)
        message = str(exc) if isinstance(exc, DatabaseError) else "پلاک ذخیره نشد."
        return jsonify(ok=False, message=message), 400

