import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def funneling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔄 Funneling command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Funneling.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_FUNNELING,
        filename="funneling.png",
        crop_box=config.CROP_DEFAULT,
        caption="🔄 Laporan Funneling"
    )
    
    if success:
        logger.info("🔄 Funneling command selesai")
    else:
        logger.error("🔄 Funneling command gagal")

async def detail_kendala_psb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔧 Detail Kendala PSB command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Detail Kendala PSB.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_DETAIL_KENDALA_PSB,
        filename="detail_kendala_psb.png",
        crop_box=config.CROP_DEFAULT,
        caption="🔧 Laporan Detail Kendala PSB"
    )
    
    if success:
        logger.info("🔧 Detail Kendala PSB command selesai")
    else:
        logger.error("🔧 Detail Kendala PSB command gagal")

async def detail_wo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📝 Detail WO command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Detail WO.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_DETAIL_WO,
        filename="detail_wo.png",
        crop_box=config.CROP_DEFAULT,
        caption="📝 Laporan Detail WO"
    )
    
    if success:
        logger.info("📝 Detail WO command selesai")
    else:
        logger.error("📝 Detail WO command gagal")
