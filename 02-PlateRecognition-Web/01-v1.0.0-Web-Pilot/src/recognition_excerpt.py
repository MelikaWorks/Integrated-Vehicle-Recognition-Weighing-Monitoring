"""Selected historical excerpts from app.py; web pilot 1.0.0.
Imports, app initialization, model assets and other logic intentionally omitted.
Documentation only; not a runnable application.
"""

def api_detect():
    if not state.inference_lock.acquire(blocking=False):
        return jsonify(ok=False, message="تشخیص قبلی هنوز در حال انجام است."), 409
    try:
        with state.lock:
            state.processing = True
            state.results = [None] * FRAME_COUNT
            state.status = "چهار فریم ذخیره شد؛ در حال تشخیص…"
        frames = camera.recent_frames()
        results = []
        for index, frame in enumerate(frames):
            try:
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                result, crop = backend.predict_plate(pil_image)
                parts = split_plate(result)
                message = parts["display"] if parts else str(result or "پلاک نامعتبر")
                if parts is None:
                    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    cv2.imwrite(str(FAILED_DIR / f"failed_{stamp}_frame{index + 1}.jpg"), frame)
                results.append({
                    "parts": parts,
                    "crop": crop,
                    "frame": frame,
                    "message": message,
                })
            except Exception:
                logger.error("Inference failed for frame %s", index + 1, exc_info=True)
                results.append({
                    "parts": None, "crop": None, "frame": frame,
                    "message": "خطای تشخیص",
                })
        valid_count = sum(item["parts"] is not None for item in results)
        with state.lock:
            state.results = results
            state.status = (
                f"تعداد نتیجه‌های معتبر: {valid_count}؛ نتیجه درست را ثبت کنید"
                if valid_count else
                "پلاک معتبری پیدا نشد؛ تشخیص مجدد را بزنید"
            )
        return jsonify(ok=True, results=state.public_results(), status=state.status)
    except Exception as exc:
        logger.error("Detection request failed", exc_info=True)
        with state.lock:
            state.status = str(exc)
        return jsonify(ok=False, message=str(exc)), 400
    finally:
        with state.lock:
            state.processing = False
        state.inference_lock.release()

