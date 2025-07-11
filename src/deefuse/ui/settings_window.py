from __future__ import annotations

import customtkinter as ctk
from tkinter import filedialog
from ..settings import settings, save_settings, Settings
from .. import config


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.on_save = on_save
        self.title("Settings")
        self.geometry("420x220")
        self.resizable(False, False)

        self.auto_var = ctk.BooleanVar(value=settings.auto_search_on_click)
        self.csv_var = ctk.StringVar(value=settings.csv_dir)
        self.quality_var = ctk.StringVar(value=settings.target_quality)

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 20, "pady": 6}
        ctk.CTkCheckBox(
            self,
            text="Search skipped tracks on click",
            variable=self.auto_var,
        ).pack(anchor="w", **pad)

        dir_frame = ctk.CTkFrame(self, fg_color="transparent")
        dir_frame.pack(fill="x", **pad)
        ctk.CTkLabel(dir_frame, text="CSV Directory:").grid(row=0, column=0, sticky="w")
        entry = ctk.CTkEntry(dir_frame, textvariable=self.csv_var, width=240)
        entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        dir_frame.columnconfigure(1, weight=1)
        ctk.CTkButton(dir_frame, text="Browse", command=self._browse_csv).grid(row=0, column=2, padx=6)

        qual_frame = ctk.CTkFrame(self, fg_color="transparent")
        qual_frame.pack(fill="x", **pad)
        ctk.CTkLabel(qual_frame, text="Target Quality:").grid(row=0, column=0, sticky="w")
        ctk.CTkOptionMenu(qual_frame, values=["flac", "320"], variable=self.quality_var).grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Save", command=self._save).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=10)

    def _browse_csv(self):
        path = filedialog.askdirectory(initialdir=self.csv_var.get())
        if path:
            self.csv_var.set(path)

    def _save(self):
        settings.auto_search_on_click = self.auto_var.get()
        settings.csv_dir = self.csv_var.get()
        settings.target_quality = self.quality_var.get()
        save_settings(settings)
        config.reload_settings(settings)
        if callable(self.on_save):
            self.on_save()
        self.destroy()
