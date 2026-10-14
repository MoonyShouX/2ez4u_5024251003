import tkinter as tk
from tkinter import ttk
import time

import os
import csv

from backend.m1_pesanan import Array
from backend.m1_linked_list import LinkedList
from backend.m2_antrean import (
    Stack,
    AntreanNaif,
    AntreanMelingkar,
    ke_postfix,
    hitung,
    prioritas_operator
)
from backend.m3_laporan import (
    insertion_sort,
    merge_sort,
    linear_search,
    binary_search,
    _ambil_nilai
)




class Aplikasi2EZ4U:
    def __init__(self, root, backend_array, backend_linkedlist, data_antrean=None, semua_pesanan=None):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1100x750")

        self.rak_pesanan = backend_array
        self.kereta_pesanan = backend_linkedlist
        self.semua_pesanan = semua_pesanan if semua_pesanan is not None else []

        # Data terurut untuk binary search (dibuat on-demand dengan merge sort)
        self.pesanan_terurut_oid = None
        self.waktu_buat_indeks_oid = 0.0

        # Nomor oid berjalan untuk pesanan baru
        self.counter_oid = 200001

        # Inisialisasi Antrean M2
        self.antrean_naif = AntreanNaif()
        self.antrean_circular = AntreanMelingkar(kapasitas=32768)

        # Muat data antrean berstatus ANTRE
        if data_antrean:
            for item in data_antrean:
                self.antrean_naif.enqueue(item)
                self.antrean_circular.enqueue(item)

        # Tumpukan undo & redo M2
        self.stack_undo = Stack()
        self.stack_redo = Stack()

        # Font Style
        font_header = ("Arial", 10, "bold")
        font_normal = ("Arial", 10)

        # Frame Utama
        frame_main = tk.Frame(root, padx=5, pady=5)
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Frame Kiri (Menu Navigasi dengan Scrollbar)
        frame_kiri_canvas = tk.Frame(frame_main, width=300)
        frame_kiri_canvas.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

        canvas = tk.Canvas(frame_kiri_canvas, width=285, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_kiri_canvas, orient="vertical", command=canvas.yview)
        self.frame_kiri = tk.Frame(canvas)

        self.frame_kiri.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.frame_kiri, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame Kanan
        self.frame_kanan = tk.Frame(frame_main)
        self.frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Kanan Atas (Konten Form dan Hasil)
        self.frame_konten = tk.Frame(self.frame_kanan, bd=1, relief=tk.SOLID, bg="white")
        self.frame_konten.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))

        # Kanan Bawah (Panel Command)
        self.frame_cmd = tk.Frame(self.frame_kanan, height=130)
        self.frame_cmd.pack(side=tk.BOTTOM, fill=tk.X)

        self.setup_menu_kiri(font_header, font_normal)
        self.setup_panel_command(font_header)

        # Status bar pojok kiri bawah
        self.label_status = tk.Label(self.frame_cmd, text="[Ready]", font=("Arial", 9, "bold"),
                                     bg="#2c4260", fg="white", padx=8, pady=2)
        self.label_status.pack(side=tk.LEFT, pady=(3, 0))

        self.tampilkan_layar_kosong()

    def setup_menu_kiri(self, font_header, font_normal):
        # Kategori: DATA
        tk.Label(self.frame_kiri, text="DATA", font=font_header, anchor="w", fg="#333").pack(fill=tk.X, pady=(0, 2))
        btn_load = tk.Button(self.frame_kiri, text="Load", anchor="w", font=font_normal,
                             command=self.muat_ulang_data)
        btn_load.pack(fill=tk.X, pady=(0, 10))

        # Kategori: M1 - DATA PESANAN
        tk.Label(self.frame_kiri, text="M1 - DATA PESANAN", font=font_header, anchor="w", fg="#333").pack(fill=tk.X, pady=(0, 2))
        menu_m1 = [
            "ARRAY - LIHAT PESANAN",
            "ARRAY - TAMBAH PESANAN REGULER",
            "ARRAY - TAMBAH PESANAN PRIORITAS",
            "ARRAY - TAMBAH PESANAN VIP",
            "ARRAY - HAPUS PESANAN",
            "LINKEDLIST - LIHAT PESANAN",
            "LINKEDLIST - TAMBAH PESANAN REGULER",
            "LINKEDLIST - TAMBAH PESANAN PRIORITAS",
            "LINKEDLIST - TAMBAH PESANAN VIP",
            "LINKEDLIST - HAPUS PESANAN"
        ]
        for m in menu_m1:
            btn = tk.Button(self.frame_kiri, text=m, anchor="w", font=font_normal)
            btn.config(command=lambda teks=m: self.ubah_layar_kanan(teks))
            btn.pack(fill=tk.X)

        # Kategori: M2 - STACK DAN QUEUE
        tk.Label(self.frame_kiri, text="M2 - STACK DAN QUEUE", font=font_header, anchor="w", fg="#333").pack(fill=tk.X, pady=(10, 2))
        menu_m2 = [
            "STACK - POSTFIX (MESIN KASIR)",
            "STACK - UNDO",
            "STACK - REDO",
            "QUEUE - ENQUEUE",
            "QUEUE - DEQUEUE NAIF",
            "QUEUE - DEQUEUE CIRCULAR"
        ]
        for m in menu_m2:
            btn = tk.Button(self.frame_kiri, text=m, anchor="w", font=font_normal)
            btn.config(command=lambda teks=m: self.ubah_layar_kanan(teks))
            btn.pack(fill=tk.X)

        # Kategori: M3 - SORT DAN SEARCH
        tk.Label(self.frame_kiri, text="M3 - SORT DAN SEARCH", font=font_header, anchor="w", fg="#333").pack(fill=tk.X, pady=(10, 2))
        menu_m3 = [
            "SORT - INSERTION SORT",
            "SORT - MERGE SORT",
            "SEARCH - LINEAR SEARCH",
            "SEARCH - BINARY SEARCH"
        ]
        for m in menu_m3:
            btn = tk.Button(self.frame_kiri, text=m, anchor="w", font=font_normal)
            btn.config(command=lambda teks=m: self.ubah_layar_kanan(teks))
            btn.pack(fill=tk.X)

    def setup_panel_command(self, font_header):
        tk.Label(self.frame_cmd, text="COMMAND", font=font_header, anchor="w", fg="#333").pack(fill=tk.X)
        self.text_cmd = tk.Text(self.frame_cmd, height=5, font=("Courier", 9), bd=1, relief=tk.SOLID)
        self.text_cmd.pack(fill=tk.BOTH, expand=True)
        self.text_cmd.config(state=tk.DISABLED)

    def log_cmd(self, command_name, method_name, waktu_ms):
        self.text_cmd.config(state=tk.NORMAL)
        log_text = f"{command_name:<24} -> {method_name:<22} {waktu_ms:.2f} ms\n"
        self.text_cmd.insert(tk.END, log_text)
        self.text_cmd.see(tk.END)
        self.text_cmd.config(state=tk.DISABLED)

        # Update status badge
        self.label_status.config(text=f"[{method_name}] {waktu_ms:.2f} ms")

    def muat_ulang_data(self):
        # Jalur file CSV dari folder data/
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_csv = os.path.join(base_dir, "data", "pesanan.csv")
        if not os.path.exists(path_csv):
            path_csv = "data/pesanan.csv"

        t0 = time.perf_counter()
        baru_rak = Array()
        baru_kereta = LinkedList()
        baru_semua = []
        baru_naif = AntreanNaif()
        baru_circular = AntreanMelingkar(kapasitas=32768)

        try:
            with open(path_csv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # lewati header
                for baris in reader:
                    baru_semua.append(baris)
                    baru_rak.tambah_reguler(baris)
                    baru_kereta.tambah_reguler(baris)
                    if len(baris) >= 9 and baris[8] == 'ANTRE':
                        baru_naif.enqueue(baris)
                        baru_circular.enqueue(baris)

            self.rak_pesanan = baru_rak
            self.kereta_pesanan = baru_kereta
            self.semua_pesanan = baru_semua
            self.antrean_naif = baru_naif
            self.antrean_circular = baru_circular
            self.pesanan_terurut_oid = None

            durasi = (time.perf_counter() - t0) * 1000
            self.log_cmd("load", "M1 - array", durasi)

            self.bersihkan_kanan()
            tk.Label(self.frame_konten, text=f"Data berhasil dimuat dari folder data/ ({len(self.semua_pesanan):,} baris).\nDurasi pemuatan: {durasi:.2f} ms",
                     bg="white", font=("Arial", 11), fg="#2c4260").pack(pady=40)
        except Exception as e:
            durasi = (time.perf_counter() - t0) * 1000
            self.log_cmd("load", "M1 - array", durasi)
            self.bersihkan_kanan()
            tk.Label(self.frame_konten, text=f"Gagal memuat data dari {path_csv}:\n{e}",
                     bg="white", font=("Arial", 11), fg="red").pack(pady=40)


    def bersihkan_kanan(self):
        for widget in self.frame_konten.winfo_children():
            widget.destroy()

    def tampilkan_layar_kosong(self):
        self.bersihkan_kanan()
        tk.Label(self.frame_konten, text="Silakan pilih menu di samping.", bg="white", font=("Arial", 12)).pack(pady=40)

    def buat_header(self, judul, deskripsi):
        frame_header = tk.Frame(self.frame_konten, bg="white")
        frame_header.pack(fill=tk.X, padx=15, pady=(10, 5))
        tk.Label(frame_header, text=judul, font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill=tk.X)
        if deskripsi:
            tk.Label(frame_header, text=deskripsi, font=("Arial", 9), bg="white", fg="#555", anchor="w").pack(fill=tk.X)
        return frame_header

    def buat_tabel(self, kolom, data_baris=None):
        frame_tabel = tk.Frame(self.frame_konten, bg="white")
        frame_tabel.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

        tree = ttk.Treeview(frame_tabel, columns=kolom, show="headings", height=10)
        vsb = ttk.Scrollbar(frame_tabel, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame_tabel, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in kolom:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame_tabel.grid_rowconfigure(0, weight=1)
        frame_tabel.grid_columnconfigure(0, weight=1)

        if data_baris:
            for baris in data_baris:
                tree.insert("", tk.END, values=baris)

        return tree

    # ==========================================================
    # LOGIKA SETIAP MENU
    # ==========================================================
    def ubah_layar_kanan(self, judul_menu):
        self.bersihkan_kanan()

        # ------------------------------------------------------
        # M1: LIHAT PESANAN (Array / LinkedList)
        # ------------------------------------------------------
        if "LIHAT PESANAN" in judul_menu:
            is_array = "ARRAY" in judul_menu
            nama_strukdat = "Array" if is_array else "LinkedList"
            method_log = "M1 - array" if is_array else "M1 - linked"
            cmd_log = "array_get" if is_array else "list_get"

            self.buat_header(f"{nama_strukdat}: Lihat Pesanan",
                             "Melihat detail satu pesanan berdasarkan indeks posisi.")

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Indeks pesanan", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_idx = tk.Entry(frame_input, width=15)
            entry_idx.insert(0, "0")
            entry_idx.grid(row=1, column=0, sticky="w", pady=(2, 0))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("kolom", "isi")
            tree = self.buat_tabel(kolom)

            def proses_lihat():
                for item in tree.get_children():
                    tree.delete(item)
                try:
                    idx = int(entry_idx.get().strip())
                except ValueError:
                    label_info.config(text="Indeks harus berupa angka!")
                    return

                t0 = time.perf_counter()
                if is_array:
                    item = self.rak_pesanan.get(idx)
                else:
                    item = self.kereta_pesanan.get(idx)
                durasi = (time.perf_counter() - t0) * 1000

                self.log_cmd(cmd_log, method_log, durasi)

                if item is None:
                    label_info.config(text=f"Pesanan pada indeks {idx} tidak ditemukan!")
                else:
                    label_info.config(text=f"Detail pesanan pada indeks {idx} (ditemukan dalam {durasi:.3f} ms):")
                    field_names = ("oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status")
                    for k, v in zip(field_names, item):
                        tree.insert("", tk.END, values=(k, v))

            btn = tk.Button(frame_input, text="LIHAT", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=12, command=proses_lihat)
            btn.grid(row=1, column=1, padx=15)

            proses_lihat()

        # ------------------------------------------------------
        # M1: TAMBAH PESANAN (Reguler / Prioritas / VIP)
        # ------------------------------------------------------
        elif "TAMBAH PESANAN" in judul_menu:
            is_array = "ARRAY" in judul_menu
            nama_strukdat = "Array" if is_array else "LinkedList"
            tipe = "REGULER" if "REGULER" in judul_menu else ("PRIORITAS" if "PRIORITAS" in judul_menu else "VIP")

            if tipe == "REGULER":
                desc = "append: pesanan biasa mengantre di barisan paling belakang."
            elif tipe == "PRIORITAS":
                desc = "insert tengah: pesanan prioritas menyerobot ke tengah barisan."
            else:
                desc = "insert depan: pesanan VIP langsung ke urutan nomor 1."

            self.buat_header(f"{nama_strukdat}: pesanan {tipe}, masuk {'belakang' if tipe=='REGULER' else ('tengah' if tipe=='PRIORITAS' else 'paling depan')}",
                             desc)

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Nama pelanggan", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_nama = tk.Entry(frame_input, width=30)
            entry_nama.insert(0, f"Pelanggan {tipe.capitalize()}")
            entry_nama.grid(row=1, column=0, sticky="w", pady=(2, 2))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("kolom", "isi")
            tree = self.buat_tabel(kolom)

            def proses_tambah():
                nama = entry_nama.get().strip()
                if not nama:
                    return

                new_oid = f"O-{self.counter_oid}"
                self.counter_oid += 1
                prioritas_val = "1" if tipe == "VIP" else ("2" if tipe == "PRIORITAS" else "3")
                pesanan_baru = [new_oid, nama, "kafe-teknik", "roti-bakar", "15000", prioritas_val, "00:00:00", "", "ANTRE"]

                method_log = "M1 - array" if is_array else "M1 - linked"
                t0 = time.perf_counter()
                if is_array:
                    if tipe == "REGULER":
                        self.rak_pesanan.tambah_reguler(pesanan_baru)
                    elif tipe == "PRIORITAS":
                        self.rak_pesanan.tambah_prioritas(pesanan_baru)
                    else:
                        self.rak_pesanan.tambah_vip(pesanan_baru)
                    panjang = len(self.rak_pesanan)
                else:
                    if tipe == "REGULER":
                        self.kereta_pesanan.tambah_reguler(pesanan_baru)
                    elif tipe == "PRIORITAS":
                        self.kereta_pesanan.tambah_prioritas(pesanan_baru)
                    else:
                        self.kereta_pesanan.tambah_vip(pesanan_baru)
                    panjang = len(self.kereta_pesanan)

                durasi = (time.perf_counter() - t0) * 1000
                self.log_cmd("insert", method_log, durasi)

                for item in tree.get_children():
                    tree.delete(item)

                label_info.config(text=f"Pesanan {new_oid} berhasil ditambahkan! Total elemen {nama_strukdat} sekarang: {panjang}")
                field_names = ("oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status")
                for k, v in zip(field_names, pesanan_baru):
                    tree.insert("", tk.END, values=(k, v))

            btn = tk.Button(frame_input, text="TAMBAH", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=15, command=proses_tambah)
            btn.grid(row=1, column=1, padx=20)

        # ------------------------------------------------------
        # M1: HAPUS PESANAN (Array / LinkedList)
        # ------------------------------------------------------
        elif "HAPUS PESANAN" in judul_menu:
            is_array = "ARRAY" in judul_menu
            nama_strukdat = "Array" if is_array else "LinkedList"
            method_log = "M1 - array" if is_array else "M1 - linked"

            self.buat_header(f"{nama_strukdat}: Hapus Pesanan",
                             "Menghapus pesanan dari barisan berdasarkan indeks posisi.")

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Indeks yang akan dihapus", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_idx = tk.Entry(frame_input, width=15)
            entry_idx.insert(0, "0")
            entry_idx.grid(row=1, column=0, sticky="w", pady=(2, 0))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            def proses_hapus():
                try:
                    idx = int(entry_idx.get().strip())
                except ValueError:
                    label_info.config(text="Indeks harus berupa angka!")
                    return

                t0 = time.perf_counter()
                if is_array:
                    item = self.rak_pesanan.hapus_pesanan(idx)
                    sisa = len(self.rak_pesanan)
                else:
                    item = self.kereta_pesanan.hapus_pesanan(idx)
                    sisa = len(self.kereta_pesanan)
                durasi = (time.perf_counter() - t0) * 1000

                self.log_cmd("delete", method_log, durasi)

                if item is None:
                    label_info.config(text=f"Gagal: Indeks {idx} tidak valid!")
                else:
                    oid_hapus = item[0] if isinstance(item, (list, tuple)) else str(item)
                    label_info.config(text=f"Pesanan {oid_hapus} berhasil dihapus dari {nama_strukdat}. Sisa elemen: {sisa}")

            btn = tk.Button(frame_input, text="HAPUS", bg="#a93226", fg="white", font=("Arial", 9, "bold"),
                            width=12, command=proses_hapus)
            btn.grid(row=1, column=1, padx=15)

        # ------------------------------------------------------
        # M2: STACK - POSTFIX (MESIN KASIR)
        # ------------------------------------------------------
        elif "POSTFIX" in judul_menu:
            self.buat_header("Stack: hitung struk lewat postfix",
                             "Struk ditulis infix, dihitung dua tahap dengan stack: tahap 1 infix menjadi postfix, tahap 2 postfix dievaluasi.")

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Struk belanja (infix)", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_expr = tk.Entry(frame_input, width=45)
            entry_expr.insert(0, "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
            entry_expr.grid(row=1, column=0, sticky="w", pady=(2, 0))

            label_hasil = tk.Label(self.frame_konten, text="", bg="white", font=("Courier", 10), justify=tk.LEFT, anchor="w")
            label_hasil.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("langkah", "token", "tindakan", "stack", "output")
            tree = self.buat_tabel(kolom)

            def proses_kasir():
                for item in tree.get_children():
                    tree.delete(item)

                ekspresi = entry_expr.get().strip()
                t0 = time.perf_counter()

                # Buat tabel trace konversi dan evaluasi sesuai PDF
                tokens = []
                i = 0
                n = len(ekspresi)
                while i < n:
                    c = ekspresi[i]
                    if c in ' \t':
                        i += 1
                        continue
                    if c in '0123456789':
                        angka = ''
                        while i < n and ekspresi[i] in '0123456789':
                            angka += ekspresi[i]
                            i += 1
                        tokens.append(angka)
                        continue
                    if c in '+-*/()':
                        tokens.append(c)
                        i += 1
                        continue
                    i += 1

                # Tahap 1: Infix ke Postfix
                op_stack = []
                output = []
                step = 1

                for t in tokens:
                    if t.isdigit():
                        output.append(t)
                        tree.insert("", tk.END, values=(f"1.{step}", t, "angka, langsung keluar", " ".join(op_stack), " ".join(output)))
                    elif t == '(':
                        op_stack.append(t)
                        tree.insert("", tk.END, values=(f"1.{step}", t, "push (", " ".join(op_stack), " ".join(output)))
                    elif t == ')':
                        while op_stack and op_stack[-1] != '(':
                            output.append(op_stack.pop())
                        if op_stack and op_stack[-1] == '(':
                            op_stack.pop()
                        tree.insert("", tk.END, values=(f"1.{step}", t, "pop sampai (, buang (", " ".join(op_stack), " ".join(output)))
                    elif t in ['+', '-', '*', '/']:
                        while (op_stack and op_stack[-1] != '(' and
                               prioritas_operator(op_stack[-1]) >= prioritas_operator(t)):
                            output.append(op_stack.pop())
                        op_stack.append(t)
                        tree.insert("", tk.END, values=(f"1.{step}", t, f"push {t}", " ".join(op_stack), " ".join(output)))
                    step += 1

                while op_stack:
                    output.append(op_stack.pop())
                tree.insert("", tk.END, values=("1.akhir", "", "pop sisa stack", "kosong", " ".join(output)))

                postfix_str = " ".join(output)

                # Tahap 2: Evaluasi
                eval_stack = []
                step = 1
                for t in output:
                    if t.isdigit():
                        eval_stack.append(int(t))
                        tree.insert("", tk.END, values=(f"2.{step}", t, f"push {t}", " ".join(str(x) for x in eval_stack), ""))
                    elif t in ['+', '-', '*', '/']:
                        b = eval_stack.pop()
                        a = eval_stack.pop()
                        if t == '+': val = a + b
                        elif t == '-': val = a - b
                        elif t == '*': val = a * b
                        elif t == '/': val = a // b if b != 0 else 0
                        eval_stack.append(val)
                        tree.insert("", tk.END, values=(f"2.{step}", t, f"pop {b} dan {a} -> {a}{t}{b}={val}", " ".join(str(x) for x in eval_stack), ""))
                    step += 1

                total = eval_stack[-1] if eval_stack else 0
                durasi = (time.perf_counter() - t0) * 1000
                self.log_cmd("stack_postfix", "M2 - stack", durasi)

                label_hasil.config(text=f"Struk   : {ekspresi}\nPostfix : {postfix_str}\nTOTAL   : Rp {total:,}")

            btn = tk.Button(frame_input, text="HITUNG", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=12, command=proses_kasir)
            btn.grid(row=1, column=1, padx=15)
            proses_kasir()

        # ------------------------------------------------------
        # M2: QUEUE - ENQUEUE
        # ------------------------------------------------------
        elif "QUEUE - ENQUEUE" in judul_menu:
            self.buat_header("Queue: pesanan baru masuk ke belakang",
                             "Menambah pesanan di ujung belakang kedua antrean sekaligus, yang naif maupun circular.")

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Nama pelanggan", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_nama = tk.Entry(frame_input, width=30)
            entry_nama.insert(0, "Pelanggan Baru")
            entry_nama.grid(row=1, column=0, sticky="w", pady=(2, 0))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("kolom", "isi")
            tree = self.buat_tabel(kolom)

            def proses_enqueue():
                nama = entry_nama.get().strip()
                if not nama: return
                new_oid = f"O-{self.counter_oid}"
                self.counter_oid += 1

                pesanan = [new_oid, nama, "kafe-teknik", "roti-bakar", "12000", "2", "00:00:00", "", "ANTRE"]

                t0 = time.perf_counter()
                self.antrean_naif.enqueue(pesanan)
                self.antrean_circular.enqueue(pesanan)
                durasi = (time.perf_counter() - t0) * 1000

                self.stack_undo.push(('ENQUEUE', [pesanan]))
                while not self.stack_redo.is_empty():
                    self.stack_redo.pop()

                self.log_cmd("queue_enqueue", "M2 - queue", durasi)

                for item in tree.get_children():
                    tree.delete(item)

                label_info.config(text=f"{new_oid} masuk ke barisan paling belakang pada KEDUA antrean.\n"
                                       f"Panjang sekarang: naif {len(self.antrean_naif):,}, circular {len(self.antrean_circular):,}.")
                field_names = ("oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status")
                for k, v in zip(field_names, pesanan):
                    tree.insert("", tk.END, values=(k, v))

            btn = tk.Button(frame_input, text="ENQUEUE", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=15, command=proses_enqueue)
            btn.grid(row=1, column=1, padx=20)

        # ------------------------------------------------------
        # M2: QUEUE - DEQUEUE NAIF & CIRCULAR
        # ------------------------------------------------------
        elif "DEQUEUE" in judul_menu:
            is_circular = "CIRCULAR" in judul_menu
            judul_teks = "Queue circular: ambil dari depan dengan memajukan penunjuk" if is_circular else "Queue naif: ambil dari depan dengan menggeser isi"
            sub_teks = "Hanya front yang maju, kapasitas tetap. O(1)" if is_circular else "Mengambil indeks 0 lalu menggeser seluruh sisa elemen ke kiri. O(n)"
            cmd_log = "queue_dequeue_circular" if is_circular else "queue_dequeue_naive"
            method_log = "M2 - queue circular" if is_circular else "M2 - queue naif"

            self.buat_header(judul_teks, sub_teks)

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Berapa kali dequeue", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_count = tk.Entry(frame_input, width=15)
            entry_count.insert(0, "1")
            entry_count.grid(row=1, column=0, sticky="w", pady=(2, 0))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), justify=tk.LEFT, anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("#", "oid", "pelanggan", "resto", "menu", "masuk")
            tree = self.buat_tabel(kolom)

            def proses_dequeue():
                try:
                    k = int(entry_count.get().strip())
                except ValueError:
                    label_info.config(text="Jumlah harus angka!")
                    return

                for item in tree.get_children():
                    tree.delete(item)

                keluar_list = []
                t0 = time.perf_counter()
                for _ in range(k):
                    if is_circular:
                        item = self.antrean_circular.dequeue()
                    else:
                        item = self.antrean_naif.dequeue()
                    if item is not None:
                        keluar_list.append(item)
                    else:
                        break
                durasi = (time.perf_counter() - t0) * 1000

                self.log_cmd(cmd_log, method_log, durasi)

                if keluar_list:
                    self.stack_undo.push(('DEQUEUE', keluar_list))
                    while not self.stack_redo.is_empty():
                        self.stack_redo.pop()

                if is_circular:
                    label_info.config(text=f"{len(keluar_list)} pesanan keluar dari depan antrean circular.\n"
                                           f"Tidak ada elemen yang digeser, front sekarang {self.antrean_circular.front}, "
                                           f"rear {self.antrean_circular.rear}, kapasitas {self.antrean_circular.kapasitas:,}.\n"
                                           f"Sisa antrean circular: {len(self.antrean_circular):,}.")
                else:
                    tot_geser = self.antrean_naif.total_geseran
                    rata_geser = self.antrean_naif.geseran_terakhir
                    label_info.config(text=f"{len(keluar_list)} pesanan keluar dari depan antrean naif.\n"
                                           f"Total {tot_geser:,} elemen digeser, geseran terakhir {rata_geser:,}. "
                                           f"Sisa antrean naif: {len(self.antrean_naif):,}.")

                for idx, row in enumerate(keluar_list[:50], 1):
                    oid_val = row[0] if len(row) > 0 else "-"
                    pel_val = row[1] if len(row) > 1 else "-"
                    resto_val = row[2] if len(row) > 2 else "-"
                    menu_val = row[3] if len(row) > 3 else "-"
                    masuk_val = row[6] if len(row) > 6 else "-"
                    tree.insert("", tk.END, values=(idx, oid_val, pel_val, resto_val, menu_val, masuk_val))

            btn = tk.Button(frame_input, text="DEQUEUE", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=15, command=proses_dequeue)
            btn.grid(row=1, column=1, padx=15)

        # ------------------------------------------------------
        # M2: STACK - UNDO & REDO
        # ------------------------------------------------------
        elif "UNDO" in judul_menu or "REDO" in judul_menu:
            is_undo = "UNDO" in judul_menu
            judul_teks = "Stack: batalkan aksi antrean terakhir" if is_undo else "Stack: kerjakan lagi aksi yang dibatalkan"
            sub_teks = "Mengambil catatan teratas tumpukan undo lalu menjalankan kebalikannya." if is_undo else "Mengambil catatan teratas tumpukan redo lalu menjalankan aksi aslinya."
            btn_teks = "UNDO" if is_undo else "REDO"

            self.buat_header(judul_teks, sub_teks)

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), justify=tk.LEFT, anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("#", "oid", "pelanggan", "resto", "menu")
            tree = self.buat_tabel(kolom)

            def proses_undo_redo():
                for item in tree.get_children():
                    tree.delete(item)

                t0 = time.perf_counter()
                if is_undo:
                    if self.stack_undo.is_empty():
                        label_info.config(text="Tumpukan undo kosong, tidak ada aksi yang bisa dibatalkan.")
                        return
                    aksi, pesanan_list = self.stack_undo.pop()
                    self.stack_redo.push((aksi, pesanan_list))

                    if aksi == 'ENQUEUE':
                        # kebalikannya: keluarkan lagi dari belakang
                        for _ in pesanan_list:
                            # pop dari naif
                            if len(self.antrean_naif.data) > 0:
                                self.antrean_naif.data.pop()
                            # kurangi circular
                            if self.antrean_circular.count > 0:
                                self.antrean_circular.rear = (self.antrean_circular.rear - 1) % self.antrean_circular.kapasitas
                                self.antrean_circular.data[self.antrean_circular.rear] = None
                                self.antrean_circular.count -= 1
                        msg = f"Pembatalan enqueue: {len(pesanan_list)} pesanan dikeluarkan lagi dari belakang."
                    else: # DEQUEUE
                        # kebalikannya: kembalikan ke depan
                        for p in pesanan_list:
                            self.antrean_naif.data.insert(0, p)
                            # masukkan ke depan circular
                            self.antrean_circular.front = (self.antrean_circular.front - 1) % self.antrean_circular.kapasitas
                            self.antrean_circular.data[self.antrean_circular.front] = p
                            self.antrean_circular.count += 1
                        msg = f"Pembatalan dequeue: {len(pesanan_list)} pesanan dikembalikan ke DEPAN antrean."

                    cmd = "stack_undo"
                else: # REDO
                    if self.stack_redo.is_empty():
                        label_info.config(text="Tumpukan redo kosong, tidak ada yang diulang.")
                        return
                    aksi, pesanan_list = self.stack_redo.pop()
                    self.stack_undo.push((aksi, pesanan_list))

                    if aksi == 'ENQUEUE':
                        for p in pesanan_list:
                            self.antrean_naif.enqueue(p)
                            self.antrean_circular.enqueue(p)
                        msg = f"Redo enqueue: {len(pesanan_list)} pesanan masuk kembali ke belakang."
                    else: # DEQUEUE
                        for _ in pesanan_list:
                            self.antrean_naif.dequeue()
                            self.antrean_circular.dequeue()
                        msg = f"Redo dequeue: {len(pesanan_list)} pesanan keluar lagi dari depan antrean."

                    cmd = "stack_redo"

                durasi = (time.perf_counter() - t0) * 1000
                self.log_cmd(cmd, "M2 - stack", durasi)

                label_info.config(text=f"{msg}\n"
                                       f"Panjang antrean sekarang: naif {len(self.antrean_naif):,}, circular {len(self.antrean_circular):,}.\n"
                                       f"Tumpukan undo: {len(self.stack_undo)}, redo: {len(self.stack_redo)}.")

                for idx, row in enumerate(pesanan_list[:50], 1):
                    oid_val = row[0] if len(row) > 0 else "-"
                    pel_val = row[1] if len(row) > 1 else "-"
                    resto_val = row[2] if len(row) > 2 else "-"
                    menu_val = row[3] if len(row) > 3 else "-"
                    tree.insert("", tk.END, values=(idx, oid_val, pel_val, resto_val, menu_val))

            btn = tk.Button(frame_input, text=btn_teks, bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=15, command=proses_undo_redo)
            btn.pack(side=tk.LEFT)

        # ------------------------------------------------------
        # M3: SORT - INSERTION SORT & MERGE SORT
        # ------------------------------------------------------
        elif "SORT" in judul_menu:
            is_insertion = "INSERTION" in judul_menu
            judul_teks = "Sort: insertion sort, O(n^2)" if is_insertion else "Sort: merge sort, O(n log n)"
            sub_teks = "Setiap elemen digeser mundur sampai menemukan tempatnya." if is_insertion else "Larik dibelah dua terus-menerus, lalu potongan yang sudah terurut disatukan kembali."
            cmd_log = "insertion_sort" if is_insertion else "merge_sort"
            method_log = "M3 - insertion sort" if is_insertion else "M3 - merge sort"

            self.buat_header(judul_teks, sub_teks)

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Jumlah baris diurutkan", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_n = tk.Entry(frame_input, width=15)
            entry_n.insert(0, "2000" if is_insertion else "4000")
            entry_n.grid(row=1, column=0, sticky="w", pady=(2, 0), padx=(0, 20))

            tk.Label(frame_input, text="Diurutkan menurut", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="w")
            combo_kunci = ttk.Combobox(frame_input, values=["harga", "oid", "selesai"], width=12, state="readonly")
            combo_kunci.current(0)
            combo_kunci.grid(row=1, column=1, sticky="w", pady=(2, 0), padx=(0, 20))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), justify=tk.LEFT, anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("#", "oid", "harga", "selesai", "resto", "menu")
            tree = self.buat_tabel(kolom)

            def proses_sort():
                for item in tree.get_children():
                    tree.delete(item)

                try:
                    n = int(entry_n.get().strip())
                except ValueError:
                    label_info.config(text="Jumlah baris harus angka!")
                    return

                kunci = combo_kunci.get()

                # Ambil subset data dari 200.000 data
                data_sort = self.semua_pesanan[:n]

                if is_insertion and n > 20000:
                    label_info.config(text="DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh.")
                    return

                t0 = time.perf_counter()
                if is_insertion:
                    hasil_urut, perbandingan = insertion_sort(data_sort, kunci=kunci)
                else:
                    hasil_urut, perbandingan = merge_sort(data_sort, kunci=kunci)
                durasi = (time.perf_counter() - t0) * 1000

                self.log_cmd(cmd_log, method_log, durasi)

                label_info.config(text=f"{len(hasil_urut):,} pesanan diurutkan menurut {kunci}.\n"
                                       f"{perbandingan:,} perbandingan.")

                for idx, row in enumerate(hasil_urut[:50], 1):
                    oid_val = row[0] if len(row) > 0 else "-"
                    resto_val = row[2] if len(row) > 2 else "-"
                    menu_val = row[3] if len(row) > 3 else "-"
                    harga_val = row[4] if len(row) > 4 else "-"
                    selesai_val = row[7] if len(row) > 7 else "-"
                    tree.insert("", tk.END, values=(idx, oid_val, harga_val, selesai_val, resto_val, menu_val))

            btn = tk.Button(frame_input, text="URUTKAN", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=15, command=proses_sort)
            btn.grid(row=1, column=2, padx=10)

        # ------------------------------------------------------
        # M3: SEARCH - LINEAR SEARCH & BINARY SEARCH
        # ------------------------------------------------------
        elif "SEARCH" in judul_menu:
            is_binary = "BINARY" in judul_menu
            judul_teks = "Search: binary search, O(log n)" if is_binary else "Search: linear search, O(n)"
            sub_teks = "Membuang separuh sisa daftar pada setiap perbandingan. Menuntut daftar terurut menurut oid." if is_binary else "Memeriksa pesanan satu per satu dari depan. Tidak menuntut data terurut."
            cmd_log = "binary_search" if is_binary else "linear_search"
            method_log = "M3 - binary search" if is_binary else "M3 - linear search"

            self.buat_header(judul_teks, sub_teks)

            frame_input = tk.Frame(self.frame_konten, bg="white")
            frame_input.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(frame_input, text="Nomor pesanan (oid)", bg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
            entry_oid = tk.Entry(frame_input, width=25)
            entry_oid.insert(0, "O-137442")
            entry_oid.grid(row=1, column=0, sticky="w", pady=(2, 0))

            label_info = tk.Label(self.frame_konten, text="", bg="white", font=("Arial", 9), justify=tk.LEFT, anchor="w")
            label_info.pack(fill=tk.X, padx=15, pady=(0, 5))

            kolom = ("kolom", "isi")
            tree = self.buat_tabel(kolom)

            def proses_cari():
                target_oid = entry_oid.get().strip()
                if not target_oid: return

                for item in tree.get_children():
                    tree.delete(item)

                msg_indeks = ""
                if is_binary:
                    # Pastikan data sudah terurut menurut oid
                    if self.pesanan_terurut_oid is None:
                        t_build0 = time.perf_counter()
                        self.pesanan_terurut_oid, _ = merge_sort(self.semua_pesanan, kunci='oid')
                        self.waktu_buat_indeks_oid = (time.perf_counter() - t_build0) * 1000
                        msg_indeks = f"Daftar terurut oid dibangun sekali dengan merge sort, {self.waktu_buat_indeks_oid:.2f} ms.\n"

                    t0 = time.perf_counter()
                    idx, perbandingan = binary_search(self.pesanan_terurut_oid, target_oid, kunci='oid')
                    durasi = (time.perf_counter() - t0) * 1000
                    data_sumber = self.pesanan_terurut_oid
                else:
                    t0 = time.perf_counter()
                    idx, perbandingan = linear_search(self.semua_pesanan, target_oid, kunci='oid')
                    durasi = (time.perf_counter() - t0) * 1000
                    data_sumber = self.semua_pesanan

                self.log_cmd(cmd_log, method_log, durasi)

                if idx == -1:
                    label_info.config(text=f"{msg_indeks}Pesanan {target_oid} tidak ditemukan. ({perbandingan:,} perbandingan)")
                else:
                    pesanan = data_sumber[idx]
                    label_info.config(text=f"{msg_indeks}Ditemukan pada indeks {idx:,} dari {len(data_sumber):,} baris.\n"
                                           f"{perbandingan:,} perbandingan.")
                    field_names = ("oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status")
                    for k, v in zip(field_names, pesanan):
                        tree.insert("", tk.END, values=(k, v))

            btn = tk.Button(frame_input, text="CARI", bg="#2c4260", fg="white", font=("Arial", 9, "bold"),
                            width=12, command=proses_cari)
            btn.grid(row=1, column=1, padx=15)