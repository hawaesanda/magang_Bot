import os
import asyncio
import logging
from datetime import datetime
import config
import utils

logger = logging.getLogger(__name__)

async def get_screenshot_with_retry(url, filename, crop, max_retries=2):
    for attempt in range(max_retries):
        try:
            path = await utils.get_looker_studio_screenshot(url, filename, crop)
            if path and os.path.exists(path):
                return path
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(10)  # Wait 10 seconds before retry
    return None

async def scheduled_snapshots(context):
    now = datetime.now(config.TIMEZONE).strftime("%d-%m-%Y %H:%M")
    logger.info(f"⏰ Mengirim snapshot otomatis... [{now}]")

    try:
        # MSA/WSA - Ganti ke retry mechanism
        logger.info("📊 Mulai screenshot MSA/WSA")
        path1 = await get_screenshot_with_retry(config.LOOKER_STUDIO_MSA_WSA_URL, "auto_msawsa.png", config.CROP_MSAWSA)
        if path1 and os.path.exists(path1):
            # Kirim ke semua chat ID
            for chat_id in config.TARGET_CHAT_IDS:
                try:
                    with open(path1, "rb") as f:
                        await context.bot.send_photo(chat_id=chat_id, photo=f, caption=f"📊 Laporan MSA/WSA\n🕘 {now}")
                    logger.info(f"✅ MSA/WSA berhasil dikirim ke chat {chat_id}")
                except Exception as e:
                    logger.error(f"❌ Gagal kirim MSA/WSA ke chat {chat_id}: {e}")
            os.remove(path1)
        else:
            logger.error("❌ Gagal kirim snapshot MSA/WSA.")

        await asyncio.sleep(5)

        # PI LATEN - Sudah benar menggunakan retry
        # logger.info("📊 Mulai screenshot PI LATEN")
        # path2 = await get_screenshot_with_retry(config.LOOKER_STUDIO_PILATEN_URL, "auto_pilaten.png", config.CROP_PILATEN)
        # if path2 and os.path.exists(path2):
        #     # Kirim ke semua chat ID
        #     for chat_id in config.TARGET_CHAT_IDS:
        #         try:
        #             with open(path2, "rb") as f:
        #                 await context.bot.send_photo(chat_id=chat_id, photo=f, caption=f"📊 Laporan PI LATEN\n🕘 {now}")
        #             logger.info(f"✅ PI LATEN berhasil dikirim ke chat {chat_id}")
        #         except Exception as e:
        #             logger.error(f"❌ Gagal kirim PI LATEN ke chat {chat_id}: {e}")
        #     os.remove(path2)
        # else:
        #     logger.error("❌ Gagal kirim snapshot PI LATEN.")
            
        # logger.info(f"🎉 Scheduled snapshots selesai pada {now}")
        
    except Exception as e:
        logger.error(f"💥 Error dalam scheduled_snapshots: {e}")
        try:
            # Kirim error message ke semua chat ID
            for chat_id in config.TARGET_CHAT_IDS:
                try:
                    await context.bot.send_message(
                        chat_id=chat_id, 
                        text=f"❌ Error dalam pengiriman otomatis pada {now}:\n{str(e)}"
                    )
                except Exception as send_error:
                    logger.error(f"💥 Gagal mengirim error message ke chat {chat_id}: {send_error}")
        except Exception as send_error:
            logger.error(f"💥 Gagal mengirim error message: {send_error}")

# Test function untuk debugging
async def test_manual_snapshots(context):
    """Test function untuk menjalankan snapshot secara manual"""
    logger.info("🧪 Testing manual snapshots...")
    logger.info(f"📋 Target Chat IDs: {config.TARGET_CHAT_IDS}")
    await scheduled_snapshots(context)
