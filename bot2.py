import os
import logging
import pytz
import requests
import time
import asyncio
from datetime import time as dt_time
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from PIL import Image
from playwright.async_api import async_playwright

# --- Konfigurasi ---
TOKEN = "7941038639:AAGOUrsa05AbgV46g-WmLszUig26Fd-tIDk"

LOOKER_STUDIO_MSA_WSA_URL = "https://lookerstudio.google.com/s/i3tlaggtDik"
LOOKER_STUDIO_PILATEN_URL = "https://lookerstudio.google.com/s/s2yRKBhqWME"

# Mengambil image laporan menggunakan ScreenshotAPI.net
SCREENSHOT_API_KEY = "7WSF13V-V5XM4HB-Q7TZQQE-X59GJKH"
SCREENSHOT_API_URL = "https://shot.screenshotapi.net/screenshot"

TARGET_CHAT_ID = "1003337187" 
TIMEZONE = pytz.timezone("Asia/Jakarta")

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fungsi crop
def crop_image(input_path: str, output_path: str, crop_box: tuple[int, int, int, int]) -> str:
    try:
        with Image.open(input_path) as img:
            cropped = img.crop(crop_box)
            cropped.save(output_path)
        os.remove(input_path)  # Hapus gambar original
        return output_path
    except Exception as e:
        logger.error(f"❌ Gagal crop gambar: {e}")
        return input_path  # fallback
# --- Fungsi Screenshot ---
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str, crop_box: tuple[int, int, int, int]) -> str | None:
    temp_path = f"full_{output_filename}"
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1920, "height": 1080})
            page = await context.new_page()
            await page.goto(looker_studio_url, timeout=60000)
            await page.wait_for_timeout(7000)  # waktu tunggu load chart
            await page.screenshot(path=temp_path, full_page=True)
            await browser.close()

        cropped_path = crop_image(temp_path, output_filename, crop_box)
        return cropped_path
    except Exception as e:
        logger.error(f"❌ Gagal ambil screenshot pakai Playwright: {e}")
        return None

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Silahkan pilih menu berikut untuk melihat laporan yang diinginkan:\n"
        "/msawsa - Laporan MSA/WSA\n"
        "/pilaten - Laporan PI LATEN"
    )
# Daftar section dan posisi crop-nya (left, top, right, bottom)
SECTION_COORDINATES = {
    "FULL_DASHBOARD": (480, 80, 1700, 1020),  # keseluruhan canvas
    "FULFILLMENT_FBB": (480, 80, 820, 370),   # baris 1 kolom 1
    "ASSURANCE_FBB": (887, 80, 1294, 393),    # baris 1 kolom 2
    "SCORE_CREDIT": (1294, 80, 1700, 393),    # baris 1 kolom 3
    "FULFILLMENT_BGES": (480, 393, 887, 706), # baris 2 kolom 1
    "ASSURANCE_BGES": (887, 393, 1294, 706),  # baris 2 kolom 2
    "MSA_ASSURANCE": (1294, 393, 1700, 706),  # baris 2 kolom 3
    "MSA_CNOP": (480, 706, 887, 1020),        # baris 3 kolom 1
    "MSA_QUALITY": (1294, 706, 1700, 1020)    # baris 3 kolom 3
}


async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("FULL DASHBOARD", callback_data='FULL_DASHBOARD')],
        [InlineKeyboardButton("FULFILLMENT_FBB", callback_data='FULFILLMENT_FBB')],
        [InlineKeyboardButton("ASSURANCE_FBB", callback_data='ASSURANCE_FBB')],
        [InlineKeyboardButton("SCORE CREDIT", callback_data='SCORE_CREDIT')],
        [InlineKeyboardButton("FULFILLMENT BGES", callback_data='FULFILLMENT_BGES')],
        [InlineKeyboardButton("ASSURANCE BGES", callback_data='ASSURANCE_BGES')],
        [InlineKeyboardButton("MSA ASSURANCE", callback_data='MSA_ASSURANCE')],
        [InlineKeyboardButton("MSA CNOP", callback_data='MSA_CNOP')],
        [InlineKeyboardButton("MSA QUALITY", callback_data='MSA_QUALITY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧭 Pilih bagian dashboard yang ingin ditampilkan:", reply_markup=reply_markup)

async def msawsa_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("FULL DASHBOARD", callback_data='FULL_DASHBOARD')],
        [InlineKeyboardButton("FULFILLMENT_FBB", callback_data='FULFILLMENT_FBB')],
        [InlineKeyboardButton("ASSURANCE_FBB", callback_data='ASSURANCE_FBB')],
        [InlineKeyboardButton("SCORE CREDIT", callback_data='SCORE_CREDIT')],
        [InlineKeyboardButton("FULFILLMENT BGES", callback_data='FULFILLMENT_BGES')],
        [InlineKeyboardButton("ASSURANCE BGES", callback_data='ASSURANCE_BGES')],
        [InlineKeyboardButton("MSA ASSURANCE", callback_data='MSA_ASSURANCE')],
        [InlineKeyboardButton("MSA CNOP", callback_data='MSA_CNOP')],
        [InlineKeyboardButton("MSA QUALITY", callback_data='MSA_QUALITY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧭 Pilih bagian dashboard yang ingin ditampilkan:", reply_markup=reply_markup)

async def handle_section_crop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    section = query.data
    crop_box = SECTION_COORDINATES.get(section)

    if not crop_box:
        await query.edit_message_text("❌ Section tidak ditemukan.")
        return

    await query.edit_message_text(f"📸 Mengambil gambar untuk bagian: *{section.replace('_', ' ')}*", parse_mode="Markdown")

    path = await get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, f"{section}.png", crop_box)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=f, caption=section.replace("_", " "))
        os.remove(path)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text="❌ Gagal mengambil screenshot.")


# Crop box (left, top, right, bottom) — sesuaikan dengan posisi chart PI LATEN
CROP_PILATEN = (250, 250, 1250, 850)

async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Sedang mengambil gambar Laporan PI LATEN.\n Harap tunggu sebentar.")

    # Panggil fungsi screenshot pakai playwright + crop
    path = await get_looker_studio_screenshot(
        LOOKER_STUDIO_PILATEN_URL,
        "pilaten.png",
        CROP_PILATEN
    )

    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="Laporan PI LATEN")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal mengambil gambar Laporan PI LATEN.")


# --- Kirim Otomatis Gabungan ---
async def send_all_snapshots(context: ContextTypes.DEFAULT_TYPE):
    # --- MSA/WSA ---
    path1 = get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png")
    if path1 and os.path.exists(path1):
        with open(path1, "rb") as f:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=f,
                caption="🔔 Snapshot (Otomatis) MSA/WSA",
                parse_mode="Markdown"
            )
        os.remove(path1)
    else:
        logger.error("❌ Gagal mengirim laporan MSA/WSA")

    # Delay sebelum kirim PI LATEN
    await asyncio.sleep(5)

    # --- PI LATEN ---
    path2 = get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png")
    if path2 and os.path.exists(path2):
        with open(path2, "rb") as f:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=f,
                caption="🔔 Snapshot (Otomatis) PI LATEN",
                parse_mode="Markdown"
            )
        os.remove(path2)
    else:
        logger.error("❌ Gagal mengirim laporan PI LATEN")

# --- Fungsi Utama ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("msawsa", msawsa))
    app.add_handler(CommandHandler("pilaten", pilaten))
    app.add_handler(CommandHandler("msawsa_section", msawsa_section))
    app.add_handler(CallbackQueryHandler(handle_section_crop))

    job_queue = app.job_queue
    time_morning = dt_time(9, 0, tzinfo=TIMEZONE)
    time_evening = dt_time(21, 0, tzinfo=TIMEZONE)

    job_queue.run_daily(send_all_snapshots, time=time_morning)
    job_queue.run_daily(send_all_snapshots, time=time_evening)

    logger.info("Bot dimulai dengan jadwal otomatis.")
    app.run_polling()


if __name__ == "__main__":
    main()