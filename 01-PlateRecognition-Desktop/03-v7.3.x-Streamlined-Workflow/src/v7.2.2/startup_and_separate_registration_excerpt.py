"""Selected historical methods from Interface_Weighbridge_IP_v7_2_2_DB_Dev.py.
Imports, initialization and other application methods intentionally omitted.
Documentation excerpt only, not a complete runnable application.
"""

class WorkflowExcerpt:
    # Remaining application code omitted.

    def begin_startup_connection(self):
        if self.closing:
            return
        self.withdraw()
        window = ctk.CTkToplevel(self)
        self.startup_window = window
        window.title("راه‌اندازی پلاک‌خوان")
        window.resizable(False, False)
        width, height = 360, 120
        x = max(0, (self.winfo_screenwidth() - width) // 2)
        y = max(0, (self.winfo_screenheight() - height) // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
        ctk.CTkLabel(window, text="در حال اتصال به دوربین…",
                     font=self.font_normal).pack(expand=True, padx=15, pady=20)
        window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.startup_after = self.after(10000, self.finish_startup_connection)
        self.start_ip_camera()

    def finish_startup_connection(self):
        if self.startup_after is not None:
            self.after_cancel(self.startup_after)
            self.startup_after = None
        if self.startup_window is not None:
            self.startup_window.destroy()
            self.startup_window = None
        if not self.closing:
            self.deiconify()
            self.lift()

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
        self.dialog_showinfo(
            "ذخیره شد",
            "پلاک انتخاب‌شده در جدول پلاک‌خوان و فایل‌های محلی ذخیره شد.\n"
            "نتایج برای خودروی بعدی پاک شدند.",
            parent=self,
        )

