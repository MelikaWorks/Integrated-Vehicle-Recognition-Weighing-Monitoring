"""Four-frame recognition, operator selection and entry into manual fallback. The manual-entry form implementation is omitted.
Selected historical methods only; initialization, imports and other methods
are intentionally omitted. This is not a runnable application/module.
Source: Interface_Weighbridge_IP_v7_2_0_DB_Dev.py
"""

class HistoricalExcerpt:
    # Other application code intentionally omitted.

    def on_manual_entry_button_clicked(self):
        """Dedicated handler used only by the manual-entry button."""
        self.logger.info("UI action: open manual plate entry")
        self.open_manual_entry()

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

    def show_manual_result(self, index, result, crop, original_frame, error=None):
        if error:
            self.set_result_message(index, "خطای پردازش", "#ff7777")
            return
        parts = self.split_plate(result) if result else None
        if parts is None:
            messages = {
                "پلاک پیدا نشد": "این فریم خوانده نشد",
                "پلاک نامعتبر": "این فریم خوانده نشد",
                "پلاک خارجی/نامعتبر": "الگوی پلاک تأیید نشد",
                "خروجی OCR ناقص بود": "این فریم خوانده نشد",
                "خروجی OCR نامعتبر بود": "این فریم خوانده نشد",
                "حرف پلاک تشخیص داده نشد": "این فریم خوانده نشد",
            }
            self.set_result_message(
                index, messages.get(result, "نتیجه نامعتبر"), "#bbbbbb")
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
        except RegistrationCancelled:
            self.status.configure(text="ثبت پلاک لغو شد")
            return
        except Exception as exc:
            message = (
                str(exc) if isinstance(exc, DatabaseError)
                else "پلاک ذخیره نشد؛ دسترسی پوشه و فضای دیسک را بررسی کنید."
            )
            self.show_friendly_error(
                "خطای ذخیره‌سازی",
                message,
                exc)
            return
        self.clear_manual_results(update_status=False)
        self.status.configure(text="پلاک ثبت شد؛ آماده خودرو بعدی")
        messagebox.showinfo(
            "ذخیره شد",
            "پلاک انتخاب‌شده در رکورد توزین و فایل‌های محلی ذخیره شد.\n"
            "نتایج برای خودروی بعدی پاک شدند.",
            parent=self,
        )

