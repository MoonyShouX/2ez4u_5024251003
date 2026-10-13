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

    def tambah_vip(self, pesanan):
        gerbong_baru = Node(pesanan)
        gerbong_baru.next = self.head
        self.head = gerbong_baru

        if self.tail is None:
            self.tail = gerbong_baru

    def tambah_prioritas(self, pesanan):
        total = 0
        saat_ini = self.head
        while saat_ini is not None:
            total += 1
            saat_ini = saat_ini.next

        tengah = total // 2

        if tengah == 0:
            self.tambah_vip(pesanan)
            return

        sebelum = self.head
        for i in range(tengah - 1):
            sebelum = sebelum.next

        gerbong_baru = Node(pesanan)
        gerbong_baru.next = sebelum.next
        sebelum.next = gerbong_baru

    def hapus_pesanan(self, posisi):
        if self.head is None:
            print("Antrean masih kosong!")
            return

        if posisi == 0:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return

        sebelum = self.head
        for i in range(posisi - 1):
            if sebelum.next is None:
                print("Posisi tidak ditemukan!")
                return
            sebelum = sebelum.next

        if sebelum.next is None:
            print("Posisi tidak ditemukan!")
            return

        if sebelum.next == self.tail:
            self.tail = sebelum

        sebelum.next = sebelum.next.next

    def lihat_pesanan(self):
        hasil = []
        saat_ini = self.head

        while saat_ini is not None:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next

        print("Daftar Pesanan Saat Ini:", hasil)
        return hasil