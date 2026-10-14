# Proyek 2EZ4U APP
**Studi Kasus Proyek Akhir Struktur Data & Analisa Algoritma (EC234303)**  
Departemen Teknik Komputer, FTEIC - Institut Teknologi Sepuluh Nopember  
Dosen Pengampu: Ir. Arta Kusuma Hernanda, S.T., M.T.

---

## 1. Deskripsi Proyek
Proyek **2EZ4U APP** adalah implementasi engine backend untuk sistem layanan pesan antar makanan (*food delivery service*) mirip GoFood/GrabFood versi mini. Seluruh struktur data dan algoritma inti pada proyek ini dibangun secara mandiri dari nol (primitif) tanpa menggunakan fungsi instan pustaka bawaan (`dict`, `set`, `.sort()`, `sorted()`, `heapq`, `bisect`, `collections.*`, dan literal `{ }`).

Aplikasi terdiri atas tiga layer:
1. **Data (`data/`)**: Database berkas CSV berisi 200.000 data transaksi pesanan (`pesanan.csv`) dan data graf lokasi (`peta.csv`).
2. **Backend (`backend/`)**: Berisi modul struktur data dan algoritma mandiri untuk setiap milestone (M1 hingga M3).
3. **Frontend (`frontend/`)**: Antarmuka GUI berbasis Python Tkinter (`frontend/ui.py`) yang dijalankan via `app.py`.

---

## 2. Struktur Repositori
```text
2ez4u/
|-- README.md                   <- Laporan dan Dokumentasi Proyek
|-- app.py                      <- Main application runner
|
|-- data/
|   |-- pesanan.csv             <- 200.000 baris data pesanan
|   '-- peta.csv                <- Data lokasi & peta graf
|
|-- backend/
|   |-- m1_pesanan.py           <- M1: Larik Dinamis (Array) + Rantai (Linked List)
|   |-- m1_linked_list.py       <- M1: Implementasi Linked List (Node, Head, Tail)
|   |-- m2_antrean.py           <- M2: Antrean Melingkar, Antrean Naif, Mesin Kasir & Undo/Redo
|   '-- m3_laporan.py           <- M3: Insertion Sort, Merge Sort, Linear Search, Binary Search
|
'-- frontend/
    '-- ui.py                   <- Tampilan GUI Tkinter dan panel COMMAND
```

---

## 3. Cara Menjalankan Aplikasi
Pastikan Python 3.11+ telah terpasang pada sistem. Buka terminal pada folder proyek, lalu jalankan:

```bash
python app.py
```

Setelah aplikasi terbuka:
1. Data dari `data/pesanan.csv` (200.000 baris) akan langsung dimuat secara otomatis.
2. Anda juga dapat menekan tombol **Load** di menu `DATA` kapan saja untuk membaca ulang berkas data secara bersih.
3. Seluruh perintah yang dijalankan akan tercatat di panel bawah **COMMAND** lengkap dengan durasi waktu eksekusi dalam milidetik (ms).

---

## 4. Penjelasan Implementasi & Analisis Tiap Milestone

### Milestone 1: Manajemen Data Pesanan (Array vs Linked List)
Menguji karakteristik dua struktur data dasar terhadap 3 skenario aturan bisnis penyisipan pesanan:
* **Pesanan REGULER (Prioritas 3)**: Mengantre di barisan paling belakang.
  * *Array*: $O(1)$ amortized (kapasitas berlipat ganda $2\times$ saat penuh).
  * *Linked List*: $O(1)$ (menggunakan pointer penunjuk `tail`).
* **Pesanan PRIORITAS (Prioritas 2)**: Menyerobot ke tengah barisan ($n // 2$).
  * *Array*: $O(n)$ (menggeser separuh isi array ke kanan).
  * *Linked List*: $O(n)$ (menelusuri $n // 2$ simpul dari depan lalu menyambungkan pointer).
* **Pesanan VIP (Prioritas 1)**: Langsung masuk ke urutan nomor 1 (paling depan).
  * *Array*: $O(n)$ (menggeser seluruh isi elemen array satu petak ke kanan).
  * *Linked List*: $O(1)$ (hanya menyambungkan simpul baru ke `head`).
* **Hapus Pesanan ke-$i$**:
  * *Array*: $O(n)$ (menggeser elemen dari $i+1$ hingga akhir satu petak ke kiri).
  * *Linked List*: $O(n)$ (menelusuri hingga posisi sebelum $i$ lalu memutus dan menyambung pointer).

---

### Milestone 2: Tumpukan (Stack) & Antrean (Queue)
1. **Mesin Kasir Postfix**:
   * Konversi ekspresi infix menjadi postfix menggunakan stack operator (contoh: `( 3 * 12000 ) + ( 2 * 8500 ) - 5000` $\rightarrow$ `3 12000 * 2 8500 * + 5000 -`). Operator `*` dan `/` memiliki prioritas lebih tinggi daripada `+` dan `-`.
   * Evaluasi postfix menggunakan stack angka untuk menghitung total pembayaran (Rp 48.000). Operand kanan ($b$) di-pop terlebih dahulu sebelum operand kiri ($a$), sehingga hasil pengurangan $a - b$ dan pembagian $a / b$ tidak terbalik.
2. **Antrean Naif vs Melingkar (Circular Queue)**:
   * **Antrean Naif**: Mengambil elemen indeks 0 lalu menggeser seluruh sisa elemen ke kiri ($O(n)$ per dequeue). Pada 19.850 data antrean, dequeue berulang menyebabkan jutaan kali operasi penggeseran memori.
   * **Antrean Melingkar**: Menggunakan larik berkapasitas tetap $K$ dengan pointer `front`, `rear`, dan pencacah `count` menggunakan operasi modulo `% K` ($O(1)$). Elemen tidak digeser sama sekali saat dequeue.
3. **Alasan Pemilihan Pencacah `count` pada Antrean Melingkar (PDF Hal. 11)**:
   * Pada antrean melingkar, kondisi **kosong** dan kondisi **penuh** sama-sama menyebabkan nilai pointer `front == rear`.
   * Untuk membedakannya, dipilih pendekatan **menyimpan variabel pencacah `count`** karena lebih sederhana, efisien, dan memanfaatkan seluruh slot kapasitas memori tanpa harus membuang satu slot kosong.
4. **Mekanisme Undo & Redo**:
   * Setiap aksi antrean dicatat ke tumpukan `undo`.
   * Jika ada aksi baru, tumpukan `redo` langsung dikosongkan untuk mencegah percabangan riwayat.
   * Pembatalan dequeue mengembalikan pesanan yang baru keluar ke posisi **DEPAN** antrean (bukan ke belakang).

---

### Milestone 3: Pengurutan (Sorting) & Pencarian (Searching)

#### Tabel Analisis Perbandingan: Insertion Sort vs Merge Sort
Pengujian dilakukan langsung pada dataset `data/pesanan.csv` dengan kunci pengurutan `harga`:

| Jumlah Data ($n$) | Algoritma | Waktu Eksekusi | Jumlah Perbandingan | Analisis Performa |
|:---:|:---:|:---:|:---:|:---|
| **10** | Insertion Sort | 0.11 ms | 24 | Sangat cepat untuk data kecil, hemat memori |
| **10** | Merge Sort | 0.15 ms | 22 | Sedikit overhead karena pemanggilan rekursif |
| **2.000** | Insertion Sort | 163.26 ms | **962.430** | Kompleksitas $O(n^2)$, kuadratik |
| **2.000** | Merge Sort | 6.36 ms | **19.240** | Kompleksitas $O(n \log n)$, jauh lebih cepat |
| **4.000** | Insertion Sort | 660.36 ms | **3.831.520** | Data naik $2\times$, perbandingan naik $\approx 4\times$ |
| **4.000** | Merge Sort | 13.66 ms | **42.355** | Data naik $2\times$, perbandingan hanya naik $\approx 2\times$ |
| **200.000** (Full) | Insertion Sort | - | - | **DITOLAK** ($n > 20.000$ baris) agar aplikasi tidak hang |
| **200.000** (Full) | Merge Sort | 2.43 s | **1.730.048** | Sukses mengurutkan seluruh 200.000 data |

#### Visualisasi Grafik Pertumbuhan Perbandingan ($n$ vs Perbandingan)
```text
Jumlah Perbandingan
    ^
4M  |                                      * [Insertion Sort n=4000: ~3.8M]
    |
2M  |
    |
1M  |                    * [Insertion Sort n=2000: ~962K]
    |
    |                                      . [Merge Sort n=4000: ~42K]
 0  +--------------------+-----------------+----------------------------------> n
    0                   2000              4000
```
> **Kesimpulan Grafik**: Kurva *Insertion Sort* melonjak tajam secara parabola ($n^2$), membuktikan kelemahannya untuk data besar. Sebaliknya, kurva *Merge Sort* tumbuh sangat landai mendekati linier ($n \log n$).

---

#### Tabel Analisis Pencarian: Linear Search vs Binary Search
Pengujian pencarian target pesanan `O-137442` pada total 200.000 baris data:

| Algoritma | Waktu Pencarian | Jumlah Perbandingan | Prasyarat Data |
|---|:---:|:---:|---|
| **Linear Search** | ~156 ms | **137.442** | Bebas, data boleh dalam kondisi acak |
| **Binary Search** | **< 0.05 ms** | **17** | Data **wajib** sudah terurut menurut kunci OID |

> *Catatan*: Indeks terurut OID untuk Binary Search dibangun satu kali menggunakan Merge Sort. Meskipun ada ongkos awal pengurutan, penghematan pada pencarian berulang sangat masif (hanya butuh 17 kali perbandingan dibandingkan 137.442 kali).

---

## 5. Pertanyaan Kunci & Bahan Penjelasan Lisan Demo (Oral Defense)

1. **Kenapa `insertion_sort` memakai operator `>` dan bukan `>=`?**
   * *Jawaban*: Agar algoritma bersifat **stabil** (*stable sort*). Jika memakai `>=`, elemen dengan kunci yang sama akan ikut tergeser ke kanan, sehingga urutan aslinya tertukar. Dengan `>`, pergeseran berhenti saat menemukan nilai yang sama, sehingga urutan asli pesanan tetap dipertahankan.
2. **Kenapa saat penggabungan `merge_sort` memakai operator `<=`?**
   * *Jawaban*: Pemakaian `<=` menjamin kestabilan. Jika elemen pada sub-array kiri bernilai sama dengan sub-array kanan, elemen kiri akan diprioritaskan masuk lebih dahulu ke array hasil.
3. **Bukti Kestabilan pada Dataset**:
   * Pesanan `O-000002` dan `O-000009` sama-sama memiliki harga Rp 11.000. Setelah diurutkan berdasarkan harga, posisi `O-000002` terbukti tetap berada di atas `O-000009` sesuai urutan aslinya.
4. **Kenapa Binary Search valid lolos uji kasus batas?**
   * Algoritma telah diuji dan terbukti bekerja benar pada 5 kondisi: target berada di posisi tengah, posisi paling kiri, posisi paling kanan, target tidak ada di dalam data, dan array dalam kondisi kosong.