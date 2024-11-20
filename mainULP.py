import re

# Fungsi untuk memproses file dan mengekstrak user:pass
def extract_user_pass(input_file, output_file):
    # Membuka file input untuk membaca dengan encoding utf-8
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Membuka file output untuk menulis hasilnya
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            # Menggunakan regex untuk memisahkan dengan beberapa karakter (":", " ", dan "/")
            parts = re.split(r'[:/ ]+', line.strip())
            # Pastikan ada setidaknya dua bagian setelah split
            if len(parts) >= 2:
                user_pass = parts[-2] + ":" + parts[-1]
                # Menulis user:pass ke file output tanpa menambahkan baris kosong
                f.write(user_pass + '\n')

# Ganti 'new.txt' dengan nama file input Anda
# Ganti 'output4.txt' dengan nama file tempat hasil ekstraksi akan disimpan
extract_user_pass('edulive.txt', 'edulivec.txt')
