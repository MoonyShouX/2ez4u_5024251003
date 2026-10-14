import tkinter as tk
from tkinter import ttk
import time


class Aplikasi2EZ4U:
    def __init__(self, root, backend_array, backend_linkedlist):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1000x700")

        self.rak_pesanan = backend_array
        self.kereta_pesanan = backend_linkedlist

        # --- FONT STYLE ---
        font_header = ("Arial", 10, "bold")
        font_normal = ("Arial", 10)

        # --- FRAME UTAMA ---
        # Pembungkus besar
        frame_main = tk.Frame(root, padx=5, pady=5)
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Frame Kiri (Menu)
        self.frame_kiri = tk.Frame(frame_main, width=280)
        self.frame_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

        # Frame Kanan (Isi Konten + Command)
        self.frame_kanan = tk.Frame(frame_main)
        self.frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Kanan Atas (Konten)
        self.frame_konten = tk.Frame(self.frame_kanan, bd=1, relief=tk.SOLID, bg="white")
        self.frame_konten.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))

        # Kanan Bawah (Command/Log)
        self.frame_cmd = tk.Frame(self.frame_kanan, height=120)
        self.frame_cmd.pack(side=tk.BOTTOM, fill=tk.X)

        self.setup_menu_kiri(font_header, font_normal)
        self.setup_panel_command(font_header)

        # Inisialisasi awal layar kosong
        self.tampilkan_layar_kosong()

    def setup_menu_kiri(self, font_header, font_normal):
        # Kategori: DATA
        tk.Label(self.frame_kiri, text="DATA", font=font_header, anchor="w", fg="#333").pack(fill=tk.X, pady=(0, 2))
        tk.Button(self.frame_kiri, text="Load", anchor="w", font=font_normal, command=self.dummy_load).pack(fill=tk.X,
                                                                                                            pady=(0,
                                                                                                                  10))

        # Kategori: M1 - DATA PESANAN
        tk.Label(self.frame_kiri, text="M1 - DATA PESANAN", font=font_header, anchor="w", fg="#333").pack(fill=tk.X,
                                                                                                          pady=(0, 2))

        menu_m1 = [
            "ARRAY - LIHAT PESANAN",
            "ARRAY - TAMBAH PESANAN REGULER",
            "ARRAY - TAMBAH PESANAN PRIORITAS",
            "ARRAY - TAMBAH PESANAN VIP",
            "ARRAY - HAPUS PESANAN",
            "LINKEDLIST - LIHAT PESANAN",
            "LINKEDLIST - TAMBAH PESANAN REGULER",
            "LINKEDLIST - TAMBAH PESANAN PRIORITA",  # Sengaja typo sesuai gambar
            "LINKEDLIST - TAMBAH PESANAN VIP",
            "LINKEDLIST - HAPUS PESANAN"
        ]
        for m in menu_m1:
            btn = tk.Button(self.frame_kiri, text=m, anchor="w", font=font_normal)
            # Pasang event click ke fungsi ubah form
            btn.config(command=lambda teks=m: self.ubah_layar_kanan(teks))
            btn.pack(fill=tk.X)

        # Kategori: M2 - ANTREAN DAN UNDO
        tk.Label(self.frame_kiri, text="M2 - ANTREAN DAN UNDO", font=font_header, anchor="w", fg="#333").pack(fill=tk.X,
                                                                                                              pady=(10,
                                                                                                                    2))
        for m in ["Isi antrean FIFO", "Layani berikutnya", "Undo"]:
            tk.Button(self.frame_kiri, text=m, anchor="w", font=font_normal, state=tk.DISABLED).pack(fill=tk.X)

        # Kategori: M3 DAN M4... dst (Sesuai gambar)
        tk.Label(self.frame_kiri, text="M3 DAN M4 - LAPORAN...", font=font_header, anchor="w", fg="#333").pack(
            fill=tk.X, pady=(10, 2))
        for m in ["Laporan harian", "Cari di laporan", "Bangun indeks hash", "Cari pesanan (oid)"]:
            tk.Button(self.frame_kiri, text=m, anchor="w", font=font_normal, state=tk.DISABLED).pack(fill=tk.X)

    def setup_panel_command(self, font_header):
        tk.Label(self.frame_cmd, text="COMMAND", font=font_header, anchor="w", fg="#333").pack(fill=tk.X)
        self.text_cmd = tk.Text(self.frame_cmd, height=5, font=("Courier", 10), bd=1, relief=tk.SOLID)
        self.text_cmd.pack(fill=tk.BOTH, expand=True)
        # Nonaktifkan edit teks
        self.text_cmd.config(state=tk.DISABLED)

    def log_cmd(self, command_name, method_name, waktu_ms):
        self.text_cmd.config(state=tk.NORMAL)
        # Format sesuai gambar: command_name -> method_name waktu_ms
        log_text = f"{command_name:<15} -> {method_name:<15} {waktu_ms:.2f} ms\n"
        self.text_cmd.insert(tk.END, log_text)
        self.text_cmd.see(tk.END)
        self.text_cmd.config(state=tk.DISABLED)

    def dummy_load(self):
        self.log_cmd("load", "M1 - array", 261.06)

    def bersihkan_kanan(self):
        for widget in self.frame_konten.winfo_children():
            widget.destroy()

    def tampilkan_layar_kosong(self):
        self.bersihkan_kanan()
        tk.Label(self.frame_konten, text="Silakan pilih menu di samping.", bg="white", font=("Arial", 12)).pack(pady=20)

    def ubah_layar_kanan(self, judul_menu):
        self.bersihkan_kanan()

        # Header Judul
        frame_header = tk.Frame(self.frame_konten, bg="white")
        frame_header.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Judul sesuai tombol yang diklik
        if "TAMBAH PESANAN REGULER" in judul_menu:
            if "ARRAY" in judul_menu:
                teks_judul = "Array: pesanan REGULER, masuk paling belakang"
                teks_desc = "append: pesanan biasa mengantre di barisan paling belakang."
                tipe_strukdat = "Array"
            else:
                teks_judul = "LinkedList: pesanan REGULER, masuk paling belakang"
                teks_desc = "tambah_belakang: pesanan biasa mengantre di barisan paling belakang."
                tipe_strukdat = "LinkedList"

            tk.Label(frame_header, text=teks_judul, font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill=tk.X)
            tk.Label(frame_header, text=teks_desc, font=("Arial", 9), bg="white", fg="#555", anchor="w").pack(fill=tk.X)

            # Form Input
            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=10, pady=10)

            tk.Label(frame_input, text="Nama pelanggan", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0,
                                                                                                     sticky="w")

            entry_nama = tk.Entry(frame_input, width=30)
            entry_nama.insert(0, "Pelanggan Baru")
            entry_nama.grid(row=1, column=0, sticky="w", pady=(0, 2))

            tk.Label(frame_input, text="nama untuk pesanan yang akan dibuat", bg="white", fg="#777",
                     font=("Arial", 8)).grid(row=2, column=0, sticky="w")

            # Area Hasil (Listbox besar di tengah)
            self.listbox_hasil = tk.Listbox(self.frame_konten, font=("Arial", 10))
            self.listbox_hasil.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

            def proses_tambah():
                nama = entry_nama.get()
                if not nama: return

                mulai = time.perf_counter()

                if tipe_strukdat == "Array":
                    self.rak_pesanan.tambah_reguler([nama])
                    # Tampilkan array get dummy
                    self.log_cmd("array_get", "M1 - array", 0.05)
                else:
                    self.kereta_pesanan.tambah_reguler([nama])
                    self.log_cmd("list_get", "M1 - linked", 0.05)

                selesai = time.perf_counter()
                durasi = (selesai - mulai) * 1000

                # Log Tambah
                self.log_cmd("insert", f"M1 - {tipe_strukdat.lower()}", durasi)

                # Update Listbox (dummy update)
                self.listbox_hasil.insert(tk.END, f"-> Ditambahkan: {nama}")

            # Tombol Tambah yang warnanya biru dongker kayak di gambar
            btn_tambah = tk.Button(frame_input, text="TAMBAH", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                                   width=15, command=proses_tambah)
            btn_tambah.grid(row=1, column=1, padx=20)

        else:
            # Tampilan default untuk menu lain yang belum dibikin spesifik formnya
            tk.Label(frame_header, text=judul_menu, font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill=tk.X)
            self.listbox_hasil = tk.Listbox(self.frame_konten, font=("Arial", 10))
            self.listbox_hasil.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.listbox_hasil.insert(tk.END, "(Form untuk menu ini belum diimplementasikan, silakan sesuaikan)")