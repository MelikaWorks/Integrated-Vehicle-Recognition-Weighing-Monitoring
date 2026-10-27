"""Selected methods from the v6.3.6 desktop application.
Documentation excerpts only: omitted UI, initialization and runtime dependencies
mean this file is not a standalone executable application.
"""

class DesktopWorkflowExcerpt:
    # Initialization and other application methods intentionally omitted.

    def manual_detect(self):
        """Freeze four recent independent frames, then process the copies."""
        if not self.capture_running or self.capture is None:
            self.status.configure(text="ابتدا دوربین شبکه را متصل کنید")
            return
        if self.processing:
            self.status.configure(text="تشخیص قبلی هنوز در حال انجام است…")
            return
        with self.frame_lock:
            buffered = list(self.frame_buffer)
        if len(buffered) < MANUAL_FRAME_COUNT:
            self.status.configure(text="چند لحظه صبر کنید تا فریم‌های دوربین آماده شوند")
            return

        # Use frames spread over roughly the last half second. They are copied
        # before inference starts, so a moving truck cannot escape mid-process.
        span = min(len(buffered) - 1, 15)
        indices = np.linspace(
            len(buffered) - 1 - span,
            len(buffered) - 1,
            MANUAL_FRAME_COUNT,
            dtype=int,
        )
        frames = [buffered[index].copy() for index in indices]
        self.clear_manual_results(update_status=False)
        self.processing = True
        self.detect_button.configure(state="disabled")
        self.status.configure(text="چهار فریم ذخیره شد؛ در حال تشخیص…")
        threading.Thread(
            target=self.manual_inference_worker,
            args=(frames,), daemon=True).start()

    def manual_inference_worker(self, frames):
        try:
            for index, frame in enumerate(frames):
                pil_image = Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                try:
                    result, crop = backend.predict_plate(pil_image)
                    error = None
                except Exception as exc:
                    result, crop, error = "خطای تشخیص", None, str(exc)
                    self.logger.error(
                        "Plate inference failed for manual frame %s",
                        index + 1, exc_info=True)
                self.after(
                    0,
                    lambda i=index, r=result, c=crop, f=frame, e=error:
                    self.show_manual_result(i, r, c, f, e),
                )
        finally:
            self.after(0, self.finish_manual_detection)

    def show_manual_result(self, index, result, crop, original_frame, error=None):
        if error:
            self.set_result_message(index, "خطا", "#ff7777")
            return
        parts = self.split_plate(result) if result else None
        if parts is None:
            message = result if result in (
                "پلاک پیدا نشد", "پلاک نامعتبر", "پلاک خارجی/نامعتبر"
            ) else "نامعتبر"
            if message in ("پلاک نامعتبر", "پلاک پیدا نشد", "پلاک خارجی/نامعتبر"):
                message = "فریم مناسب نبود"
            self.set_result_message(index, message, "#bbbbbb")
            return

        self.result_data[index] = (
            parts,
            crop.copy() if crop is not None else None,
            original_frame.copy(),
        )
        self.set_result_plate(index, parts)
        self.result_save_buttons[index].configure(state="normal")
        if crop is not None:
            shown_crop = crop.copy()
            shown_crop.thumbnail(
                (CROP_WIDTH, CROP_HEIGHT), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (CROP_WIDTH, CROP_HEIGHT), "white")
            canvas.paste(
                shown_crop,
                ((CROP_WIDTH - shown_crop.width) // 2,
                 (CROP_HEIGHT - shown_crop.height) // 2),
            )
            result_image = ctk.CTkImage(
                light_image=canvas,
                dark_image=canvas,
                size=(CROP_WIDTH, CROP_HEIGHT),
            )
            self.result_images[index] = result_image
            self.result_image_labels[index].configure(
                image=result_image, text="")

    def save_manual_result(self, index):
        item = self.result_data[index]
        if item is None:
            self.status.configure(text="این نتیجه برای ثبت معتبر نیست")
            return
        parts, crop, original_frame = item
        try:
            self.save_detection(parts, crop, original_frame)
        except Exception as exc:
            self.show_friendly_error(
                "خطای ذخیره‌سازی",
                "پلاک ذخیره نشد؛ دسترسی پوشه و فضای دیسک را بررسی کنید.",
                exc)
            return
        self.clear_manual_results(update_status=False)
        self.status.configure(text="پلاک ثبت شد؛ آماده خودرو بعدی")
        messagebox.showinfo(
            "ذخیره شد",
            "پلاک انتخاب‌شده ذخیره شد.\nنتایج برای خودروی بعدی پاک شدند.",
            parent=self,
        )

