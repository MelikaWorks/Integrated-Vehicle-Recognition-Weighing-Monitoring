"""Selected historical methods from agent_bridge.py.
Imports, initialization and remaining application code intentionally omitted.
Documentation excerpt only, not a standalone executable implementation.
"""

def transfer_plate(parts):
    base = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    exe = base / "TowzinPlateAgent.exe"
    if not exe.is_file():
        raise TransferError("فایل TowzinPlateAgent.exe کنار برنامه پیدا نشد.")
    if os.name != "nt":
        raise TransferError("انتقال به فرم توزین فقط روی ویندوز اجرا می‌شود.")
    values = [str(parts[k]).strip() for k in ("part1", "letter", "part2", "iran_code")]
    for i, size in ((0, 2), (2, 3), (3, 2)):
        if len(values[i]) != size or any(c not in "0123456789" for c in values[i]):
            raise TransferError("شماره پلاک برای انتقال کامل نیست.")
    if not values[1]:
        raise TransferError("حرف پلاک خالی است.")
    with tempfile.TemporaryDirectory(prefix="towzin-transfer-") as folder:
        response = Path(folder) / "result.txt"
        command = [str(exe), "--transfer"] + values + [str(response)]
        try:
            process = subprocess.run(command, timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except subprocess.TimeoutExpired as exc:
            raise TransferError("پاسخ انتقال دریافت نشد؛ ممکن است پلاک وارد شده باشد. فرم توزین را بررسی کنید؛ انتقال خودکار تکرار نشد.") from exc
        except OSError as exc:
            raise TransferError("ایجنت اجرا نشد؛ مسیر، دسترسی و نصب .NET را بررسی کنید.") from exc
        result = response.read_text(encoding="utf-8-sig").splitlines() if response.is_file() else []
        expected = "".join(values)
        if process.returncode == 0 and result == ["OK", expected]:
            return expected
        message = "\n".join(result[1:]) or "پاسخ معتبر از ایجنت دریافت نشد."
        if not result or result[0] == "PARTIAL" or process.returncode == 4:
            message += "\nممکن است انتقال انجام شده یا ناقص باشد؛ قبل از تلاش مجدد، فیلدهای توزین را بررسی کنید."
        raise TransferError(message)

