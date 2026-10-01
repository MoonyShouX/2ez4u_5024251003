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

    def hapus_pesanan(self, indeks):

        if indeks < 0 or indeks >= self.isi:
            print("Indeks not found")
            return

        for i in range(indeks, self.isi - 1 ):
            self.data[i] = self.data[i+1]
        self.data[self.isi - 1 ] = None
        self.isi -= 1
    def lihat_pesanan(self):
        hasil = []
        for i in range(self.isi):
            hasil.append(self.data[i])
        print("Daftar Pesanan Sekarang:", hasil)
        return hasil


