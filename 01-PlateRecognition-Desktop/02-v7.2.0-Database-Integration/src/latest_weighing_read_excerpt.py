"""Read-only retrieval of latest weighing context.
Selected historical methods only; initialization, imports and other methods
are intentionally omitted. This is not a runnable application/module.
Source: database_service.py
"""

class HistoricalExcerpt:
    # Other application code intentionally omitted.

    def get_latest_weighing(self):
        """Return the newest weighbridge row without changing any data."""
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT TOP 1 towzin_code, car_pelak,
                       ISNULL(towzin_emptyweight, 0),
                       ISNULL(towzin_fullweight, 0),
                       towzin_date, towzin_time
                FROM dbo.towzin_tb
                WHERE towzin_code IS NOT NULL
                ORDER BY towzin_code DESC
                """
            )
            row = cursor.fetchone()
        if row is None:
            raise WeighingNotFoundError("هیچ رکورد توزینی در دیتابیس پیدا نشد.")
        return WeighingRecord(
            towzin_code=str(row[0]),
            car_pelak=self._normalize_plate(row[1]),
            empty_weight=float(row[2] or 0),
            full_weight=float(row[3] or 0),
            towzin_date=str(row[4] or ""),
            towzin_time=str(row[5] or ""),
        )

