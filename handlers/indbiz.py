import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def funneling_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Funneling INDBIZ command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Funneling INDBIZ.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_FUNNELING_INDBIZ,
        filename="funneling_indbiz.png",
        crop_box=config.CROP_DEFAULT,
        caption="🏢 Laporan Funneling INDBIZ"
    )
    
    if success:
        logger.info("🏢 Funneling INDBIZ command selesai")
    else:
        logger.error("🏢 Funneling INDBIZ command gagal")

async def detail_kendala_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Detail Kendala INDBIZ command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Detail Kendala INDBIZ.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ,
        filename="detail_kendala_indbiz.png",
        crop_box=config.CROP_DEFAULT,
        caption="🏢 Laporan Detail Kendala INDBIZ"
    )
    
    if success:
        logger.info("🏢 Detail Kendala INDBIZ command selesai")
    else:
        logger.error("🏢 Detail Kendala INDBIZ command gagal")

async def detail_wo_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Detail WO INDBIZ command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Detail WO INDBIZ.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_DETAIL_WO_INDBIZ,
        filename="detail_wo_indbiz.png",
        crop_box=config.CROP_DEFAULT,
        caption="🏢 Laporan Detail WO INDBIZ"
    )
    
    if success:
        logger.info("🏢 Detail WO INDBIZ command selesai")
    else:
        logger.error("🏢 Detail WO INDBIZ command gagal")
