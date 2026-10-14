class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.jumlah = 0

    def tambah_reguler(self, pesanan):
        gerbong_baru = Node(pesanan)

        if self.head is None:
            self.head = gerbong_baru
            self.tail = gerbong_baru
        else:
            self.tail.next = gerbong_baru
            self.tail = gerbong_baru
        self.jumlah += 1

    def append(self, pesanan):
        self.tambah_reguler(pesanan)

    def tambah_vip(self, pesanan):
        gerbong_baru = Node(pesanan)
        gerbong_baru.next = self.head
        self.head = gerbong_baru

        if self.tail is None:
            self.tail = gerbong_baru
        self.jumlah += 1

    def tambah_prioritas(self, pesanan):
        if self.head is None or self.jumlah == 0:
            self.tambah_vip(pesanan)
            return

        tengah = self.jumlah // 2
        if tengah == 0:
            self.tambah_vip(pesanan)
            return

        sebelum = self.head
        for i in range(tengah - 1):
            sebelum = sebelum.next

        gerbong_baru = Node(pesanan)
        gerbong_baru.next = sebelum.next
        sebelum.next = gerbong_baru

        if gerbong_baru.next is None:
            self.tail = gerbong_baru
        self.jumlah += 1

    def hapus_pesanan(self, posisi):
        if self.head is None or posisi < 0 or posisi >= self.jumlah:
            print("Posisi tidak ditemukan!")
            return None

        if posisi == 0:
            data_keluar = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.jumlah -= 1
            return data_keluar

        sebelum = self.head
        for i in range(posisi - 1):
            sebelum = sebelum.next

        data_keluar = sebelum.next.data
        if sebelum.next == self.tail:
            self.tail = sebelum

        sebelum.next = sebelum.next.next
        self.jumlah -= 1
        return data_keluar

    def get(self, posisi):
        if posisi < 0 or posisi >= self.jumlah:
            return None
        saat_ini = self.head
        for i in range(posisi):
            saat_ini = saat_ini.next
        return saat_ini.data

    def lihat_pesanan(self, posisi=None):
        if posisi is not None:
            return self.get(posisi)
        hasil = []
        saat_ini = self.head
        while saat_ini is not None:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

    def __len__(self):
        return self.jumlah