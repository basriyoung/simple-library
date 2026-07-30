from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# =====================================================================
# 1. CLASS ABSTRAK (ABSTRAKSI & ENKAPSULASI)
# =====================================================================
class ItemPerpustakaan(ABC):
    def __init__(self, id_item, judul, penulis):
        self._id_item = id_item        # Protected
        self._judul = judul            # Protected
        self._penulis = penulis        # Protected
        self.__status_dipinjam = False # Private (Enkapsulasi ketat)

    @property
    def id_item(self): return self._id_item

    @property
    def judul(self): return self._judul

    @property
    def penulis(self): return self._penulis

    @property
    def status_dipinjam(self): return self.__status_dipinjam

    @status_dipinjam.setter
    def status_dipinjam(self, status): self.__status_dipinjam = status

    @abstractmethod
    def tampilkan_info(self): pass


# =====================================================================
# 2. CLASS ANAK / TURUNAN (INHERITANSI & POLIMORFISME)
# =====================================================================
class Buku(ItemPerpustakaan):
    def __init__(self, id_item, judul, penulis, isbn):
        super().__init__(id_item, judul, penulis)
        self.isbn = isbn

    def tampilkan_info(self):
        status = "Dipinjam" if self.status_dipinjam else "Tersedia"
        return f"[BUKU] [{self.id_item}] {self.judul} - {self.penulis} (ISBN: {self.isbn}) | Status: {status}"


class Jurnal(ItemPerpustakaan):
    def __init__(self, id_item, judul, penulis, volume, nomor):
        super().__init__(id_item, judul, penulis)
        self.volume = volume
        self.nomor = nomor

    def tampilkan_info(self):
        status = "Dipinjam" if self.status_dipinjam else "Tersedia"
        return f"[JURNAL] [{self.id_item}] {self.judul} Vol.{self.volume} No.{self.nomor} | Status: {status}"


class KoleksiDigital(ItemPerpustakaan):
    def __init__(self, id_item, judul, penulis, format_file, url_unduh):
        super().__init__(id_item, judul, penulis)
        self.format_file = format_file
        self.url_unduh = url_unduh

    # Polimorfisme: Koleksi digital tidak bisa dipinjam secara fisik (selalu tersedia)
    def tampilkan_info(self):
        return f"[DIGITAL] [{self.id_item}] {self.judul} ({self.format_file}) | Link: {self.url_unduh} | Status: Selalu Tersedia"


# =====================================================================
# 3. CLASS ANGGOTA
# =====================================================================
class Anggota:
    def __init__(self, id_anggota, nama):
        self.id_anggota = id_anggota
        self.nama = nama


# =====================================================================
# 4. CLASS PEMINJAMAN (Mencatat Log Transaksi Aktif)
# =====================================================================
class Peminjaman:
    def __init__(self, anggota: Anggota, item: ItemPerpustakaan):
        self.anggota = anggota
        self.item = item
        self.tanggal_pinjam = datetime.now()
        self.tanggal_kembali = datetime.now() + timedelta(days=7) # Batas awal 7 hari

    def perpanjang_durasi(self):
        self.tanggal_kembali += timedelta(days=7) # Tambah 7 hari lagi

    def tampilkan_log(self):
        return f"Peminjam: {self.anggota.nama} | Item: '{self.item.judul}' | Batas Kembali: {self.tanggal_kembali.strftime('%Y-%m-%d')}"


# =====================================================================
# SYSTEM ENGINE (Manajer Aplikasi)
# =====================================================================
class PerpustakaanMaju:
    def __init__(self):
        self.koleksi_item = {}
        self.daftar_anggota = {}
        self.transaksi_aktif = {} # Menyimpan Objek dari Class Peminjaman (Key: id_item)

    def tambah_item(self, item: ItemPerpustakaan):
        self.koleksi_item[item.id_item] = item

    def tambah_anggota(self, anggota: Anggota):
        self.daftar_anggota[anggota.id_anggota] = anggota

    # Kasus 1: Pencarian
    def cari_item(self, kata_kunci):
        kata_kunci = kata_kunci.lower()
        return [item for item in self.koleksi_item.values()
                if kata_kunci in item.judul.lower() or kata_kunci in item.penulis.lower()]

    # Kasus 2: Peminjaman (Membuat Objek 'Peminjaman')
    def proses_pinjam(self, id_item, id_anggota):
        anggota = self.daftar_anggota.get(id_anggota)
        item = self.koleksi_item.get(id_item)

        if not anggota: return "❌ ID Anggota tidak ditemukan."
        if not item: return "❌ ID Item tidak ditemukan."
        if isinstance(item, KoleksiDigital):
            return f"✅ Sukses! '{item.judul}' adalah koleksi digital. Unduh langsung di: {item.url_unduh} (Akses diberikan ke {anggota.nama})."
        if item.status_dipinjam: return "❌ Maaf, item ini sedang dipinjam orang lain."

        # UBAH STATUS & BUAT OBJEK PEMINJAMAN BARU
        item.status_dipinjam = True
        log_baru = Peminjaman(anggota, item)
        self.transaksi_aktif[id_item] = log_baru # Objek Peminjaman disimpan di dictionary
        return f"✅ Berhasil dipinjam!\n   {log_baru.tampilkan_log()}"

    # Kasus 3: Perpanjangan (Memanggil Method di Objek Peminjaman)
    def proses_perpanjang(self, id_item):
        log_pinjam = self.transaksi_aktif.get(id_item)
        if not log_pinjam: return "❌ Tidak ada riwayat peminjaman aktif untuk item ini."

        log_pinjam.perpanjang_durasi() # Memanggil perilaku internal objek Peminjaman
        return f"✅ Perpanjangan Berhasil!\n   {log_pinjam.tampilkan_log()}"

    # Kasus 4: Pengembalian (Menghapus Objek Peminjaman)
    def proses_kembali(self, id_item):
        item = self.koleksi_item.get(id_item)
        log_pinjam = self.transaksi_aktif.get(id_item)

        if not item or not log_pinjam: return "❌ Item tidak valid atau sedang tidak dipinjam."

        item.status_dipinjam = False
        del self.transaksi_aktif[id_item] # Hapus transaksi dari memori aktif
        return f"✅ Terima kasih, '{item.judul}' telah berhasil dikembalikan ke rak!"


# =====================================================================
# USER INTERFACE MENU INTERAKTIF (CLI)
# =====================================================================
def main():
    sys = PerpustakaanMaju()
    
    # Inject Master Data Awal (Instansiasi Objek)
    sys.tambah_anggota(Anggota("A01", "Budi Santoso"))
    sys.tambah_anggota(Anggota("A02", "Siti Aminah"))
    sys.tambah_item(Buku("B01", "Laskar Pelangi", "Andrea Hirata", "978-979"))
    sys.tambah_item(Buku("B02", "Bumi Manusia", "Pramoedya Ananta Toer", "978-602"))
    sys.tambah_item(Jurnal("J01", "Riset AI Indonesia", "Dr. Dian", "Vol 12", "No 2"))
    sys.tambah_item(KoleksiDigital("D01", "E-Book Belajar Python", "Riko", "PDF", "perpus.id/dl/py"))

    while True:
        print("\n" + "="*50)
        print("    SISTEM MANAJEMEN PERPUSTAKAAN - OOP    ")
        print("    Hasan Basri - 2024230019    ")
        print("="*50)
        print("1. 🔍 Cari Buku / Lihat Semua Koleksi")
        print("2. 📑 Peminjaman Buku (Buat Objek Peminjaman)")
        print("3. ⏳ Perpanjangan Durasi Buku")
        print("4. 📦 Pengembalian Buku")
        print("5. ❌ Keluar Aplikasi")
        print("="*50)
        
        pilihan = input("Masukkan Pilihan (1-5): ").strip()

        if pilihan == "1":
            print("\n--- MENU PENCARIAN ---")
            keyword = input("Masukkan judul/penulis (Tekan ENTER langsung untuk lihat semua): ")
            hasil = sys.cari_item(keyword)
            print(f"\nMenampilkan {len(hasil)} Item Cocok:")
            for item in hasil:
                print(item.tampilkan_info())

        elif pilihan == "2":
            print("\n--- MENU PEMINJAMAN ---")
            id_anggota = input("Masukkan ID Anggota (Contoh: A01): ").strip()
            id_item = input("Masukkan ID Item (Contoh: B01 / J01): ").strip()
            print(sys.proses_pinjam(id_item, id_anggota))

        elif pilihan == "3":
            print("\n--- MENU PERPANJANGAN ---")
            id_item = input("Masukkan ID Item yang ingin diperpanjang: ").strip()
            print(sys.proses_perpanjang(id_item))

        elif pilihan == "4":
            print("\n--- MENU PENGEMBALIAN ---")
            id_item = input("Masukkan ID Item yang ingin dikembalikan: ").strip()
            print(sys.proses_kembali(id_item))

        elif pilihan == "5":
            print("\nSistem dimatikan. Sampai jumpa!")
            break
        else:
            print("\n❌ Pilihan salah! Masukkan angka 1 sampai 5.")

if __name__ == "__main__":
    main()
