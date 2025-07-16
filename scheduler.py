import os
import asyncio
import logging
from datetime import datetime
import config
import utils

logger = logging.getLogger(__name__)

async def scheduled_snapshots(context):
    now = datetime.now(config.TIMEZONE).strftime("%d-%m-%Y %H:%M")
    logger.info(f"⏰ Mengirim snapshot otomatis... [{now}]")

    # MSA/WSA
    path1 = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png", config.CROP_MSA_WSA)
    if path1 and os.path.exists(path1):
        with open(path1, "rb") as f:
            await context.bot.send_photo(chat_id=config.TARGET_CHAT_ID, photo=f, caption=f"📊 Laporan MSA/WSA\n🕘 {now}")
        os.remove(path1)
    else:
        logger.error("❌ Gagal kirim snapshot MSA/WSA.")

    await asyncio.sleep(5)

    # PI LATEN
    path2 = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png", config.CROP_PILATEN)
    if path2 and os.path.exists(path2):
        with open(path2, "rb") as f:
            await context.bot.send_photo(chat_id=config.TARGET_CHAT_ID, photo=f, caption=f"📊 Laporan PI LATEN\n🕘 {now}")
        os.remove(path2)
    else:
        logger.error("❌ Gagal kirim snapshot PI LATEN.")
