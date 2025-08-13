# import os
# import logging
# from datetime import datetime
# from telegram import Update
# from telegram.ext import ContextTypes
# import config 
# import utils

# logger = logging.getLogger(__name__)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     now = datetime.now(config.TIMEZONE)
#     hour = now.hour

#     if 5 <= hour < 12:
#         greeting = "Selamat pagi"
#     elif 12 <= hour < 15:
#         greeting = "Selamat siang"
#     elif 15 <= hour < 18:
#         greeting = "Selamat sore"
#     else:
#         greeting = "Selamat malam"

#     await update.message.reply_text(
#         f"Halo, {greeting}!\n\n"
#         "Silakan pilih laporan yang ingin anda tampilkan:\n\n"
#         "/msawsa - Laporan MSA/WSA\n"
#         "/pilaten - Laporan PI LATEN\n\n"
#         "📊 ASSURANCE\n"
#         "/monitoring_ticket - Monitoring Ticket\n"
#         "/closed_ticket - Closed Ticket\n"
#         "/unspec - UNSPEC\n\n"
#         "🔧 PROVISIONING\n"
#         "/funneling - Funneling\n"
#         "/detail_kendala_psb - Detail Kendala PSB\n"
#         "/detail_wo - Detail WO\n\n"
#         "🏢 INDBIZ\n"
#         "/funneling_indbiz - Funneling INDBIZ\n"
#         "/detail_kendala_indbiz - Detail Kendala INDBIZ\n"
#         "/detail_wo_indbiz - Detail WO INDBIZ\n\n"
#         "🏬 B2B\n"
#         "/monitoring_ticket_b2b - Monitoring Ticket B2B\n"
#         "/performance - Performance\n\n"
#         "📱 IMJAS\n"
#         "/imjas - IM3AS Dashboard"
#     )

# # Command handler for MSA/WSA
# async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Memuat Laporan MSA/WSA.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, "msawsa.png", config.CROP_MSAWSA)
#     if path and os.path.exists(path):
#         with open(path, "rb") as f:
#             await update.message.reply_photo(f, caption="📊 Laporan MSA/WSA")
#         os.remove(path)
#     else:
#         await update.message.reply_text("❌ Gagal menampilkan laporan MSA/WSA.\nMohon coba lagi.")

# # Command handler for Pilaten
# async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Memuat Laporan PI LATEN.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PILATEN_URL, "pilaten.png", config.CROP_PILATEN)
#     if path and os.path.exists(path):
#         with open(path, "rb") as f:
#             await update.message.reply_photo(f, caption="📊 Laporan PI LATEN")
#         os.remove(path)
#     else:
#         await update.message.reply_text("❌ Gagal menampilkan laporan PI LATEN.\nMohon coba lagi.")

# # command handler for monitoring ticket
# async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🔧 Monitoring command dipanggil")
#     await update.message.reply_text("Memuat Laporan Monitoring Ticket.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         logger.info("🔧 Mulai screenshot monitoring dengan crop")
#         # Gunakan crop monitoring yang sudah didefinisikan
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MONITORING, "monitoring.png", config.CROP_MONITORING)
        
#         if path and os.path.exists(path):
#             logger.info(f"🔧 Screenshot berhasil: {path}")
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="📊 Laporan Monitoring")
#             os.remove(path)
#             logger.info("🔧 Monitoring command selesai")
#         else:
#             logger.error("🔧 Screenshot gagal atau file tidak ada")
#             await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🔧 Error di monitoring handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring.\nMohon coba lagi.")

# # ASSURANCE Handlers
# async def closed_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("📋 Closed Ticket command dipanggil")
#     await update.message.reply_text("Memuat Laporan Closed Ticket.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_CLOSED_TICKET, "closed_ticket.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="📋 Laporan Closed Ticket")
#             os.remove(path)
#             logger.info("📋 Closed Ticket command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Closed Ticket.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"📋 Error di closed ticket handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Closed Ticket.\nMohon coba lagi.")

# async def unspec(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("⚠️ UNSPEC command dipanggil")
#     await update.message.reply_text("Memuat Laporan UNSPEC.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_UNSPEC, "unspec.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="⚠️ Laporan UNSPEC")
#             os.remove(path)
#             logger.info("⚠️ UNSPEC command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan UNSPEC.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"⚠️ Error di UNSPEC handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan UNSPEC.\nMohon coba lagi.")

# # PROVISIONING Handlers
# async def funneling(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🔄 Funneling command dipanggil")
#     await update.message.reply_text("Memuat Laporan Funneling.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_FUNNELING, "funneling.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="🔄 Laporan Funneling")
#             os.remove(path)
#             logger.info("🔄 Funneling command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Funneling.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🔄 Error di Funneling handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Funneling.\nMohon coba lagi.")

# async def detail_kendala_psb(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🔧 Detail Kendala PSB command dipanggil")
#     await update.message.reply_text("Memuat Laporan Detail Kendala PSB.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_KENDALA_PSB, "detail_kendala_psb.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="🔧 Laporan Detail Kendala PSB")
#             os.remove(path)
#             logger.info("🔧 Detail Kendala PSB command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala PSB.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🔧 Error di Detail Kendala PSB handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala PSB.\nMohon coba lagi.")

# async def detail_wo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("📝 Detail WO command dipanggil")
#     await update.message.reply_text("Memuat Laporan Detail WO.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_WO, "detail_wo.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="📝 Laporan Detail WO")
#             os.remove(path)
#             logger.info("📝 Detail WO command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"📝 Error di Detail WO handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO.\nMohon coba lagi.")

# # INDBIZ Handlers
# async def funneling_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🏢 Funneling INDBIZ command dipanggil")
#     await update.message.reply_text("Memuat Laporan Funneling INDBIZ.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_FUNNELING_INDBIZ, "funneling_indbiz.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="🏢 Laporan Funneling INDBIZ")
#             os.remove(path)
#             logger.info("🏢 Funneling INDBIZ command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Funneling INDBIZ.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🏢 Error di Funneling INDBIZ handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Funneling INDBIZ.\nMohon coba lagi.")

# async def detail_kendala_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🏢 Detail Kendala INDBIZ command dipanggil")
#     await update.message.reply_text("Memuat Laporan Detail Kendala INDBIZ.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ, "detail_kendala_indbiz.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="🏢 Laporan Detail Kendala INDBIZ")
#             os.remove(path)
#             logger.info("🏢 Detail Kendala INDBIZ command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala INDBIZ.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🏢 Error di Detail Kendala INDBIZ handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala INDBIZ.\nMohon coba lagi.")

# async def detail_wo_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🏢 Detail WO INDBIZ command dipanggil")
#     await update.message.reply_text("Memuat Laporan Detail WO INDBIZ.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_WO_INDBIZ, "detail_wo_indbiz.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="🏢 Laporan Detail WO INDBIZ")
#             os.remove(path)
#             logger.info("🏢 Detail WO INDBIZ command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO INDBIZ.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🏢 Error di Detail WO INDBIZ handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO INDBIZ.\nMohon coba lagi.")

# # B2B Handlers
# async def monitoring_ticket_b2b(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("🏬 Monitoring Ticket B2B command dipanggil")
#     await update.message.reply_text("Memuat Laporan Monitoring Ticket B2B.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MONITORING_TICKET_B2B, "monitoring_ticket_b2b.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="🏬 Laporan Monitoring Ticket B2B")
#             os.remove(path)
#             logger.info("🏬 Monitoring Ticket B2B command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket B2B.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"🏬 Error di Monitoring Ticket B2B handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket B2B.\nMohon coba lagi.")

# async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("📊 Performance command dipanggil")
#     await update.message.reply_text("Memuat Laporan Performance.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PERFORMANCE, "performance.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="📊 Laporan Performance")
#             os.remove(path)
#             logger.info("📊 Performance command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan laporan Performance.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"📊 Error di Performance handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan laporan Performance.\nMohon coba lagi.")

# # IM3AS Handler
# async def im3as(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("📱 IM3AS command dipanggil")
#     await update.message.reply_text("Memuat Dashboard IM3AS.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

#     try:
#         path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_IM3AS, "im3as.png", config.CROP_DEFAULT)
        
#         if path and os.path.exists(path):
#             with open(path, "rb") as f:
#                 await update.message.reply_photo(f, caption="📱 Dashboard IM3AS")
#             os.remove(path)
#             logger.info("📱 IM3AS command selesai")
#         else:
#             await update.message.reply_text("❌ Gagal menampilkan Dashboard IM3AS.\nMohon coba lagi.")
#     except Exception as e:
#         logger.error(f"📱 Error di IM3AS handler: {e}")
#         await update.message.reply_text("❌ Gagal menampilkan Dashboard IM3AS.\nMohon coba lagi.")

