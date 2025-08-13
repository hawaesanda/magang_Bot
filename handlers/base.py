import logging
import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
import config
import scheduler
from utils import get_looker_studio_screenshot

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(config.TIMEZONE)
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
        "Silakan pilih laporan yang ingin anda tampilkan:\n\n"
        "/msawsa - Laporan MSA/WSA\n"
        "/pilaten - Laporan PI LATEN\n\n"
        "📊 ASSURANCE\n"
        "/monitoring_ticket - Monitoring Ticket\n"
        "/closed_ticket - Closed Ticket\n"
        "/unspec - UNSPEC\n\n"
        "🔧 PROVISIONING\n"
        "/funneling - Funneling\n"
        "/detail_kendala_psb - Detail Kendala PSB\n"
        "/detail_wo - Detail WO\n\n"
        "🏢 INDBIZ\n"
        "/funneling_indbiz - Funneling INDBIZ\n"
        "/detail_kendala_indbiz - Detail Kendala INDBIZ\n"
        "/detail_wo_indbiz - Detail WO INDBIZ\n\n"
        "🏬 B2B\n"
        "/monitoring_ticket_b2b - Monitoring Ticket B2B\n"
        "/performance - Performance\n\n"
        "📱 IMJAS\n"
        "/imjas - IMJAS Dashboard\n\n"
        "🧪 TEST COMMANDS\n"
        "/test_scheduler - Test Scheduler Manual"
    )

async def test_scheduler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test command untuk menjalankan scheduler secara manual"""
    logger.info("🧪 Test scheduler command dipanggil")
    await update.message.reply_text("🧪 Menjalankan test scheduler...\nMohon tunggu...")
    
    try:
        await scheduler.test_manual_snapshots(context)
        await update.message.reply_text("✅ Test scheduler selesai! Cek chat target untuk melihat hasilnya.")
    except Exception as e:
        logger.error(f"💥 Error dalam test scheduler: {e}")
        await update.message.reply_text(f"❌ Test scheduler gagal: {str(e)}")

async def handle_screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                   url: str, filename: str, crop_config: dict, caption: str, 
                                   loading_text: str = None):
    """
    Template function untuk menangani semua command screenshot dengan loading message yang bisa dihapus
    """
    if loading_text is None:
        loading_text = f"Memuat {caption}.\nMohon Tunggu Sebentar..."
    
    loading_msg = await update.message.reply_text(loading_text, parse_mode="Markdown")

    try:
        path = await get_looker_studio_screenshot(url, filename, crop_config)
        
        if path and os.path.exists(path):
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption=caption)
            os.remove(path)
            logger.info(f"✅ {caption} berhasil dikirim")
        else:
            await loading_msg.delete()
            await update.message.reply_text(f"❌ Gagal menampilkan {caption.lower()}.\nMohon coba lagi.")
            logger.error(f"❌ Gagal screenshot {caption}")
    except Exception as e:
        logger.error(f"❌ Error di {caption} handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Gagal menampilkan {caption.lower()}.\nMohon coba lagi.")
