"""Selected historical methods from Interface_Weighbridge_IP_v7_3_3_DB_Dev.py.
Imports, initialization and other application methods intentionally omitted.
Documentation excerpt only, not a complete runnable application.
"""

class WorkflowExcerpt:
    # Remaining application code omitted.

    def show_centered_dialog(self, title, message, confirm=False, parent=None,
                             accept_text=None, reject_text=None, plate_crop=None, plate_parts=None):
        """Display a modal message centered over the control window."""
        owner = self
        dialog = ctk.CTkToplevel(owner)
        dialog.withdraw()
        dialog.title(title)
        dialog.transient(owner)
        dialog.resizable(False, False)
        result = [False]
        previous_focus = self.focus_get()
        previous_grab = self.grab_current()

        def finish(value=False):
            result[0] = value
            dialog.destroy()

        ctk.CTkLabel(
            dialog, text=message, font=self.font_normal,
            wraplength=310, justify="center").pack(
                fill="x", padx=18, pady=(18, 12))
        if plate_parts is not None:
            plate_line = ctk.CTkFrame(dialog, fg_color="transparent")
            plate_line.pack(pady=(0, 12))
            for value, width in (
                    (plate_parts["part1"], 28), (plate_parts["letter"], 24),
                    (plate_parts["part2"], 38), ("ایران", 40),
                    (plate_parts["iran_code"], 28)):
                ctk.CTkLabel(
                    plate_line, text=value, width=width, font=self.font_plate,
                    text_color="#66ff99", anchor="center"
                ).pack(side="left", padx=1)
            ctk.CTkLabel(
                dialog, text="آیا شماره پلاک درست است؟", font=self.font_normal
            ).pack(pady=(0, 12))
        if plate_crop is not None:
            preview = plate_crop.copy()
            preview.thumbnail((280, 120), Image.Resampling.LANCZOS)
            preview_image = ctk.CTkImage(light_image=preview, dark_image=preview,
                                        size=preview.size)
            preview_label = ctk.CTkLabel(dialog, text="", image=preview_image)
            preview_label.image = preview_image
            preview_label.pack(padx=18, pady=(0, 12))
        actions = ctk.CTkFrame(dialog, fg_color="transparent")
        actions.pack(pady=(0, 16))
        accept = ctk.CTkButton(
            actions, text=accept_text or ("تأیید" if confirm else "باشه"),
            width=130 if accept_text else 100, font=self.font_button,
            command=lambda: finish(True))
        accept.pack(side="right", padx=5)
        if confirm:
            ctk.CTkButton(
                actions, text=reject_text or "لغو", width=130,
                font=self.font_button,
                fg_color="#b7791f" if plate_parts is not None else "#555555",
                hover_color="#916018" if plate_parts is not None else "#444444",
                command=lambda: finish(False)).pack(side="right", padx=5)
        dialog.protocol("WM_DELETE_WINDOW", lambda: finish(False))
        dialog.bind("<Escape>", lambda event: finish(False))
        dialog.update_idletasks()
        owner.update_idletasks()
        width = max(350, dialog.winfo_reqwidth())
        height = dialog.winfo_reqheight()
        x = owner.winfo_rootx() + (owner.winfo_width() - width) // 2
        y = owner.winfo_rooty() + (owner.winfo_height() - height) // 2
        x = max(0, min(x, owner.winfo_screenwidth() - width))
        y = max(0, min(y, owner.winfo_screenheight() - height - 40))
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        dialog.deiconify()
        dialog.lift()
        dialog.grab_set()
        # Focus Cancel on confirmations to avoid accidental acceptance.
        dialog.focus_set() if confirm else accept.focus_set()
        owner.wait_window(dialog)
        if previous_grab is not None:
            try:
                if previous_grab.winfo_exists():
                    previous_grab.grab_set()
            except Exception:
                pass
        try:
            if previous_focus is not None and previous_focus.winfo_exists():
                previous_focus.focus_set()
        except Exception:
            pass
        return result[0]

