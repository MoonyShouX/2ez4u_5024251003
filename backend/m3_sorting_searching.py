# Fungsi pembantu untuk mengambil nilai kunci perbandingan dari tuple/list data pesanan
def _ambil_nilai(item, kunci):
    if callable(kunci):
        return kunci(item)

    if isinstance(item, (list, tuple)):
        # Cek nama kolom
        if kunci == 'oid' or kunci == 0:
            return item[0]
        elif kunci == 'pelanggan' or kunci == 1:
            return item[1]
        elif kunci == 'resto' or kunci == 2:
            return item[2]
        elif kunci == 'menu' or kunci == 3:
            return item[3]
        elif kunci == 'harga' or kunci == 4:
            try:
                return int(item[4])
            except (ValueError, TypeError):
                return item[4]
        elif kunci == 'prioritas' or kunci == 5:
            try:
                return int(item[5])
            except (ValueError, TypeError):
                return item[5]
        elif kunci == 'masuk' or kunci == 't_masuk_detik' or kunci == 6:
            try:
                return int(item[6])
            except (ValueError, TypeError):
                return item[6]
        elif kunci == 'selesai' or kunci == 't_selesai_detik' or kunci == 7:
            try:
                return int(item[7])
            except (ValueError, TypeError):
                return item[7]
        elif kunci == 'status' or kunci == 8:
            return item[8]
        elif isinstance(kunci, int) and 0 <= kunci < len(item):
            val = item[kunci]
            try:
                return int(val)
            except (ValueError, TypeError):
                return val

    return item


def _bandingkan(a, b):
    # Bandingkan dua nilai (bisa numerik atau teks)
    try:
        fa = float(a)
        fb = float(b)
        if fa < fb:
            return -1
        elif fa > fb:
            return 1
        return 0
    except (ValueError, TypeError):
        sa = str(a)
        sb = str(b)
        if sa < sb:
            return -1
        elif sa > sb:
            return 1
        return 0


# Insertion Sort: stabil (memakai > bukan >=), tolak bila n > 20.000
def insertion_sort(larik, kunci='harga'):
    n = len(larik)
    if n > 20000:
        print("DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh")
        return larik, 0

    data = list(larik)
    perbandingan = 0

    for i in range(1, n):
        simpan = data[i]
        nilai_simpan = _ambil_nilai(simpan, kunci)
        j = i - 1

        while j >= 0:
            perbandingan += 1
            nilai_j = _ambil_nilai(data[j], kunci)
            if _bandingkan(nilai_j, nilai_simpan) > 0:
                data[j + 1] = data[j]
                j -= 1
            else:
                break
        data[j + 1] = simpan

    return data, perbandingan


# Merge Sort: stabil (memakai <= saat gabung)
def merge_sort(larik, kunci='harga'):
    data = list(larik)
    hitung_banding = [0]

    def _pisahkan_dan_gabung(arr):
        if len(arr) <= 1:
            return arr

        tengah = len(arr) // 2
        kiri = _pisahkan_dan_gabung(arr[:tengah])
        kanan = _pisahkan_dan_gabung(arr[tengah:])

        hasil = []
        i = 0
        j = 0
        n_kiri = len(kiri)
        n_kanan = len(kanan)

        while i < n_kiri and j < n_kanan:
            hitung_banding[0] += 1
            nilai_kiri = _ambil_nilai(kiri[i], kunci)
            nilai_kanan = _ambil_nilai(kanan[j], kunci)

            # <= agar stabil (elemen bagian kiri didahulukan)
            if _bandingkan(nilai_kiri, nilai_kanan) <= 0:
                hasil.append(kiri[i])
                i += 1
            else:
                hasil.append(kanan[j])
                j += 1

        while i < n_kiri:
            hasil.append(kiri[i])
            i += 1
        while j < n_kanan:
            hasil.append(kanan[j])
            j += 1

        return hasil

    hasil_terurut = _pisahkan_dan_gabung(data)
    return hasil_terurut, hitung_banding[0]


# Linear Search: menelusuri dari awal satu per satu
def linear_search(larik, target, kunci='oid'):
    perbandingan = 0
    for i in range(len(larik)):
        perbandingan += 1
        nilai = _ambil_nilai(larik[i], kunci)
        if _bandingkan(nilai, target) == 0:
            return i, perbandingan
    return -1, perbandingan


# Binary Search: separuh sisa tiap langkah (data harus sudah terurut)
def binary_search(larik, target, kunci='oid'):
    lo = 0
    hi = len(larik) - 1
    perbandingan = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        nilai = _ambil_nilai(larik[mid], kunci)
        perbandingan += 1

        cmp = _bandingkan(nilai, target)
        if cmp == 0:
            return mid, perbandingan
        elif cmp < 0:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, perbandingan
