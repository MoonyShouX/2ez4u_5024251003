import tkinter as tk
from backend.m1_pesanan import Array
from backend.m1_linked_list import LinkedList
from frontend.ui import Aplikasi2EZ4U


def muat_data_csv(nama_file, struktur_data):
    try:
        with open(nama_file, 'r') as file:
            file.readline()
            for baris in file:
                data_pecah = baris.strip().split(',')
                struktur_data.tambah_reguler(data_pecah)
        print(f"Selesai memuat {nama_file}!")
    except FileNotFoundError:
        print("Data CSV tidak ditemukan.")


if __name__ == "__main__":
    print("Memuat 200.000 data CSV... Mohon tunggu sebentar.")
    path_csv = "data/pesanan.csv"

    rak_pesanan = Array()
    kereta_pesanan = LinkedList()

    muat_data_csv(path_csv, kereta_pesanan)

    root = tk.Tk()
    app = Aplikasi2EZ4U(root, rak_pesanan, kereta_pesanan)
    root.mainloop()