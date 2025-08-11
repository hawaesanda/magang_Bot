import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

# Command handler for monitoring ticket
async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔧 Monitoring command dipanggil")
    loading_msg = await update.message.reply_text("Memuat Laporan Monitoring Ticket.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info("🔧 Mulai screenshot monitoring ticket dengan fungsi khusus")
        # Gunakan fungsi khusus monitoring ticket
        path = await utils.take_monitoring_ticket_screenshot("monitoring_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"🔧 Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📊 Laporan Monitoring Ticket")
            os.remove(path)
            logger.info("🔧 Monitoring command selesai")
        else:
            logger.error("🔧 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🔧 Error di monitoring handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket.\nMohon coba lagi.")

async def closed_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📋 Closed Ticket command dipanggil")
    loading_msg = await update.message.reply_text("Memuat Laporan Closed Ticket.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info("📋 Mulai screenshot closed ticket dengan fungsi khusus")
        # Gunakan fungsi khusus closed ticket
        path = await utils.take_closed_ticket_screenshot("closed_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"📋 Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📋 Laporan Closed Ticket")
            os.remove(path)
            logger.info("📋 Closed Ticket command selesai")
        else:
            logger.error("📋 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan laporan Closed Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📋 Error di closed ticket handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan laporan Closed Ticket.\nMohon coba lagi.")

async def unspec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("⚠️ UNSPEC command dipanggil")
    loading_msg = await update.message.reply_text("Memuat Laporan UNSPEC.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info("⚠️ Mulai screenshot unspec dengan fungsi khusus")
        # Gunakan fungsi khusus unspec
        path = await utils.take_unspec_screenshot("unspec.png")
        
        if path and os.path.exists(path):
            logger.info(f"⚠️ Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="⚠️ Laporan UNSPEC")
            os.remove(path)
            logger.info("⚠️ UNSPEC command selesai")
        else:
            logger.error("⚠️ Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan laporan UNSPEC.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"⚠️ Error di UNSPEC handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan laporan UNSPEC.\nMohon coba lagi.")
