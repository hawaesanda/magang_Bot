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

    try:
        # MSA/WSA
        logger.info("📊 Mulai screenshot MSA/WSA")
        path1 = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png", config.CROP_MSAWSA)
        if path1 and os.path.exists(path1):
            with open(path1, "rb") as f:
                await context.bot.send_photo(chat_id=config.TARGET_CHAT_ID, photo=f, caption=f"📊 Laporan MSA/WSA\n🕘 {now}")
            os.remove(path1)
            logger.info("✅ MSA/WSA berhasil dikirim")
        else:
            logger.error("❌ Gagal kirim snapshot MSA/WSA.")

        await asyncio.sleep(5)

        # PI LATEN
        logger.info("📊 Mulai screenshot PI LATEN")
        path2 = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png", config.CROP_PILATEN)
        if path2 and os.path.exists(path2):
            with open(path2, "rb") as f:
                await context.bot.send_photo(chat_id=config.TARGET_CHAT_ID, photo=f, caption=f"📊 Laporan PI LATEN\n🕘 {now}")
            os.remove(path2)
            logger.info("✅ PI LATEN berhasil dikirim")
        else:
            logger.error("❌ Gagal kirim snapshot PI LATEN.")
            
        logger.info(f"🎉 Scheduled snapshots selesai pada {now}")
        
    except Exception as e:
        logger.error(f"💥 Error dalam scheduled_snapshots: {e}")
        try:
            await context.bot.send_message(
                chat_id=config.TARGET_CHAT_ID, 
                text=f"❌ Error dalam pengiriman otomatis pada {now}:\n{str(e)}"
            )
        except Exception as send_error:
            logger.error(f"💥 Gagal mengirim error message: {send_error}")

# Test function untuk debugging
async def test_manual_snapshots(context):
    """Test function untuk menjalankan snapshot secara manual"""
    logger.info("🧪 Testing manual snapshots...")
    await scheduled_snapshots(context)
