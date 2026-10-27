"""Selected historical methods from Interface_Weighbridge_IP_v7_3_0_DB_Dev.py.
Imports, initialization and other application methods intentionally omitted.
Documentation excerpt only, not a complete runnable application.
"""

class WorkflowExcerpt:
    # Remaining application code omitted.

    def manual_detect(self):
        """One click starts a bounded detection-and-registration request."""
        if self.processing:
            self.status.configure(text="تشخیص یا ثبت قبلی هنوز در حال انجام است…")
            return
        if not self.capture_running or self.capture is None:
            self.status.configure(text="ابتدا دوربین شبکه را متصل کنید")
            return
        if any(item is not None for item in self.result_data) and self.result_save_buttons[0].winfo_manager():
            self.status.configure(text="پلاک قبلی ثبت نشد؛ ابتدا «تلاش مجدد ثبت» یا ثبت دستی را انجام دهید")
            return
        self.clear_manual_results(update_status=False)
        self.processing = True
        self.detection_cancel.clear()
        self.detection_attempt = 0
        self.detection_frame_serial = -1
        self.detect_button.configure(state="disabled")
        self.attempt_manual_detection()

    def retry_manual_detection(self, reason):
        if self.detection_attempt < MAX_DETECTION_ATTEMPTS and not self.detection_cancel.is_set():
            self.status.configure(text=f"{reason}؛ یک تلاش دیگر با تصویر تازه…")
            self.after(500, self.attempt_manual_detection)
        else:
            self.set_result_message(0, "خوانده نشد", "#ff7777")
            self.finish_manual_detection("پلاک خوانده نشد؛ ثبت دستی یا تشخیص دوباره")

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

