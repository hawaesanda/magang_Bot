import os
import logging
import asyncio
from datetime import datetime, time as dt_time
from telegram.ext import ContextTypes
import config
import utils

logger = logging.getLogger(__name__)

# Cek waktu kerja
def is_within_working_hours():
    now = datetime.now(config.TIMEZONE).time()
    return dt_time(10, 0) <= now <= dt_time(17, 0)

# Job yang hanya jalan di jam kerja otomatis
async def scheduled_snapshots(context: ContextTypes.DEFAULT_TYPE):
    if is_within_working_hours():
        logger.info("⏰ Dalam jam kerja, mengirim snapshot otomatis...")
        await send_all_snapshots(context)
    else:
        logger.info("⏸️ Di luar jam kerja, tidak mengirim snapshot.")

# --- Auto Job Scheduler ---
async def send_all_snapshots(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(config.TIMEZONE).strftime("%d-%m-%Y %H:%M")

    # MSA/WSA
    path1 = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png", config.SECTION_COORDINATES["FULL_DASHBOARD"])
    if path1 and os.path.exists(path1):
        with open(path1, "rb") as f:
            await context.bot.send_photo(
                chat_id=config.TARGET_CHAT_ID,
                photo=f,
                caption=f"📊 Laporan MSA/WSA\n🕘 {now}"
            )
        os.remove(path1)
    else:
        logger.error("❌ Gagal kirim snapshot MSA/WSA. Coba lagi nanti.")

    await asyncio.sleep(5)

    # PI LATEN
    path2 = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png", config.CROP_PILATEN)
    if path2 and os.path.exists(path2):
        with open(path2, "rb") as f:
            await context.bot.send_photo(
                chat_id=config.TARGET_CHAT_ID,
                photo=f,
                caption=f"📊 Laporan PI LATEN\n🕘 {now}"
            )
        os.remove(path2)
    else:
        logger.error("❌ Gagal kirim snapshot PI LATEN. Coba lagi nanti.")