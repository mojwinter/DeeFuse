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
        self.geometry("500x500")
        self.resizable(False, False)
        
        # Ensure window appears on top of parent
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        # Center the window on the parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (500 // 2)
        self.geometry(f"500x500+{x}+{y}")

        self.auto_var = ctk.BooleanVar(value=settings.auto_search_on_click)
        self.csv_var = ctk.StringVar(value=settings.csv_dir)
        self.quality_var = ctk.StringVar(value=settings.target_quality)

        self._build_ui()

    def _build_ui(self):
        # Main container with transparent background
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Settings sections
        self._build_auto_search_section(main_frame)
        self._build_csv_section(main_frame)
        self._build_quality_section(main_frame)
        
        # Buttons
        self._build_buttons(main_frame)

    def _build_auto_search_section(self, parent):
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(0, 20))
        header_label = ctk.CTkLabel(
            section_frame, 
            text="Search Behavior", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header_label.pack(anchor="w", pady=(0, 10))
        checkbox_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        checkbox_frame.pack(fill="x")
        ctk.CTkCheckBox(
            checkbox_frame,
            text="Auto-search on track selection",
            variable=self.auto_var,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")
        desc_label = ctk.CTkLabel(
            checkbox_frame,
            text="Automatically search Deezer when clicking on a skipped track",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        desc_label.pack(anchor="w", padx=(25, 0), pady=(5, 0))

    def _build_csv_section(self, parent):
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(0, 20))
        header_label = ctk.CTkLabel(
            section_frame, 
            text="Data Storage", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header_label.pack(anchor="w", pady=(0, 10))
        dir_label = ctk.CTkLabel(
            section_frame, 
            text="CSV Directory:", 
            font=ctk.CTkFont(size=12)
        )
        dir_label.pack(anchor="w", pady=(0, 8))
        dir_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        dir_frame.pack(fill="x")
        dir_frame.columnconfigure(1, weight=1)
        entry = ctk.CTkEntry(
            dir_frame, 
            textvariable=self.csv_var, 
            placeholder_text="Select directory for CSV files...",
            height=32,
            fg_color="transparent"
        )
        entry.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(0, 12))
        ctk.CTkButton(
            dir_frame, 
            text="Browse", 
            command=self._browse_csv,
            width=80,
            height=32
        ).grid(row=0, column=2)
        # Description under the entry
        desc_label = ctk.CTkLabel(
            section_frame,
            text="Matched and skipped track .csv files are saved in this directory.",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        desc_label.pack(anchor="w", pady=(8, 0))

    def _build_quality_section(self, parent):
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(0, 20))
        header_label = ctk.CTkLabel(
            section_frame, 
            text="Download Quality", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header_label.pack(anchor="w", pady=(0, 10))
        qual_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        qual_frame.pack(fill="x")
        qual_frame.columnconfigure(1, weight=1)
        ctk.CTkLabel(
            qual_frame, 
            text="Target Quality:", 
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, sticky="w")
        quality_menu = ctk.CTkOptionMenu(
            qual_frame, 
            values=["flac", "mp3 320"], 
            variable=self.quality_var,
            width=120,
            height=32
        )
        quality_menu.grid(row=0, column=1, sticky="w", padx=(12, 0))
        desc_label = ctk.CTkLabel(
            qual_frame,
            text="flac: Lossless (best quality, largest files) | mp3 320: High quality MP3 (smaller files)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        desc_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))

    def _build_buttons(self, parent):
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        save_btn = ctk.CTkButton(
            btn_frame, 
            text="Save Settings", 
            command=self._save,
            fg_color="#28a745",
            hover_color="#23913c",
            height=36
        )
        save_btn.pack(side="right", padx=(12, 0))
        cancel_btn = ctk.CTkButton(
            btn_frame, 
            text="Cancel", 
            command=self.destroy,
            height=36
        )
        cancel_btn.pack(side="right")

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