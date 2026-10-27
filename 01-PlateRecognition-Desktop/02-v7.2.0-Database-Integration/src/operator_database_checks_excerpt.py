"""v7.2.0 operator checks and historical latest-record confirmation. The confirmation wording predates the later database write strategy.
Selected historical methods only; initialization, imports and other methods
are intentionally omitted. This is not a runnable application/module.
Source: Interface_Weighbridge_IP_v7_2_0_DB_Dev.py
"""

class HistoricalExcerpt:
    # Other application code intentionally omitted.

    def check_database_connection(self):
        """Verify the configured SQL Server without changing any data."""
        try:
            database_name = self.db_service.test_connection()
        except DatabaseError as exc:
            self.logger.error("Database connection test failed", exc_info=True)
            self.db_status.configure(
                text="اتصال دیتابیس برقرار نشد", text_color="#ff7777")
            messagebox.showerror(
                "خطای دیتابیس", str(exc), parent=self)
            return
        self.db_status.configure(
            text=f"متصل: {database_name}", text_color="#66ff99")
        messagebox.showinfo(
            "اتصال برقرار است",
            f"اتصال به دیتابیس {database_name} موفق بود.",
            parent=self,
        )

    def check_latest_weighing(self, show_dialog=True):
        """Load the newest weighbridge record without changing it."""
        try:
            record = self.db_service.get_latest_weighing()
        except DatabaseError as exc:
            self.last_db_record = None
            self.db_status.configure(text=str(exc), text_color="#ff7777")
            if show_dialog:
                messagebox.showerror("توزین پیدا نشد", str(exc), parent=self)
            return None
        self.last_db_record = record
        current_plate = record.car_pelak or "ثبت نشده"
        self.db_status.configure(
            text=(f"آخرین توزین: {record.towzin_code} | "
                  f"{record.towzin_date} {record.towzin_time} | "
                  f"پلاک فعلی: {current_plate}"),
            text_color="#66ff99",
        )
        if show_dialog:
            messagebox.showinfo(
                "آخرین رکورد توزین",
                f"کد توزین: {record.towzin_code}\n"
                f"تاریخ: {record.towzin_date}\n"
                f"ساعت: {record.towzin_time}\n"
                f"پلاک فعلی: {current_plate}\n"
                f"وزن خالی: {record.empty_weight:g}\n"
                f"وزن پر: {record.full_weight:g}",
                parent=self,
            )
        return record

    def prepare_database_registration(self, parts):
        """Show the current newest weighing and obtain operator approval."""
        record = self.check_latest_weighing(show_dialog=False)
        if record is None:
            raise DatabaseError("آخرین رکورد توزین قابل دریافت نیست.")
        current_plate = record.car_pelak or "ثبت نشده"
        if not messagebox.askyesno(
                "تأیید ثبت در دیتابیس",
                f"کد توزین: {record.towzin_code}\n"
                f"تاریخ و ساعت: {record.towzin_date} {record.towzin_time}\n"
                f"پلاک فعلی: {current_plate}\n"
                f"پلاک جدید: {parts['display']}\n\n"
                "پلاک جدید در آخرین رکورد توزین ثبت شود؟",
                parent=self):
            raise RegistrationCancelled("ثبت پلاک توسط کاربر لغو شد.")
        return record

