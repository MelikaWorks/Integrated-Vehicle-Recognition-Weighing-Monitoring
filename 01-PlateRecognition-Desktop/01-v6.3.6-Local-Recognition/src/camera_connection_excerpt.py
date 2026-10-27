"""Selected methods from the v6.3.6 desktop application.
Documentation excerpts only: omitted UI, initialization and runtime dependencies
mean this file is not a standalone executable application.
"""

class DesktopWorkflowExcerpt:
    # Initialization and other application methods intentionally omitted.

    def start_ip_camera(self):
        """Connect to the Milesight camera's H.264 secondary RTSP stream."""
        if self.capture_running:
            self.status.configure(text="دوربین از قبل متصل است")
            return
        camera_ip = simpledialog.askstring(
            "دوربین IP", "آدرس IP دوربین:",
            initialvalue=DEFAULT_CAMERA_IP, parent=self)
        if not camera_ip:
            return
        username = simpledialog.askstring(
            "دوربین IP", "نام کاربری:",
            initialvalue=DEFAULT_CAMERA_USER, parent=self)
        if username is None:
            return
        password = simpledialog.askstring(
            "دوربین IP", "رمز دوربین:", show="*", parent=self)
        if password is None:
            return

        safe_user = quote(username, safe="")
        safe_password = quote(password, safe="")
        rtsp_url = (
            f"rtsp://{safe_user}:{safe_password}@{camera_ip.strip()}:"
            f"{DEFAULT_RTSP_PORT}/{DEFAULT_RTSP_PATH}"
        )
        self.stop_capture()
        self.current_source = "ip_camera"
        self.ip_camera_button.configure(
            state="disabled", text="در حال اتصال…")
        self.status.configure(text="در حال اتصال به دوربین شبکه…")
        threading.Thread(
            target=self.open_ip_camera_worker,
            args=(rtsp_url,), daemon=True).start()

    def open_ip_camera_worker(self, rtsp_url):
        # Keep low-level FFmpeg/OpenCV diagnostics out of normal operator use.
        # Connection failures are reported in Persian inside the application.
        try:
            if hasattr(cv2, "setLogLevel"):
                cv2.setLogLevel(0)
            elif hasattr(cv2, "utils") and hasattr(cv2.utils, "logging"):
                cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_SILENT)
        except Exception:
            pass
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
            "rtsp_transport;tcp|stimeout;8000000"
        )
        capture = cv2.VideoCapture()
        try:
            if hasattr(cv2, "CAP_PROP_OPEN_TIMEOUT_MSEC"):
                capture.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 8000)
            if hasattr(cv2, "CAP_PROP_READ_TIMEOUT_MSEC"):
                capture.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
            if not capture.open(rtsp_url, cv2.CAP_FFMPEG):
                capture.release()
                self.logger.warning("IP camera connection failed")
                self.after(0, self.show_ip_connection_error)
                return
        except Exception as exc:
            capture.release()
            self.logger.error("IP camera open failed", exc_info=True)
            self.after(0, lambda e=exc: self.show_ip_connection_exception(e))
            return
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.capture = capture
        self.capture_running = True
        # The live stream stays open, but inference starts only when the
        # operator presses the manual detection button.
        self.auto_active = False
        with self.frame_lock:
            self.frame_buffer.clear()
            self.latest_frame = None
        self.votes.clear()
        self.consecutive_misses = 0
        self.last_process_time = 0.0
        self.after(0, lambda: self.on_ip_camera_opened(capture))

