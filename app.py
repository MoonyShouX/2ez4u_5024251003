import os
import csv
import tkinter as tk
from backend.m1_pesanan import Array
from backend.m1_linked_list import LinkedList
from frontend.ui import Aplikasi2EZ4U


def muat_data_csv(nama_file):
    semua_pesanan = []
    pesanan_antre = []
    rak = Array()
    kereta = LinkedList()

    try:
        with open(nama_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # lewati baris header
            for baris in reader:
                semua_pesanan.append(baris)
                rak.tambah_reguler(baris)
                kereta.tambah_reguler(baris)
                if len(baris) >= 9 and baris[8] == 'ANTRE':
                    pesanan_antre.append(baris)

        print(f"Selesai memuat {nama_file} ({len(semua_pesanan):,} baris)!")
    except FileNotFoundError:
        print(f"Data CSV tidak ditemukan di {nama_file}.")

    return rak, kereta, pesanan_antre, semua_pesanan


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_csv = os.path.join(base_dir, "data", "pesanan.csv")
    if not os.path.exists(path_csv):
        path_csv = "data/pesanan.csv"

    print("Memuat 200.000 data CSV dari folder data/... Mohon tunggu sebentar.")
    rak_pesanan, kereta_pesanan, data_antrean, semua_pesanan = muat_data_csv(path_csv)

    root = tk.Tk()
    app = Aplikasi2EZ4U(root, rak_pesanan, kereta_pesanan, data_antrean, semua_pesanan)
    root.mainloop()