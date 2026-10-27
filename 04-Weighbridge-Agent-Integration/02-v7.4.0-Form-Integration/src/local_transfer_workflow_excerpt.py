"""Selected historical methods from Interface_Weighbridge_IP_v7_4_0_Agent.py.
Imports, initialization and remaining application code intentionally omitted.
Documentation excerpt only, not a standalone executable implementation.
"""

class HistoricalExcerpt:
    # Other application members omitted.

    def save_detection(
            self, parts, crop, original_frame, source_override=None, confirm=True):
        timestamp = datetime.now()
        stamp = timestamp.strftime("%Y%m%d_%H%M%S_%f")
        record_source = source_override or self.current_source
        safe_plate = "".join(
            char for char in parts["full"] if char.isalnum()) or "plate"
        file_stem = f"{safe_plate}_{stamp}"
        vehicle_path = None
        plate_path = None
        if original_frame is not None:
            vehicle_path = self.output_dir / f"vehicle_{file_stem}.jpg"
            if not cv2.imwrite(str(vehicle_path), original_frame):
                raise OSError("Vehicle image could not be written")
        if crop is not None:
            plate_path = self.output_dir / f"plate_{file_stem}.jpg"
            crop.save(plate_path, quality=95)

        transfer_plate(parts)
        self.db_status.configure(text="پلاک به فرم توزین منتقل شد", text_color="#66ff99")

        try:
            txt_path = self.output_dir / "plates.txt"
            csv_path = self.output_dir / "plates.csv"
            with txt_path.open("a", encoding="utf-8-sig") as stream:
                stream.write(
                    f"{timestamp:%Y-%m-%d %H:%M:%S} | "
                    f"{parts['display']} | {parts['full']} | {record_source}\n")
            write_header = not csv_path.exists()
            with csv_path.open("a", newline="", encoding="utf-8-sig") as stream:
                writer = csv.writer(stream)
                if write_header:
                    writer.writerow([
                        "date_time", "plate_full", "part_1", "letter",
                        "part_2", "iran_code", "special_plate", "source"
                    ])
                writer.writerow([
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    parts["full"], parts["part1"], parts["letter"],
                    parts["part2"], parts["iran_code"],
                    "yes" if parts["special"] else "no", record_source
                ])
        except Exception:
            self.logger.error("Plate transferred but local text/CSV log failed", exc_info=True)
            return "پلاک منتقل شد؛ نوشتن لاگ محلی ناموفق بود؛ انتقال را تکرار نکنید"
        self.logger.info(
            "Plate saved successfully: %s; source=%s; image=%s",
            parts["full"], record_source,
            "yes" if original_frame is not None else "no")
        return None

