import os
import logging
import pytz
import asyncio
from datetime import time as dt_time
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from PIL import Image
from playwright.async_api import async_playwright

# --- Konfigurasi ---
TOKEN = "7941038639:AAGOUrsa05AbgV46g-WmLszUig26Fd-tIDk"
LOOKER_STUDIO_MSA_WSA_URL = "https://lookerstudio.google.com/s/i3tlaggtDik"
LOOKER_STUDIO_PILATEN_URL = "https://lookerstudio.google.com/s/s2yRKBhqWME"
TARGET_CHAT_ID = "1003337187"
TIMEZONE = pytz.timezone("Asia/Jakarta")

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Fungsi Crop ---
def crop_image(input_path: str, output_path: str, crop_box: tuple[int, int, int, int]) -> str:
    try:
        with Image.open(input_path) as img:
            cropped = img.crop(crop_box)
            cropped.save(output_path)
        os.remove(input_path)
        return output_path
    except Exception as e:
        logger.error(f"❌ Gagal crop gambar: {e}")
        return input_path

# --- Fungsi Screenshot ---
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str, crop_box: tuple[int, int, int, int]) -> str | None:
    temp_path = f"full_{output_filename}"
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1920, "height": 1080})
            page = await context.new_page()
            await page.goto(looker_studio_url, timeout=60000)
            await page.wait_for_timeout(7000)
            await page.screenshot(path=temp_path, full_page=True)
            await browser.close()
        cropped_path = crop_image(temp_path, output_filename, crop_box)
        return cropped_path
    except Exception as e:
        logger.error(f"❌ Gagal ambil screenshot pakai Playwright: {e}")
        return None

# Daftar section dan posisi crop-nya (left, top, right, bottom)
SECTION_COORDINATES = {
    "FULL_DASHBOARD": (480, 80, 1700, 1020),  # keseluruhan canvas
    "FULFILLMENT_FBB": (485, 80, 820, 370),   # baris 1 kolom 1
    "ASSURANCE_FBB": (800, 170, 1210, 525),    # baris 1 kolom 2
    "SCORE_CREDIT": (1200, 170, 1700, 330),    # baris 1 kolom 3
    "FULFILLMENT_BGES": (485, 360, 820, 620), # baris 2 kolom 1
    "ASSURANCE_BGES": (485, 620, 810, 990),  # baris 2 kolom 2
    "MSA_ASSURANCE": (1205, 330, 1690, 690),  # baris 2 kolom 3
    "MSA_CNOP": (800, 515, 1210, 998),        # baris 3 kolom 1
    "MSA_QUALITY": (1205, 696, 1685, 995)    # baris 3 kolom 3
}

# --- Command: /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(TIMEZONE)
    hour = now.hour

    if 5 <= hour < 12:
        greeting = "Selamat pagi"
    elif 12 <= hour < 15:
        greeting = "Selamat siang"
    elif 15 <= hour < 18:
        greeting = "Selamat sore"
    else:
        greeting = "Selamat malam"

    await update.message.reply_text(
        f"Halo, {greeting}!\n\n"
        "Silakan pilih laporan yang ingin anda tampilkan:\n"
        "/msawsa - Laporan MSA/WSA\n"
        "/pilaten - Laporan PI LATEN"
    )

# --- Command: /msawsa ---
async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Memuat Laporan MSA/WSA.\nMohon Tunggu Sebentar.", parse_mode="Markdown")

    path = await get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "full_dashboard.png", SECTION_COORDINATES["FULL_DASHBOARD"])
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="Laporan MSA/WSA")
        os.remove(path)
    else:
        await update.message.reply_text("Gagal menampilkan laporan MSA/WSA.\nMohon coba lagi.")

    # Menu 2 kolom
    keyboard = [
        [InlineKeyboardButton("FULFILLMENT_FBB", callback_data='FULFILLMENT_FBB'),
         InlineKeyboardButton("ASSURANCE_FBB", callback_data='ASSURANCE_FBB')],
        [InlineKeyboardButton("SCORE CREDIT", callback_data='SCORE_CREDIT'),
         InlineKeyboardButton("FULFILLMENT BGES", callback_data='FULFILLMENT_BGES')],
        [InlineKeyboardButton("ASSURANCE BGES", callback_data='ASSURANCE_BGES'),
         InlineKeyboardButton("MSA ASSURANCE", callback_data='MSA_ASSURANCE')],
        [InlineKeyboardButton("MSA CNOP", callback_data='MSA_CNOP'),
         InlineKeyboardButton("MSA QUALITY", callback_data='MSA_QUALITY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Pilih bagian Laporan lainnya untuk ditampilkan:", reply_markup=reply_markup)

# --- Callback: Handle Section ---
async def handle_section_crop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    section = query.data
    crop_box = SECTION_COORDINATES.get(section)

    if not crop_box:
        await query.edit_message_text("Section tidak ditemukan. Silakan coba lagi.")
        return

    # Edit pesan lama untuk hilangkan tombol (biar tidak bisa diklik ulang)
    await query.edit_message_text(f"Memuat Laporan: *{section.replace('_', ' ')}*", parse_mode="Markdown")

    # Ambil dan kirim gambar
    path = await get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, f"{section}.png", crop_box)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=f, caption=section.replace("_", " "))
        os.remove(path)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text="Gagal memuat laporan. Silahkan coba lagi.")

    # Kirim ulang pilihan section (di pesan baru)
    keyboard = [
        [InlineKeyboardButton("FULL DASHBOARD", callback_data='FULL_DASHBOARD')],
        [InlineKeyboardButton("FULFILLMENT FBB", callback_data='FULFILLMENT_FBB'),
         InlineKeyboardButton("ASSURANCE FBB", callback_data='ASSURANCE_FBB')],
        [InlineKeyboardButton("SCORE CREDIT", callback_data='SCORE_CREDIT'),
         InlineKeyboardButton("FULFILLMENT BGES", callback_data='FULFILLMENT_BGES')],
        [InlineKeyboardButton("ASSURANCE BGES", callback_data='ASSURANCE_BGES'),
         InlineKeyboardButton("MSA ASSURANCE", callback_data='MSA_ASSURANCE')],
        [InlineKeyboardButton("MSA CNOP", callback_data='MSA_CNOP'),
         InlineKeyboardButton("MSA QUALITY", callback_data='MSA_QUALITY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Pilih bagian Laporan lainnya untuk ditampilkan:",
        reply_markup=reply_markup
    )

# --- Command: /pilaten ---
CROP_PILATEN = (480, 80, 1700, 1020)
async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Memuat Laporan PI LATEN.\nMohon Tunggu Sebentar.")

    path = await get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "pilaten.png", CROP_PILATEN)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="Laporan PI LATEN")
        os.remove(path)
    else:
        await update.message.reply_text("Gagal mengambil gambar PI LATEN. Mohon coba lagi.")

# --- Auto Job Scheduler ---
async def send_all_snapshots(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(TIMEZONE).strftime("%d-%m-%Y %H:%M")

    # MSA/WSA
    path1 = await get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png", SECTION_COORDINATES["FULL_DASHBOARD"])
    if path1 and os.path.exists(path1):
        with open(path1, "rb") as f:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=f,
                caption=f"Laporan MSA/WSA\n🕘 {now}"
            )
        os.remove(path1)
    else:
        logger.error("Gagal kirim snapshot MSA/WSA. Coba lagi nanti.")

    await asyncio.sleep(5)

    # PI LATEN
    path2 = await get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png", CROP_PILATEN)
    if path2 and os.path.exists(path2):
        with open(path2, "rb") as f:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=f,
                caption=f"Laporan PI LATEN\n🕘 {now}"
            )
        os.remove(path2)
    else:
        logger.error("Gagal kirim snapshot PI LATEN. Coba lagi nanti.")

# --- Main Bot ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("msawsa", msawsa))
    app.add_handler(CommandHandler("pilaten", pilaten))
    app.add_handler(CallbackQueryHandler(handle_section_crop))

    job_queue = app.job_queue
    job_queue.run_daily(send_all_snapshots, time=dt_time(9, 0, tzinfo=TIMEZONE))
    job_queue.run_daily(send_all_snapshots, time=dt_time(21, 0, tzinfo=TIMEZONE))

    logger.info("✅ Bot dimulai...")
    app.run_polling()

if __name__ == "__main__":
    main()
