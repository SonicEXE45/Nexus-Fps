from __future__ import annotations

import threading
import urllib.error
import urllib.request
import webbrowser
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

ROOT = Path(__file__).resolve().parent
PUBLIC_URL = "https://nexusfps.io"
HEALTH_URL = f"{PUBLIC_URL}/api/health"
BG = "#080811"
CARD = "#11101e"
PURPLE = "#963cff"
CYAN = "#52dfff"


class NexusLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("NEXUS FPS | Website Launcher")
        self.root.geometry("610x390")
        self.root.minsize(570, 360)
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._build_ui()
        self.check_public_site(auto_open=True)

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=BG, padx=28, pady=24)
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg=BG)
        header.pack(fill="x")

        logo = tk.PhotoImage(file=str(ROOT / "site" / "assets" / "nexus.png"))
        shrink = max(1, logo.width() // 72)
        self.logo_image = logo.subsample(shrink, shrink) if shrink > 1 else logo
        tk.Label(header, image=self.logo_image, bg=BG).pack(side="left", padx=(0, 14))

        brand = tk.Frame(header, bg=BG)
        brand.pack(side="left", fill="y", pady=5)
        tk.Label(brand, text="NEXUS FPS", fg="#f7f7ff", bg=BG,
                 font=("Segoe UI", 21, "bold")).pack(anchor="w")
        tk.Label(brand, text="PUBLIC WEBSITE LAUNCHER", fg="#8888a8", bg=BG,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(2, 0))

        tk.Frame(outer, bg="#242039", height=1).pack(fill="x", pady=22)

        card = tk.Frame(outer, bg=CARD, highlightbackground="#29213d",
                        highlightthickness=1, padx=18, pady=16)
        card.pack(fill="x")

        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x")
        self.dot = tk.Label(top, text="●", fg="#f0ae42", bg=CARD,
                            font=("Segoe UI", 13))
        self.dot.pack(side="left")
        self.status = tk.Label(top, text="NEXUS FPS kontrol ediliyor...", fg="#f5f3ff",
                                bg=CARD, font=("Segoe UI", 11, "bold"))
        self.status.pack(side="left", padx=(8, 0))
        self.detail = tk.Label(card, text="Yayın adresi kontrol ediliyor.", fg="#9693ad",
                               bg=CARD, font=("Segoe UI", 9), justify="left", wraplength=500)
        self.detail.pack(anchor="w", pady=(8, 0))

        tk.Label(outer, text="PUBLIC WEBSITE ADDRESS", fg="#85829c", bg=BG,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(20, 7))
        address = tk.Frame(outer, bg=CARD, highlightbackground="#29213d",
                           highlightthickness=1, padx=13, pady=11)
        address.pack(fill="x")
        tk.Label(address, text=PUBLIC_URL, fg=CYAN, bg=CARD,
                 font=("Consolas", 12, "bold")).pack(side="left")
        tk.Button(address, text="KOPYALA", command=self.copy_address,
                  bg="#211735", fg="#d9c6ff", activebackground="#30204d",
                  activeforeground="#ffffff", relief="flat", bd=0,
                  font=("Segoe UI", 8, "bold"), padx=12, pady=6,
                  cursor="hand2").pack(side="right")

        buttons = tk.Frame(outer, bg=BG)
        buttons.pack(fill="x", pady=(18, 0))
        tk.Button(buttons, text="  SİTEYİ AÇ  ↗", command=self.open_site,
                  bg=PURPLE, fg="white", activebackground="#a54cff",
                  activeforeground="white", relief="flat", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=18, pady=12,
                  cursor="hand2").pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(buttons, text="YENİDEN KONTROL ET", command=self.check_public_site,
                  bg="#1b1929", fg="#d8d5e8", activebackground="#302b42",
                  activeforeground="white", relief="flat", bd=0,
                  font=("Segoe UI", 9, "bold"), padx=14, pady=12,
                  cursor="hand2").pack(side="left", padx=(6, 0))

        tk.Label(outer,
                 text="Bu pencere herkese açık siteyi kontrol eder ve açar. Site hosting üzerinde çalışır;\nPython penceresinin sürekli açık kalması gerekmez.",
                 fg="#77748d", bg=BG, justify="left", font=("Segoe UI", 8)).pack(anchor="w", pady=(17, 0))

    def check_public_site(self, auto_open: bool = False) -> None:
        self.dot.config(fg="#f0ae42")
        self.status.config(text="NEXUS FPS kontrol ediliyor...")
        self.detail.config(text="https://nexusfps.io adresine erişim deneniyor.")

        def worker() -> None:
            request = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "NEXUS-FPS-Launcher/1.0"})
            try:
                with urllib.request.urlopen(request, timeout=8) as response:
                    ok = response.status == 200
                if ok:
                    self.root.after(0, lambda: self._set_online(auto_open))
                else:
                    self.root.after(0, self._set_offline)
            except (OSError, urllib.error.URLError, TimeoutError):
                self.root.after(0, self._set_offline)

        threading.Thread(target=worker, daemon=True).start()

    def _set_online(self, auto_open: bool) -> None:
        self.dot.config(fg="#43e6a1")
        self.status.config(text="NEXUS FPS yayında")
        self.detail.config(text="Public siteye erişim başarılı. Adres herkese açık şekilde çalışıyor.")
        if auto_open:
            self.open_site()

    def _set_offline(self) -> None:
        self.dot.config(fg="#f0ae42")
        self.status.config(text="Public yayın henüz erişilebilir değil")
        self.detail.config(text=("Alan adı DNS kaydı veya hosting yayını henüz tamamlanmamış olabilir. "
                                 "Yayın tamamlandığında bu pencere siteyi açacaktır."))

    def open_site(self) -> None:
        webbrowser.open(PUBLIC_URL, new=2)

    def copy_address(self) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(PUBLIC_URL)
        messagebox.showinfo("NEXUS FPS", "https://nexusfps.io kopyalandı.")


def main() -> None:
    root = tk.Tk()
    NexusLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
