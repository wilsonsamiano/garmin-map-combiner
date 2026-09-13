#!/usr/bin/env python3
"""Garmin Map Combiner — merge OSM/GMapTool .img files into one gmapsupp.img."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

APP_NAME = "Garmin Map Combiner"
MAX_BYTES = 4 * 1024 * 1024 * 1024 - 1024
HOME = Path.home()
DEFAULT_OUT = HOME / "Downloads" / "combined"

CANDIDATE_JAVA = [
    Path("/opt/homebrew/opt/openjdk/bin/java"),
    Path("/opt/homebrew/opt/openjdk@21/bin/java"),
    Path("/opt/homebrew/opt/openjdk@17/bin/java"),
    Path("/usr/libexec/java_home"),
]


def resource_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent.parent / "Resources"
    return Path(__file__).resolve().parent


def which_java() -> str | None:
    for p in CANDIDATE_JAVA:
        if p.name == "java_home" and p.parent.exists():
            try:
                home = subprocess.check_output([str(p)], text=True).strip()
                exe = Path(home) / "bin" / "java"
                if exe.is_file():
                    return str(exe)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            continue
        if p.is_file():
            return str(p)
    found = shutil.which("java")
    return found


def which_mkgmap() -> str | None:
    base = resource_dir()
    for p in (
        HOME / "Downloads" / "mkgmap-r4924" / "mkgmap.jar",
        HOME / "Downloads" / "mkgmap" / "mkgmap.jar",
        base / "vendor" / "mkgmap.jar",
        base / "mkgmap.jar",
    ):
        if p.is_file():
            return str(p)
    downloads = HOME / "Downloads"
    if downloads.is_dir():
        matches = sorted(downloads.glob("mkgmap-*/mkgmap.jar"))
        if matches:
            return str(matches[-1])
    return None


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry("780x620")
        self.minsize(640, 520)
        self.configure(bg="#0c0e0c")
        self.files: list[str] = []
        self.java = which_java()
        self._style()
        self._menu()
        self._build()

    def _style(self) -> None:
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        bg, surface, fg, muted, accent = (
            "#0c0e0c",
            "#141714",
            "#eceee9",
            "#9aa196",
            "#d7dbd4",
        )
        s.configure(".", background=bg, foreground=fg, fieldbackground=surface)
        s.configure("TFrame", background=bg)
        s.configure("Card.TFrame", background=surface)
        s.configure("TLabel", background=bg, foreground=fg, font=("TkDefaultFont", 12))
        s.configure("Muted.TLabel", background=bg, foreground=muted, font=("TkDefaultFont", 11))
        s.configure("Title.TLabel", background=bg, foreground=fg, font=("TkDefaultFont", 20, "bold"))
        s.configure("TButton", background=surface, foreground=fg, padding=8)
        s.map("TButton", background=[("active", "#1c211c")])
        s.configure(
            "Accent.TButton",
            background=accent,
            foreground="#0c0e0c",
            padding=10,
            font=("TkDefaultFont", 12, "bold"),
        )
        s.map("Accent.TButton", background=[("active", "#eceee9")])
        s.configure("TEntry", fieldbackground=surface, foreground=fg, insertcolor=fg)
        s.configure("Horizontal.TProgressbar", troughcolor=surface, background=accent)

    def _menu(self) -> None:
        if sys.platform != "darwin":
            return
        menubar = tk.Menu(self)
        apple = tk.Menu(menubar, name="apple")
        menubar.add_cascade(menu=apple)
        apple.add_command(label=f"About {APP_NAME}", command=self.about)
        self.config(menu=menubar)
        try:
            self.createcommand("tkAboutDialog", self.about)
        except tk.TclError:
            pass

    def about(self) -> None:
        messagebox.showinfo(
            APP_NAME,
            "Merges OSM / GMapTool .img files into one gmapsupp.img\n"
            "for older Garmin nüvi units (FAT32, under 4 GB).\n\n"
            "https://github.com/wilsonsamiano/garmin-map-combiner",
        )

    def _build(self) -> None:
        pad = {"padx": 20, "pady": 6}
        ttk.Label(self, text=APP_NAME, style="Title.TLabel").pack(anchor="w", padx=20, pady=(20, 4))
        ttk.Label(
            self,
            text="Merge OSM / GMapTool .img files into one gmapsupp.img for a nüvi SD card (FAT32, under 4 GB).",
            style="Muted.TLabel",
            wraplength=720,
        ).pack(anchor="w", **pad)

        row = ttk.Frame(self)
        row.pack(fill="x", padx=20, pady=8)
        ttk.Button(row, text="Add .img files", command=self.add_files).pack(side="left")
        ttk.Button(row, text="Clear list", command=self.clear_files).pack(side="left", padx=8)

        self.listbox = tk.Listbox(
            self,
            height=7,
            bg="#141714",
            fg="#eceee9",
            highlightthickness=1,
            highlightbackground="#2a332c",
            selectbackground="#2a332c",
            relief="flat",
            font=("TkDefaultFont", 12),
        )
        self.listbox.pack(fill="x", padx=20, pady=4)

        grid = ttk.Frame(self)
        grid.pack(fill="x", padx=20, pady=8)
        ttk.Label(grid, text="mkgmap.jar").grid(row=0, column=0, sticky="w")
        self.mkgmap = tk.StringVar(value=which_mkgmap() or "")
        ttk.Entry(grid, textvariable=self.mkgmap).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(grid, text="Browse", command=self.pick_jar).grid(row=0, column=2)
        ttk.Label(grid, text="Output folder").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.outdir = tk.StringVar(value=str(DEFAULT_OUT))
        ttk.Entry(grid, textvariable=self.outdir).grid(row=1, column=1, sticky="ew", padx=8, pady=(8, 0))
        ttk.Button(grid, text="Browse", command=self.pick_out).grid(row=1, column=2, pady=(8, 0))
        grid.columnconfigure(1, weight=1)

        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=20, pady=8)
        self.go = ttk.Button(btns, text="Combine maps", style="Accent.TButton", command=self.start)
        self.go.pack(side="left")
        ttk.Button(btns, text="Open output folder", command=self.open_out).pack(side="left", padx=8)

        java_txt = self.java or "not found — install with: brew install openjdk"
        self.status = tk.StringVar(value=f"Java: {java_txt}")
        ttk.Label(self, textvariable=self.status, style="Muted.TLabel").pack(anchor="w", padx=20)

        self.log = tk.Text(
            self,
            height=12,
            wrap="word",
            bg="#141714",
            fg="#9aa196",
            insertbackground="#eceee9",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2a332c",
            font=("Menlo", 11),
        )
        self.log.pack(fill="both", expand=True, padx=20, pady=(6, 20))

    def add_files(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Select .img map files",
            initialdir=str(HOME / "Downloads"),
            filetypes=[("Garmin IMG", "*.img"), ("All files", "*.*")],
        )
        for p in paths:
            if p not in self.files:
                self.files.append(p)
                self.listbox.insert("end", os.path.basename(p))

    def clear_files(self) -> None:
        self.files.clear()
        self.listbox.delete(0, "end")

    def pick_jar(self) -> None:
        p = filedialog.askopenfilename(
            title="Select mkgmap.jar",
            filetypes=[("Java JAR", "*.jar")],
        )
        if p:
            self.mkgmap.set(p)

    def pick_out(self) -> None:
        p = filedialog.askdirectory(title="Output folder")
        if p:
            self.outdir.set(p)

    def open_out(self) -> None:
        out = Path(self.outdir.get())
        out.mkdir(parents=True, exist_ok=True)
        if sys.platform == "darwin":
            subprocess.run(["open", str(out)], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", str(out)], check=False)
        else:
            os.startfile(str(out))  # type: ignore[attr-defined]

    def write(self, text: str) -> None:
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.update_idletasks()

    def start(self) -> None:
        if not self.java:
            messagebox.showerror(
                "Java missing",
                "Install Java first:\n\nbrew install openjdk\n\nThen quit and reopen this app.",
            )
            return
        if not self.files:
            messagebox.showwarning("No maps", "Add at least one .img file.")
            return
        jar = self.mkgmap.get().strip()
        if not jar or not Path(jar).is_file():
            messagebox.showerror(
                "mkgmap missing",
                "Download mkgmap from https://www.mkgmap.org.uk/download/mkgmap.html\n"
                "Unzip it, then Browse to mkgmap.jar.",
            )
            return
        self.go.config(state="disabled")
        self.log.delete("1.0", "end")
        threading.Thread(target=self.run_merge, daemon=True).start()

    def run_merge(self) -> None:
        out = Path(self.outdir.get())
        out.mkdir(parents=True, exist_ok=True)
        dest = out / "gmapsupp.img"
        if dest.exists():
            dest.unlink()
        cmd = [self.java, "-Xmx4g", "-jar", self.mkgmap.get(), "--gmapsupp", *self.files]
        self.after(0, lambda: self.write("Running:\n" + " ".join(cmd) + "\n"))
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(out),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            assert proc.stdout
            for line in proc.stdout:
                self.after(0, lambda l=line.rstrip(): self.write(l))
            rc = proc.wait()
        except Exception as exc:
            self.after(0, lambda: messagebox.showerror("Error", str(exc)))
            self.after(0, lambda: self.go.config(state="normal"))
            return

        if rc != 0 or not dest.is_file():
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Failed",
                    "gmapsupp.img was not created. Scroll the log for mkgmap errors.",
                ),
            )
            self.after(0, lambda: self.go.config(state="normal"))
            return

        size = dest.stat().st_size
        gb = size / (1024**3)
        if size >= MAX_BYTES:
            msg = (
                f"Created gmapsupp.img ({gb:.2f} GB) — over the 4 GB FAT32 limit.\n\n"
                "Remove a region and combine again."
            )
            self.after(0, lambda: messagebox.showwarning("Too large", msg))
        else:
            msg = (
                f"Created gmapsupp.img ({gb:.2f} GB)\n\n"
                f"{dest}\n\n"
                "Copy this file to the SD card as:\nGarmin/gmapsupp.img"
            )
            self.after(0, lambda: messagebox.showinfo("Done", msg))
        self.after(0, lambda: self.status.set(f"Done — {gb:.2f} GB"))
        self.after(0, lambda: self.go.config(state="normal"))
        self.after(0, self.open_out)


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
