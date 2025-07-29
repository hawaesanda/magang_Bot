import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
import config
import scheduler

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
        "📱 IM3AS\n"
        "/im3as - IM3AS Dashboard\n\n"
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
