from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
import logging
import pytz 

# Konfigurasi logging untuk debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7941038639:AAENqyPdkx2TGKFEq448fwZdBKEyUtzBE-g"

LOOKER_STUDIO_MSA_WSA_URL = "https://lookerstudio.google.com/s/tR0woFxlU6g"
LOOKER_STUDIO_PILATEN_URL = "https://lookerstudio.google.com/s/sw2UI-AT_Yw"

# Mengambil image laporan menggunakan ScreenshotAPI.net
SCREENSHOT_API_KEY = "5AMQNJ2-48649WX-GDNY765-F9DH7HY"
SCREENSHOT_API_URL = "https://shot.screenshotapi.net/screenshot"

TARGET_CHAT_ID = "1003337187" 

# Zona waktu untuk penjadwalan (Malang, Indonesia = Asia/Jakarta)
TIMEZONE = pytz.timezone('Asia/Jakarta')

# --- Fungsi Pembantu untuk Mengambil Screenshot ---
def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str) -> str | None:
    """
    Mengambil screenshot dari URL Looker Studio yang diberikan dan menyimpannya secara lokal.
    Mengembalikan path ke file gambar yang disimpan, atau None jika gagal.
    """
    if SCREENSHOT_API_KEY == "YOUR_SCREENSHOTAPI_NET_KEY" or not SCREENSHOT_API_KEY:
        logger.error("ERROR: SCREENSHOT_API_KEY belum dikonfigurasi. Harap masukkan kunci API Anda dari screenshotapi.net.")
        return None
    
    if not looker_studio_url:
        logger.error("ERROR: URL Looker Studio tidak boleh kosong.")
        return None

    params = {
        "token": SCREENSHOT_API_KEY,
        "url": looker_studio_url,
        "width": 1920,  
        "height": 1080, 
        "full_page": "true", # Ambil screenshot seluruh halaman, bukan hanya viewport
        "delay": 5000 # Tunggu 5 detik agar halaman Looker Studio dimuat sempurna (dalam milidetik)
    }
    
    try:
        logger.info(f"Mencoba mengambil screenshot dari: {looker_studio_url}")
        
        # Mengambil image dari ScreenshotAPI.net
        response = requests.get(SCREENSHOT_API_URL, params=params, stream=True)
        response.raise_for_status() # Akan memunculkan HTTPError jika respons 4xx/5xx

        response_json = response.json()
        image_url = response_json.get('screenshot')

        if not image_url:
            logger.error(f"ERROR: Tidak ada URL screenshot ditemukan dalam respons dari ScreenshotAPI.net. Respons: {response_json}")
            return None

        # debugging: Log URL gambar yang diterima
        logger.info(f"URL Gambar Screenshot Diterima: {image_url}")
        
        # Mengunduh gambar sebenarnya dari URL yang diberikan oleh ScreenshotAPI.net
        image_data_response = requests.get(image_url, stream=True)
        image_data_response.raise_for_status()

        # Menyimpan gambar ke file lokal
        with open(output_filename, 'wb') as f:
            for chunk in image_data_response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Screenshot berhasil disimpan secara lokal: {output_filename}")
        return output_filename

    except requests.exceptions.RequestException as e:
        logger.error(f"Kesalahan jaringan atau HTTP saat mengambil screenshot dari {looker_studio_url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Terjadi kesalahan tak terduga saat memproses screenshot: {e}", exc_info=True)
        return None


# --- Perintah Bot ---
def msawsa(update: Update, context: CallbackContext):
    """Menanggapi perintah /msawsa dengan hanya mengirim screenshot dashboard MSA/WSA."""
    update.message.reply_text("Mengambil screenshot Dashboard MSA/WSA, harap tunggu sebentar...")

    image_path = get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "msawsa_dashboard.png")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            update.message.reply_photo(image_file, caption="Laporan MSA/WSA:")
        os.remove(image_path) # Hapus file gambar lokal setelah dikirim
        logger.info(f"File screenshot lokal dihapus: {image_path}")
    else:
        update.message.reply_text("Maaf, gagal mengambil screenshot dashboard MSA/WSA. "
                                  "Periksa log untuk detail lebih lanjut dan pastikan "
                                  "API Key ScreenshotAPI.net sudah benar dan dashboard dapat diakses publik.")

def pilaten(update: Update, context: CallbackContext):
    """Menanggapi perintah /pilaten dengan hanya mengirim screenshot dashboard PI LATEN."""
    update.message.reply_text("Mengambil screenshot Dashboard PI LATEN, harap tunggu sebentar...")

    image_path = get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "pilaten_dashboard.png")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            update.message.reply_photo(image_file, caption="Laporan PI LATEN:")
        os.remove(image_path) # Hapus file gambar lokal setelah dikirim
        logger.info(f"File screenshot lokal dihapus: {image_path}")
    else:
        update.message.reply_text("Maaf, gagal mengambil screenshot dashboard PI LATEN. "
                                  "Periksa log untuk detail lebih lanjut dan pastikan "
                                  "API Key ScreenshotAPI.net sudah benar dan dashboard dapat diakses publik.")

def start(update: Update, context: CallbackContext):
    """Menanggapi perintah /start dan menampilkan daftar perintah."""
    message = (
        "Selamat datang! Berikut daftar perintah yang bisa digunakan:\n\n"
        "/start - Menampilkan pesan ini\n"
        "/msawsa - Melihat laporan MSA/WSA (tautan & snapshot)\n"
        "/pilaten - Melihat dashboard PI LATEN (tautan & snapshot)\n"
        "\n_Snapshot dashboard akan dikirim secara otomatis ke chat ini setiap jam 9 pagi dan 9 malam WIB._"
    )
    update.message.reply_text(message, parse_mode='Markdown')

# --- Tugas Terjadwal (Automatic Scheduled Jobs) ---
def send_scheduled_msawsa(context: CallbackContext):
    """Mengirim screenshot dashboard MSA/WSA secara otomatis."""
    logger.info(f"Memicu pengiriman otomatis snapshot MSA/WSA ke chat ID: {TARGET_CHAT_ID}")
    
    if not TARGET_CHAT_ID or TARGET_CHAT_ID == "1003337187":
        logger.error("ERROR: TARGET_CHAT_ID belum dikonfigurasi. Penjadwalan otomatis tidak dapat berjalan.")
        return

    context.bot.send_message(chat_id=TARGET_CHAT_ID, text="⏰ *Laporan Otomatis: Snapshot Dashboard MSA/WSA*", parse_mode='Markdown')
    
    image_path = get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "msawsa_dashboard_scheduled.png")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            context.bot.send_photo(chat_id=TARGET_CHAT_ID, photo=image_file, caption="Snapshot Dashboard MSA/WSA:")
        os.remove(image_path)
        logger.info(f"Snapshot terjadwal MSA/WSA berhasil dikirim dan file lokal dihapus: {image_path}")
    else:
        context.bot.send_message(chat_id=TARGET_CHAT_ID, text="Maaf, gagal mengambil snapshot otomatis dashboard MSA/WSA.")
        logger.error("Gagal mengambil snapshot otomatis dashboard MSA/WSA. Periksa log.")

def send_scheduled_pilaten(context: CallbackContext):
    """Mengirim screenshot dashboard PI LATEN secara otomatis."""
    logger.info(f"Memicu pengiriman otomatis snapshot PI LATEN ke chat ID: {TARGET_CHAT_ID}")

    if not TARGET_CHAT_ID or TARGET_CHAT_ID == "1003337187":
        logger.error("ERROR: TARGET_CHAT_ID belum dikonfigurasi. Penjadwalan otomatis tidak dapat berjalan.")
        return

    context.bot.send_message(chat_id=TARGET_CHAT_ID, text="⏰ *Laporan Otomatis: Snapshot Dashboard PI LATEN*", parse_mode='Markdown')
    
    image_path = get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "pilaten_dashboard_scheduled.png")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            context.bot.send_photo(chat_id=TARGET_CHAT_ID, photo=image_file, caption="Snapshot Dashboard PI LATEN:")
        os.remove(image_path)
        logger.info(f"Snapshot terjadwal PI LATEN berhasil dikirim dan file lokal dihapus: {image_path}")
    else:
        context.bot.send_message(chat_id=TARGET_CHAT_ID, text="Maaf, gagal mengambil snapshot otomatis dashboard PI LATEN.")
        logger.error("Gagal mengambil snapshot otomatis dashboard PI LATEN. Periksa log.")


# --- Fungsi Utama (Main Execution) ---
def main():
    """Fungsi utama untuk menjalankan bot Telegram dan scheduler."""
    # Membuat Updater dan Dispatcher untuk bot
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Menambahkan Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("msawsa", msawsa))
    dp.add_handler(CommandHandler("pilaten", pilaten))

    # Mengatur Scheduler untuk tugas otomatis
    scheduler = BackgroundScheduler(timezone=str(TIMEZONE)) # Menggunakan timezone yang didefinisikan

    # Menambahkan tugas terjadwal untuk Dashboard MSA/WSA
    # Setiap jam 9 pagi (09:00)
    scheduler.add_job(send_scheduled_msawsa, 'cron', hour=9, minute=0, timezone=str(TIMEZONE), args=[updater.job_queue])
    # Setiap jam 9 malam (21:00)
    scheduler.add_job(send_scheduled_msawsa, 'cron', hour=21, minute=0, timezone=str(TIMEZONE), args=[updater.job_queue])
    
    # Menambahkan tugas terjadwal untuk Dashboard PI LATEN
    # Setiap jam 9 pagi (09:00)
    scheduler.add_job(send_scheduled_pilaten, 'cron', hour=9, minute=0, timezone=str(TIMEZONE), args=[updater.job_queue])
    # Setiap jam 9 malam (21:00)
    scheduler.add_job(send_scheduled_pilaten, 'cron', hour=21, minute=0, timezone=str(TIMEZONE), args=[updater.job_queue])

    # Memulai scheduler
    scheduler.start()
    logger.info("Scheduler telah diinisialisasi dan dimulai.")

    # Memulai polling bot Telegram
    logger.info("Bot Telegram dimulai dan mendengarkan pesan...")
    updater.start_polling()
    
    # Menjaga bot tetap berjalan hingga dihentikan secara manual (misal: Ctrl+C)
    updater.idle()

if __name__ == "__main__":
    main()