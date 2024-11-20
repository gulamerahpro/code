from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Ganti dengan API ID dan API Hash Anda
api_id = ''
api_hash = ''
phone = ''

# Nama file untuk menyimpan pesan
output_file = "telegram_messages.txt"

# Ganti dengan username atau ID channel
channel_username = '@warpplus'

# Fungsi untuk menyimpan pesan
def save_messages_to_file(messages):
    with open(output_file, "w", encoding="utf-8") as file:
        for message in messages:
            if message.message:
                file.write(f"{message.date} - {message.message}\n")

# Menghubungkan ke Telegram
with TelegramClient(phone, api_id, api_hash) as client:
    print("Berhasil login!")
    # Mendapatkan history pesan
    messages = client.iter_messages(channel_username, limit=100)  # Ubah limit sesuai kebutuhan
    save_messages_to_file(messages)
    print(f"Pesan berhasil disimpan di {output_file}")
