import os
from datetime import datetime

# Fungsi untuk membersihkan layar
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Fungsi untuk membaca data rekening dari file
def baca_data_rekening():
    data = {} 
    if os.path.exists("data_rekening.txt"):
        with open("data_rekening.txt", "r") as f:
            for baris in f:
                norek, nama, pin, saldo = baris.strip().split("|")
                data[norek] = {"nama": nama, "pin": pin, "saldo": int(saldo)}
    return data

# Fungsi untuk menyimpan data rekening ke file
def simpan_data_rekening(data):
    with open("data_rekening.txt", "w") as f:
        for norek, info in data.items():
            f.write(f"{norek}|{info['nama']}|{info['pin']}|{info['saldo']}\n")
            
def catat_riwayat_tunggal(norek, nama, jumlah, jenis):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    baris = f"[{waktu}] Rekening: {norek} | {jenis} | Jumlah: Rp{jumlah}\n"
    with open(f"log_{norek}.txt", "a") as f:
        f.write(baris)

# Fungsi mencatat riwayat transaksi
def catat_riwayat(norek_pengirim, nama_pengirim, norek_penerima, nama_penerima, jumlah, jenis):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    baris = f"{waktu} | {jenis} | DARI: {norek_pengirim} ({nama_pengirim}) -> KE: {norek_penerima} ({nama_penerima}) | JUMLAH: Rp {jumlah}\n"
    for norek in [norek_pengirim, norek_penerima]:
        with open(f"log_{norek}.txt", "a") as f:
            f.write(baris)

# Fungsi tampilan awal login
def login(data):
    attempts = 0
    while True:
        clear()
        print("\t\t=== SELAMAT DATANG DI ATM ===")
        norek = input("\tMasukkan No Rekening: ").strip()
        if norek not in data:
            print("\tMohon Maaf, Nomor rekening anda tidak ditemukan! Silakan coba lagi.")
            print("\n")
            input("\tTekan ENTER untuk lanjut...")
            continue

        for i in range(3):
            pin = input("\tMasukkan PIN: ").strip()
            if pin == data[norek]["pin"]:
                print("\tLogin berhasil!")
                print("\n")
                input("\tTekan ENTER untuk lanjut...")
                return norek, data[norek]
            else:
                print("\tPIN salah! Percobaan ke", i+1, "dari 3")
        print("\tTerlalu banyak percobaan PIN salah!")
        print("\n")
        input("\tTekan ENTER untuk keluar...")
        return None, None

def pilih_bahasa():
    clear()
    print("\tSilahkan Pilih Bahasa yang anda dapat pahami:")
    print("\t1. Indonesia")
    print("\t2. English")
    print("\n")

    bahasa = input("\tPilih (1/2): ").strip()

    if bahasa == "1":
        return "id"  # Atau bisa langsung lanjut ke menu utama
    elif bahasa == "2":
        print("\n\tMaaf, terjadi kesalahan saat menggunakan bahasa Inggris.")
        input("\tTekan Enter untuk kembali...")
        return pilih_bahasa()  # Kembali ke pilihan bahasa
    else:
        print("\n\tInput tidak valid.")
        input("\tTekan Enter untuk coba lagi...")
        return pilih_bahasa()


# Fungsi menu utama
def menu(norek, user, data):
    while True:
        clear()
        print(f"\tSelamat Datang, {user['nama']}")
        print("\n")
        print("\t\t==== MENU ATM ====")
        print("\t1. Cek Saldo\t\t4. Transfer")
        print("\t2. Setor Tunai\t\t5. Ubah PIN")
        print("\t3. Tarik Tunai\t\t6. Keluar")
        print("\n")
        pilihan = input("\tPilih menu (1-6): ").strip()

        if pilihan == "1":
            print(f"\tSaldo Anda Sekarang : Rp {user['saldo']}")
            print("\n")
            input("\tTekan ENTER untuk kembali ke menu...") 

        elif pilihan == "2":
            jumlah = int(input("\tMasukkan jumlah setor: "))
            user['saldo'] += jumlah
            simpan_data_rekening(data)
            catat_riwayat_tunggal(norek, user['nama'], jumlah, "Setor Tunai")
            print("\tSetoran anda berhasil")
            print("\tData Transaksi anda akan disimpan!!")
            print("\n")
            input("\tTekan ENTER...")


        elif pilihan == "3":
            jumlah = int(input("\tMasukkan jumlah tarik: "))
            if jumlah > user['saldo']:
                print("\tMohon Maaf, Saldo Anda tidak mencukupi!")
            else:
                user['saldo'] -= jumlah
                simpan_data_rekening(data)
                catat_riwayat_tunggal(norek, user['nama'], jumlah, "Tarik Tunai")  # Log simpel
                print("\tPenarikan Berhasil")
                print("\tData Penarikan anda akan disimpan!!")
                print("\n")
            input("\tTekan ENTER...")


        elif pilihan == "4":
            norek_tujuan = input("\tMasukkan No Rekening Tujuan: ").strip()
            if norek_tujuan not in data:
                print("\tMohon Maaf, Nomor rekening tidak ditemukan!")
            else:
                jumlah = int(input("\tMasukkan jumlah transfer: "))
                if jumlah > user['saldo']:
                    print("\tMohon Maaf, Saldo anda tidak mencukupi!")
                else:
                    data[norek_tujuan]['saldo'] += jumlah
                    user['saldo'] -= jumlah
                    simpan_data_rekening(data)
                    catat_riwayat(norek, user['nama'], norek_tujuan, data[norek_tujuan]['nama'], jumlah, "TRANSFER")
                    print("\tTransfer Berasil")
                    print("\tData Transaksi anda akan disimpan!!")
                    print("\n")
            input("\tTekan ENTER...")

        elif pilihan == "5":
            pin_baru = input("\tMasukkan PIN baru: ").strip()
            user["pin"] = pin_baru
            simpan_data_rekening(data)
            print("\tPIN berhasil diubah.")
            print("\n")
            input("\tTekan ENTER...")

        elif pilihan == "6":
            print("\tTerima kasih telah menggunakan layanan ATM.")
            break
        else:
            print("\tPilihan tidak valid!")
            print("\n")
            input("\tTekan ENTER...")

# Program utama
def main():
    data = baca_data_rekening()
    norek, user = login(data)
    if norek:
        pilih_bahasa()
        menu(norek, user, data)

if __name__ == "__main__":
    main()
