"""Selected historical methods from Interface_Weighbridge_IP_v7_4_2_Agent.py.
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
        is_manual = 1 if source_override == "manual_entry" else 0
        safe_plate = "".join(char for char in parts["full"] if char.isalnum()) or "plate"
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

        # Transfer is performed once. Database failures must never repeat it.
        transfer_plate(parts)
        warnings = []
        event = {
            "plate": parts["full"], "registered_at_local": timestamp.isoformat(),
            "registration_source": record_source, "is_manual": is_manual,
            "towzin_code": None,
            "plate_image_path": str(plate_path.resolve()) if plate_path else None,
            "vehicle_image_path": str(vehicle_path.resolve()) if vehicle_path else None,
            "transfer_status": "verified", "database_status": "not_attempted",
        }
        event_path = self.output_dir / f"transfer_{stamp}.json"
        try:
            event_path.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            self.logger.error("Local transfer manifest could not be saved", exc_info=True)
            warnings.append("گزارش محلی کامل ذخیره نشد")

        try:
            AuditService().save_transfer(parts["full"], record_source, is_manual,
                                         plate_path, vehicle_path)
        except Exception:
            self.logger.error("Plate transferred; database audit could not be confirmed", exc_info=True)
            event["database_status"] = "unconfirmed"
            warnings.append("ثبت لاگ دیتابیس تأیید نشد؛ انتقال را تکرار نکنید")
        else:
            event["database_status"] = "committed"
        try:
            event_path.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            self.logger.error("Transfer manifest update failed", exc_info=True)

        try:
            with (self.output_dir / "plates.txt").open("a", encoding="utf-8-sig") as stream:
                stream.write(f"{timestamp:%Y-%m-%d %H:%M:%S} | {parts['display']} | "
                             f"{parts['full']} | {record_source} | is_manual={is_manual}\n")
            csv_path = self.output_dir / "transfers.csv"
            write_header = not csv_path.exists()
            with csv_path.open("a", newline="", encoding="utf-8-sig") as stream:
                writer = csv.writer(stream)
                if write_header:
                    writer.writerow(["date_time", "plate_full", "part_1", "letter", "part_2",
                                     "iran_code", "source", "is_manual", "database_status"])
                writer.writerow([timestamp.isoformat(), parts["full"], parts["part1"],
                                 parts["letter"], parts["part2"], parts["iran_code"],
                                 record_source, is_manual, event["database_status"]])
        except Exception:
            self.logger.error("Plate transferred; local text/CSV logging failed", exc_info=True)
            warnings.append("نوشتن لاگ محلی ناموفق بود")
        self.logger.info("Plate transferred: %s; source=%s; is_manual=%s; audit=%s",
                         parts["full"], record_source, is_manual, event["database_status"])
        self.db_status.configure(
            text="پلاک منتقل شد؛ " + ("؛ ".join(warnings) if warnings else "لاگ دیتابیس ثبت شد"),
            text_color="#ffbb55" if warnings else "#66ff99")
        return "پلاک منتقل شد؛ " + "؛ ".join(warnings) if warnings else None

