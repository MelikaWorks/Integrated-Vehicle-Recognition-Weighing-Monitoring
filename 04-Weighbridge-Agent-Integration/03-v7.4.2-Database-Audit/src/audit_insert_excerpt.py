"""Selected historical methods from audit_service.py.
Imports, initialization and remaining application code intentionally omitted.
Documentation excerpt only, not a standalone executable implementation.
"""

class HistoricalExcerpt:
    # Other application members omitted.

    def save_transfer(self, plate, source, is_manual, plate_image=None, vehicle_image=None):
        if is_manual not in (0, 1):
            raise DatabaseError("حالت ثبت لاگ معتبر نیست.")
        connection = self.connect()
        try:
            connection.autocommit = False
            connection.timeout = int(self.config.get("timeout_seconds", 5))
            cursor = connection.cursor()
            # Read metadata only; never alter production schema or invent a weighing code.
            cursor.execute(
                "SELECT TYPE_NAME(system_type_id) FROM sys.columns "
                "WHERE object_id = OBJECT_ID(N'dbo.plate_reader_log') "
                "AND name = N'towzin_code'")
            column = cursor.fetchone()
            if not column or str(column[0]).lower() not in {"nvarchar", "varchar", "nchar", "char"}:
                raise DatabaseError(
                    "ستون towzin_code در جدول لاگ متنی نیست یا قابل بررسی نیست؛ "
                    "ثبت بدون شماره توزین انجام نشد. ساختار دیتابیس تغییر نکرد.")
            cursor.execute("INSERT INTO dbo.plate_detection (plate) VALUES (?)", plate)
            cursor.execute(
                """INSERT INTO dbo.plate_reader_log
                   (towzin_code, car_pelak, registered_at, registration_source,
                    plate_image_name, plate_image_path, vehicle_image_name,
                    vehicle_image_path, is_manual)
                   VALUES (N'', ?, GETDATE(), ?, ?, ?, ?, ?, ?)""",
                plate, source,
                Path(plate_image).name if plate_image else None,
                str(Path(plate_image).resolve()) if plate_image else None,
                Path(vehicle_image).name if vehicle_image else None,
                str(Path(vehicle_image).resolve()) if vehicle_image else None,
                int(is_manual))
            connection.commit()
        except Exception:
            try:
                connection.rollback()
            except Exception:
                pass
            raise
        finally:
            connection.close()

