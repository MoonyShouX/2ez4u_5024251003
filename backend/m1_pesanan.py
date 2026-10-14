class Array:
    def __init__(self):
        self.kapasitas = 4
        self.isi = 0
        self.data = [None] * self.kapasitas

    def _tambah_kapasitas(self):
        self.kapasitas *= 2
        rak_baru = [None] * self.kapasitas
        for i in range(self.isi):
            rak_baru[i] = self.data[i]
        self.data = rak_baru

    def tambah_reguler(self, pesanan):
        if self.isi == self.kapasitas:
            self._tambah_kapasitas()
        self.data[self.isi] = pesanan
        self.isi += 1

    def tambah_vip(self, pesanan):
        if self.isi == self.kapasitas:
            self._tambah_kapasitas()
        for i in range(self.isi,0,-1):
            self.data[i] = self.data[i-1]
        self.data[0] = pesanan
        self.isi += 1
    def tambah_prioritas(self, pesanan):
        if self.isi == self.kapasitas:
            self._tambah_kapasitas()
        posisi = self.isi // 2
        for i in range(self.isi,posisi,-1):
            self.data[i] = self.data[i-1]
        self.data[posisi] = pesanan
        self.isi += 1

    def append(self, pesanan):
        self.tambah_reguler(pesanan)

    def insert(self, indeks, pesanan):
        if indeks < 0 or indeks > self.isi:
            return
        if self.isi == self.kapasitas:
            self._tambah_kapasitas()
        for i in range(self.isi, indeks, -1):
            self.data[i] = self.data[i - 1]
        self.data[indeks] = pesanan
        self.isi += 1

    def get(self, indeks):
        if indeks < 0 or indeks >= self.isi:
            return None
        return self.data[indeks]

    def hapus_pesanan(self, indeks):
        if indeks < 0 or indeks >= self.isi:
            print("Indeks not found")
            return None

        item_dihapus = self.data[indeks]
        for i in range(indeks, self.isi - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.isi - 1] = None
        self.isi -= 1
        return item_dihapus

    def lihat_pesanan(self, indeks=None):
        if indeks is not None:
            return self.get(indeks)
        hasil = []
        for i in range(self.isi):
            hasil.append(self.data[i])
        return hasil

    def __len__(self):
        return self.isi


from backend.m1_linked_list import Node, LinkedList
LinkList = LinkedList




