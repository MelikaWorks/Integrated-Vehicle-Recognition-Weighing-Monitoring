"""Selected historical methods from Interface_Weighbridge_IP_v7_3_2_DB_Dev.py.
Imports, initialization and other application methods intentionally omitted.
Documentation excerpt only, not a complete runnable application.
"""

class WorkflowExcerpt:
    # Remaining application code omitted.

    def retry_manual_detection(self, reason):
        if self.detection_attempt < MAX_DETECTION_ATTEMPTS and not self.detection_cancel.is_set():
            self.status.configure(text=f"{reason}؛ یک تلاش دیگر با تصویر تازه…")
            self.after(500, self.attempt_manual_detection)
        else:
            self.set_result_message(0, "خوانده نشد", "#ff7777")
            self.finish_manual_detection("پلاک خوانده نشد؛ شماره را دستی وارد کنید")
            if not self.closing and not self.detection_cancel.is_set() and self.capture_running:
                self.open_manual_entry()

    def consume_manual_detection(self):
        if self.closing:
            return
        try:
            result, crop, frame, error = self.detection_queue.get_nowait()
        except queue.Empty:
            self.after(100, self.consume_manual_detection)
            return
        if self.detection_cancel.is_set() or not self.capture_running:
            self.finish_manual_detection("تشخیص متوقف شد؛ چیزی ثبت نشد")
            return
        self.show_manual_result(0, result, crop, frame, error)
        if error or not result or self.split_plate(result) is None:
            self.retry_manual_detection(error or "این تصویر خوانده نشد")
            return
        # Exactly one save for the first valid result; OCR never retries a save.
        self.save_manual_result(0)

