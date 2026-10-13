from backend.m1_pesanan import Array
from backend.m1_linked_list import LinkedList


def muat_data_csv(nama_file, struktur_data):
    try:
        with open(nama_file, 'r') as file:
            header = file.readline()
            jumlah = 0

            for baris in file:
                data_pecah = baris.strip().split(',')
                struktur_data.tambah_reguler(data_pecah)
                jumlah += 1

        print(f"Sukses! Memuat {jumlah} data dari {nama_file}.")
        return struktur_data

    except FileNotFoundError:
        print(f"Error: File {nama_file} tidak ditemukan. Pastikan folder 'data' ada!")
        return None


if __name__ == "__main__":
    path_csv = "data/pesanan.csv"

    print("=== MENGUJI ARRAY ===")
    rak_pesanan = Array()
    rak_pesanan = muat_data_csv(path_csv, rak_pesanan)

    print("\n=== MENGUJI LINKED LIST ===")
    kereta_pesanan = LinkedList()
    kereta_pesanan = muat_data_csv(path_csv, kereta_pesanan)