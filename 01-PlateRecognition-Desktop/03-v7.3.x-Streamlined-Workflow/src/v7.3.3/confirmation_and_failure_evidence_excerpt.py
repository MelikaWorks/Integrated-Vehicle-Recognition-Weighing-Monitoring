"""Selected historical methods from Interface_Weighbridge_IP_v7_3_3_DB_Dev.py.
Imports, initialization and other application methods intentionally omitted.
Documentation excerpt only, not a complete runnable application.
"""

class WorkflowExcerpt:
    # Remaining application code omitted.

    def save_failed_frame(self, frame, index, reason):
        """Keep a bounded diagnostic sample for misses and OCR failures."""
        reason_keys = {
            "پلاک پیدا نشد": "not_found",
            "پلاک نامعتبر": "invalid_plate",
            "پلاک خارجی/نامعتبر": "foreign_or_invalid",
            "خروجی OCR ناقص بود": "ocr_incomplete",
            "خروجی OCR نامعتبر بود": "ocr_invalid",
            "حرف پلاک تشخیص داده نشد": "letter_not_detected",
            "exception": "exception",
        }
        reason_key = reason_keys.get(reason, "invalid_result")
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = self.failed_frames_dir / (
            f"failed_{stamp}_frame{index + 1}_{reason_key}.jpg")
        try:
            if not cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 90]):
                raise OSError("cv2.imwrite returned False")
            self.logger.info(
                "Failed frame saved: frame=%s reason=%s file=%s",
                index + 1, reason, path.name)

            # Prevent unattended pilot operation from filling the disk.
            saved = sorted(
                self.failed_frames_dir.glob("failed_*.jpg"),
                key=lambda item: item.stat().st_mtime,
                reverse=True)
            for old_path in saved[200:]:
                old_path.unlink(missing_ok=True)
        except Exception:
            self.logger.error("Could not save failed frame", exc_info=True)

    def save_manual_result(self, index):
        item = self.result_data[index]
        if item is None or self.closing:
            self.finish_manual_detection("این نتیجه برای ثبت معتبر نیست")
            return
        self.processing = True
        self.detect_button.configure(state="disabled")
        self.result_save_buttons[index].configure(state="disabled")
        parts, crop, original_frame = item
        self.status.configure(text="شماره خوانده‌شده را با تصویر پلاک مقایسه کنید")
        accepted = self.show_centered_dialog(
            "تأیید شماره پلاک",
            "شماره خوانده‌شده:",
            confirm=True, parent=self, accept_text="بله، ثبت شود",
            reject_text="خیر، ثبت دستی", plate_crop=crop, plate_parts=parts)
        if self.closing or self.detection_cancel.is_set() or not self.capture_running:
            self.finish_manual_detection("ثبت لغو شد؛ چیزی ذخیره نشد")
            return
        if not accepted:
            self.result_data[index] = None
            self.result_save_buttons[index].pack_forget()
            self.manual_reference_frame = original_frame.copy() if original_frame is not None else None
            self.finish_manual_detection("ثبت انجام نشد؛ شماره را اصلاح کنید")
            self.open_manual_entry(initial_parts=parts)
            return
        self.status.configure(text="شماره تأیید شد؛ در حال ثبت…")
        self.update_idletasks()
        try:
            warning = self.save_detection(parts, crop, original_frame, confirm=False)
        except Exception as exc:
            self.logger.error("Automatic registration failed", exc_info=True)
            message = str(exc) if isinstance(exc, DatabaseError) else "ذخیره تصویر یا ثبت انجام نشد؛ دسترسی پوشه را بررسی کنید"
            self.db_status.configure(text="ثبت نشد", text_color="#ff7777")
            self.result_save_buttons[index].configure(state="normal")
            self.result_save_buttons[index].pack(pady=(1, 4))
            self.finish_manual_detection(f"ثبت نشد: {message}؛ نتیجه حفظ شد")
            return
        self.clear_manual_results(update_status=False)
        self.manual_reference_frame = None
        self.finish_manual_detection(warning or "ثبت شد؛ آماده خودرو بعدی")

