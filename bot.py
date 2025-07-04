from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os
import logging
import pytz

# Konfigurasi logging untuk debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7941038639:AAE1RCoWFE85yfxXm4neRWABBqBdQhdSWV0"

LOOKER_STUDIO_MSA_WSA_URL = "https://lookerstudio.google.com/s/tR0woFxlU6g"
LOOKER_STUDIO_PILATEN_URL = "https://lookerstudio.google.com/s/sw2UI-AT_Yw"

# Mengambil image laporan menggunakan ScreenshotAPI.net
SCREENSHOT_API_KEY = "5AMQNJ2-48649WX-GDNY765-F9DH7HY"
SCREENSHOT_API_URL = "https://shot.screenshotapi.net/screenshot"

TARGET_CHAT_ID = "1003337187" 

# Zona waktu untuk penjadwalan (Malang, Indonesia = Asia/Jakarta)
TIMEZONE = pytz.timezone('Asia/Jakarta')

# --- Fungsi untuk Mengambil Screenshot ---
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
        "full_page": "true",
        "delay": 5000
    }
    
    try:
        logger.info(f"Mencoba mengambil screenshot dari: {looker_studio_url}")
        response = requests.get(SCREENSHOT_API_URL, params=params, stream=True)
        response.raise_for_status()
        response_json = response.json()
        image_url = response_json.get('screenshot')
        if not image_url:
            logger.error(f"ERROR: Tidak ada URL screenshot ditemukan dalam respons dari ScreenshotAPI.net. Respons: {response_json}")
            return None
        logger.info(f"URL Gambar Screenshot Diterima: {image_url}")
        image_data_response = requests.get(image_url, stream=True)
        image_data_response.raise_for_status()
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
async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mengambil screenshot Dashboard MSA/WSA, harap tunggu sebentar...")
    image_path = get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "msawsa_dashboard.png")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            await update.message.reply_photo(image_file, caption="Laporan MSA/WSA:")
        os.remove(image_path)
        logger.info(f"File screenshot lokal dihapus: {image_path}")
    else:
        await update.message.reply_text("Maaf, gagal mengambil screenshot dashboard MSA/WSA. "
                                        "Periksa log untuk detail lebih lanjut dan pastikan "
                                        "API Key ScreenshotAPI.net sudah benar dan dashboard dapat diakses publik.")

async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mengambil screenshot Dashboard PI LATEN, harap tunggu sebentar...")
    image_path = get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "pilaten_dashboard.png")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            await update.message.reply_photo(image_file, caption="Laporan PI LATEN:")
        os.remove(image_path)
        logger.info(f"File screenshot lokal dihapus: {image_path}")
    else:
        await update.message.reply_text("Maaf, gagal mengambil screenshot dashboard PI LATEN. "
                                        "Periksa log untuk detail lebih lanjut dan pastikan "
                                        "API Key ScreenshotAPI.net sudah benar dan dashboard dapat diakses publik.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Selamat datang! Berikut daftar perintah yang bisa digunakan:\n\n"
        "/start - Menampilkan pesan ini\n"
        "/msawsa - Melihat laporan MSA/WSA\n"
        "/pilaten - Melihat dashboard PI LATEN\n"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

# --- Fungsi Utama (Main Execution) ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("msawsa", msawsa))
    app.add_handler(CommandHandler("pilaten", pilaten))

    logger.info("Bot Telegram dimulai dan mendengarkan pesan...")
    app.run_polling()

if __name__ == "__main__":
    main()