"""Selected methods from the v6.3.6 desktop application.
Documentation excerpts only: omitted UI, initialization and runtime dependencies
mean this file is not a standalone executable application.
"""

class DesktopWorkflowExcerpt:
    # Initialization and other application methods intentionally omitted.

    def save_detection(self, parts, crop, original_frame):
        timestamp = datetime.now()
        stamp = timestamp.strftime("%Y%m%d_%H%M%S")
        txt_path = self.output_dir / "plates.txt"
        csv_path = self.output_dir / "plates.csv"
        with txt_path.open("a", encoding="utf-8-sig") as stream:
            stream.write(
                f"{timestamp:%Y-%m-%d %H:%M:%S} | "
                f"{parts['display']} | {parts['full']}\n")
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
                "yes" if parts["special"] else "no", self.current_source
            ])
        if not cv2.imwrite(
                str(self.output_dir / f"vehicle_{stamp}.jpg"), original_frame):
            raise OSError("Vehicle image could not be written")
        if crop is not None:
            crop.save(
                self.output_dir / f"plate_{stamp}.jpg", quality=95)
        self.logger.info("Plate saved successfully: %s", parts["full"])

