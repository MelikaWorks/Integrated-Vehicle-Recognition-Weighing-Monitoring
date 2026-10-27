"""Historical experimental write path, abandoned because latest-row selection cannot identify the current weighing transaction. Includes additional car/audit/auxiliary-table writes found in the original method; not a recommended implementation.
Selected historical methods only; initialization, imports and other methods
are intentionally omitted. This is not a runnable application/module.
Source: old vesion/database_service - Copy.py
"""

class HistoricalExcerpt:
    # Other application code intentionally omitted.

    def save_plate_to_latest(
            self, expected_towzin_code, plate, registration_source=None,
            plate_image_name=None, plate_image_path=None,
            vehicle_image_name=None, vehicle_image_path=None):
        """Register a plate atomically in car, towzin and audit tables."""
        expected_code = self._normalize_code(expected_towzin_code)
        normalized_plate = self._normalize_plate(plate)
        if not expected_code:
            raise DatabaseError("کد توزین انتخاب‌شده خالی است.")
        if not normalized_plate:
            raise DatabaseError("شماره پلاک برای ثبت خالی است.")

        with self.connect() as connection:
            connection.autocommit = False
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    SELECT TOP 1 towzin_code, car_pelak,
                           ISNULL(towzin_emptyweight, 0),
                           ISNULL(towzin_fullweight, 0),
                           towzin_date, towzin_time
                    FROM dbo.towzin_tb WITH (UPDLOCK, HOLDLOCK)
                    WHERE towzin_code IS NOT NULL
                    ORDER BY towzin_code DESC
                    """
                )
                row = cursor.fetchone()
                if row is None:
                    raise WeighingNotFoundError(
                        "هیچ رکورد توزینی در دیتابیس پیدا نشد."
                    )

                latest_code = str(row[0])
                current_plate = self._normalize_plate(row[1])
                if latest_code != expected_code:
                    raise LatestWeighingChangedError(
                        "در فاصله تأیید، توزین جدیدی ثبت شد؛ دوباره ثبت پلاک را بزنید."
                    )

                cursor.execute(
                    """
                    SELECT TOP 1 car_pelak
                    FROM dbo.car_tb WITH (UPDLOCK, HOLDLOCK)
                    WHERE car_pelak = ?
                    """,
                    normalized_plate,
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        """
                        INSERT INTO dbo.car_tb
                            (car_pelak, car_name, car_type,
                             car_towzinprice, car_emptyweight,
                             car_emptydate1, car_emptydate2, car_emptytime,
                             status, driver_code)
                        VALUES (?, NULL, ?, 0, 0, NULL, NULL, NULL, ?, ?)
                        """,
                        normalized_plate,
                        "بدون نوع",
                        "0",
                        "بدون راننده",
                    )

                cursor.execute(
                    """
                    UPDATE dbo.towzin_tb
                    SET car_pelak = ?
                    WHERE towzin_code = ?
                      AND ISNULL(car_pelak, '') = ?
                    """,
                    normalized_plate,
                    latest_code,
                    current_plate,
                )
                if cursor.rowcount != 1:
                    raise DatabaseError(
                        "رکورد توزین در زمان ثبت تغییر کرده است؛ دوباره تلاش کنید."
                    )

                cursor.execute(
                    """
                    INSERT INTO dbo.plate_reader_log
                        (towzin_code, car_pelak, registered_at,
                         registration_source,
                         plate_image_name, plate_image_path,
                         vehicle_image_name, vehicle_image_path)
                    VALUES (?, ?, GETDATE(), ?, ?, ?, ?, ?)
                    """,
                    latest_code,
                    normalized_plate,
                    registration_source,
                    plate_image_name,
                    plate_image_path,
                    vehicle_image_name,
                    vehicle_image_path,
                )

                cursor.execute(
                    """
                    INSERT INTO dbo.a (b)                        
                    VALUES (?)
                    """,
                    normalized_plate,
                )
                if cursor.rowcount !=1:
                    raise DatabaseError("پلاک در جدول a ثبت نشد")

                connection.commit()
                return WeighingRecord(
                    towzin_code=latest_code,
                    car_pelak=normalized_plate,
                    empty_weight=float(row[2] or 0),
                    full_weight=float(row[3] or 0),
                    towzin_date=str(row[4] or ""),
                    towzin_time=str(row[5] or ""),
                )
            except DatabaseError:
                connection.rollback()
                raise
            except pyodbc.Error as exc:
                connection.rollback()
                raise DatabaseError(
                    "ثبت پلاک در دیتابیس کامل نشد؛ هیچ تغییری ذخیره نشد."
                ) from exc
            except Exception:
                connection.rollback()
                raise

