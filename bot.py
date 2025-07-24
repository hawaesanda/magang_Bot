import os
import logging
import pytz
import asyncio
from datetime import time as dt_time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from playwright.async_api import async_playwright
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- Konfigurasi ---
TOKEN = "7941038639:AAGOUrsa05AbgV46g-WmLszUig26Fd-tIDk"

LOOKER_STUDIO_MSA_WSA_URL = "https://lookerstudio.google.com/reporting/c3dde9be-7050-40d9-b9b0-ebcaf65ac573"
LOOKER_STUDIO_PILATEN_URL = "https://lookerstudio.google.com/s/s2yRKBhqWME"

TARGET_CHAT_ID = "1003337187"
TIMEZONE = pytz.timezone("Asia/Jakarta")

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Fungsi Screenshot Pakai Playwright ---
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str) -> str | None:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            page.set_default_timeout(90000)

            logger.info(f"Membuka URL: {looker_studio_url}")
            await page.goto(looker_studio_url, timeout=90000, wait_until="networkidle")

            # Tunggu halaman termuat sepenuhnya
            await page.wait_for_timeout(5000)
            
            # Scroll ke bawah untuk memuat konten lazy-loaded
            await page.evaluate("""
                async () => {
                    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                    
                    // Get total height
                    const totalHeight = Math.max(
                        document.body.scrollHeight,
                        document.body.offsetHeight,
                        document.documentElement.clientHeight,
                        document.documentElement.scrollHeight,
                        document.documentElement.offsetHeight
                    );
                    
                    const viewportHeight = window.innerHeight;
                    let currentPosition = 0;
                    
                    // Scroll gradually to load all content
                    while (currentPosition < totalHeight) {
                        window.scrollTo(0, currentPosition);
                        await delay(1000); // Wait for content to load
                        currentPosition += viewportHeight;
                    }
                    
                    // Scroll to bottom to ensure everything is loaded
                    window.scrollTo(0, totalHeight);
                    await delay(2000);
                    
                    // Scroll back to top for final screenshot
                    window.scrollTo(0, 0);
                    await delay(1000);
                }
            """)
            
            # Tunggu setelah scroll untuk memastikan konten termuat
            await page.wait_for_timeout(3000)

            # Screenshot seluruh halaman
            await page.screenshot(path=output_filename, full_page=True, timeout=60000)

            await browser.close()

        return output_filename
    except Exception as e:
        logger.error(f"❌ Gagal mengambil screenshot pakai Playwright: {e}")
        return None

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Berikut daftar perintah:\n"
        "/msawsa - Kirim snapshot dashboard MSA/WSA\n"
        "/pilaten - Kirim snapshot dashboard PI LATEN"
    )

async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Sedang mengambil snapshot dashboard MSA/WSA...")
    path = await get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "msawsa.png")
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="Laporan MSA/WSA")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal mengambil screenshot dashboard MSA/WSA.")

async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Sedang mengambil snapshot dashboard PI LATEN...")
    path = await get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "pilaten.png")
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="Laporan PI LATEN")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal mengambil screenshot dashboard PI LATEN.")

# --- Kirim Otomatis Gabungan ---
async def send_all_snapshots(context: ContextTypes.DEFAULT_TYPE):
    # --- MSA/WSA ---
    path1 = await get_looker_studio_screenshot(LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png")
    if path1 and os.path.exists(path1):
        with open(path1, "rb") as f:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=f,
                caption="🔔 Snapshot (Otomatis) MSA/WSA"
            )
        os.remove(path1)
    else:
        logger.error("❌ Gagal kirim otomatis MSA/WSA")

    await asyncio.sleep(5)

    # --- PI LATEN ---
    path2 = await get_looker_studio_screenshot(LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png")
    if path2 and os.path.exists(path2):
        with open(path2, "rb") as f:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=f,
                caption="🔔 Snapshot (Otomatis) PI LATEN"
            )
        os.remove(path2)
    else:
        logger.error("❌ Gagal kirim otomatis PI LATEN")

# --- Fungsi Utama ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("msawsa", msawsa))
    app.add_handler(CommandHandler("pilaten", pilaten))

    job_queue = app.job_queue
    time_morning = dt_time(9, 0, tzinfo=TIMEZONE)
    time_evening = dt_time(21, 0, tzinfo=TIMEZONE)

    job_queue.run_daily(send_all_snapshots, time=time_morning)
    job_queue.run_daily(send_all_snapshots, time=time_evening)

    logger.info("Bot dimulai dengan jadwal otomatis.")
    app.run_polling()

if __name__ == "__main__":
    main()
