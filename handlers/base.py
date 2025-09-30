import logging
import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

    # Main menu keyboard - hapus test scheduler
    keyboard = [
        [InlineKeyboardButton("📊 MSA/WSA", callback_data="msawsa")],
        [InlineKeyboardButton("🛡️ ASSURANCE", callback_data="menu_assurance")],
        [InlineKeyboardButton("🔧 PROVISIONING", callback_data="menu_provisioning")],
        [InlineKeyboardButton("🏢 INDBIZ", callback_data="menu_indbiz")],
        [InlineKeyboardButton("🏬 B2B", callback_data="menu_b2b")],
        [InlineKeyboardButton("📱 IMJAS", callback_data="imjas")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Halo, {greeting}!\n\n"
        "Silakan pilih kategori laporan yang ingin anda lihat:",
        reply_markup=reply_markup
    )

async def show_assurance_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk kategori Assurance"""
    keyboard = [
        [InlineKeyboardButton("📊 Monitoring Ticket", callback_data="menu_monitoring")],
        [InlineKeyboardButton("✅ Closed Ticket", callback_data="closed_ticket")],
        [InlineKeyboardButton("⚠️ UNSPEC", callback_data="unspec")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🛡️ **ASSURANCE**\n\nPilih laporan yang ingin ditampilkan:"
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_monitoring_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk Monitoring Ticket per HSA"""
    keyboard = [
        [InlineKeyboardButton("📊 All HSA", callback_data="monitoring")],
        [InlineKeyboardButton("🏢 HSA Kepanjen", callback_data="hsa_kepanjen")],
        [InlineKeyboardButton("🏢 HSA Blimbing", callback_data="hsa_blimbing")],
        [InlineKeyboardButton("🏢 HSA Batu", callback_data="hsa_batu")],
        [InlineKeyboardButton("🏢 HSA Klojen", callback_data="hsa_klojen")],
        [InlineKeyboardButton("🏢 HSA Malang", callback_data="hsa_malang")],
        [InlineKeyboardButton("🏢 HSA Singosari", callback_data="hsa_singosari")],
        [InlineKeyboardButton("🏢 HSA Turen", callback_data="hsa_turen")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_assurance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "📊 **MONITORING TICKET**\n\nPilih HSA yang ingin ditampilkan:"
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_provisioning_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk kategori Provisioning"""
    keyboard = [
        [InlineKeyboardButton("📈 Funneling", callback_data="funneling")],
        [InlineKeyboardButton("🔍 Detail Kendala PSB", callback_data="detail_kendala_psb")],
        [InlineKeyboardButton("📋 Detail WO", callback_data="detail_wo")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🔧 **PROVISIONING**\n\nPilih laporan yang ingin ditampilkan:"
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_indbiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk kategori INDBIZ"""
    keyboard = [
        [InlineKeyboardButton("📈 Funneling INDBIZ", callback_data="funneling_indbiz")],
        [InlineKeyboardButton("🔍 Detail Kendala INDBIZ", callback_data="detail_kendala_indbiz")],
        [InlineKeyboardButton("📋 Detail WO INDBIZ", callback_data="detail_wo_indbiz")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🏢 **INDBIZ**\n\nPilih laporan yang ingin ditampilkan:"
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_b2b_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk kategori B2B"""
    keyboard = [
        [InlineKeyboardButton("📊 Monitoring Ticket B2B", callback_data="monitoring_ticket_b2b")],
        [InlineKeyboardButton("📈 Performance", callback_data="performance")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🏬 **B2B**\n\nPilih laporan yang ingin ditampilkan:"
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kembali ke main menu"""
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

    # Main menu keyboard - hapus test scheduler
    keyboard = [
        [InlineKeyboardButton("📊 MSA/WSA", callback_data="msawsa")],
        [InlineKeyboardButton("🛡️ ASSURANCE", callback_data="menu_assurance")],
        [InlineKeyboardButton("🔧 PROVISIONING", callback_data="menu_provisioning")],
        [InlineKeyboardButton("🏢 INDBIZ", callback_data="menu_indbiz")],
        [InlineKeyboardButton("🏬 B2B", callback_data="menu_b2b")],
        [InlineKeyboardButton("📱 IMJAS", callback_data="imjas")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"Halo, {greeting}!\n\nSilakan pilih kategori laporan yang ingin anda lihat:"
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk callback query dari inline keyboard"""
    query = update.callback_query
    await query.answer()

    # Menu navigation
    if query.data == "main_menu":
        await show_main_menu(update, context)
    elif query.data == "menu_assurance":
        await show_assurance_menu(update, context)
    elif query.data == "menu_monitoring":
        await show_monitoring_menu(update, context)
    elif query.data == "menu_provisioning":
        await show_provisioning_menu(update, context)
    elif query.data == "menu_indbiz":
        await show_indbiz_menu(update, context)
    elif query.data == "menu_b2b":
        await show_b2b_menu(update, context)
    
    # Direct actions - hapus test_scheduler dan pilaten
    elif query.data == "msawsa":
        from .reports import msawsa_callback
        await msawsa_callback(update, context)
    elif query.data == "imjas":
        from .imjas import imjas_callback
        await imjas_callback(update, context)
    
    # Assurance actions
    elif query.data == "monitoring":
        from .assurance import monitoring_callback
        await monitoring_callback(update, context)
    elif query.data == "closed_ticket":
        from .assurance import closed_ticket_callback
        await closed_ticket_callback(update, context)
    elif query.data == "unspec":
        from .assurance import unspec_callback
        await unspec_callback(update, context)
    
    # HSA specific
    elif query.data.startswith("hsa_"):
        hsa_name = query.data.replace("hsa_", "")
        from .assurance import hsa_callback
        await hsa_callback(update, context, hsa_name)
    
    # Provisioning actions
    elif query.data == "funneling":
        from .provisioning import funneling_callback
        await funneling_callback(update, context)
    elif query.data == "detail_kendala_psb":
        from .provisioning import detail_kendala_psb_callback
        await detail_kendala_psb_callback(update, context)
    elif query.data == "detail_wo":
        from .provisioning import detail_wo_callback
        await detail_wo_callback(update, context)
    
    # INDBIZ actions
    elif query.data == "funneling_indbiz":
        from .indbiz import funneling_indbiz_callback
        await funneling_indbiz_callback(update, context)
    elif query.data == "detail_kendala_indbiz":
        from .indbiz import detail_kendala_indbiz_callback
        await detail_kendala_indbiz_callback(update, context)
    elif query.data == "detail_wo_indbiz":
        from .indbiz import detail_wo_indbiz_callback
        await detail_wo_indbiz_callback(update, context)
    
    # B2B actions
    elif query.data == "monitoring_ticket_b2b":
        from .b2b import monitoring_ticket_b2b_callback
        await monitoring_ticket_b2b_callback(update, context)
    elif query.data == "performance":
        from .b2b import performance_callback
        await performance_callback(update, context)

async def handle_screenshot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                   url: str, filename: str, crop_config: dict, caption: str, 
                                   loading_text: str = None, back_menu: str = "main_menu"):
    """
    Template function untuk menangani semua callback screenshot dengan tombol kembali di chat terbawah
    """
    if loading_text is None:
        loading_text = f"Memuat {caption}.\nMohon Tunggu Sebentar..."
    
    await update.callback_query.edit_message_text(loading_text)

    try:
        path = await get_looker_studio_screenshot(url, filename, crop_config)
        
        if path and os.path.exists(path):
            # Hapus pesan loading terlebih dahulu
            await update.callback_query.delete_message()
            
            # Kirim foto sebagai pesan baru
            with open(path, "rb") as f:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=f, 
                    caption=caption
                )
            os.remove(path)
            
            # Kirim tombol kembali sebagai pesan terpisah di bawah (chat terbawah)
            keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data=back_menu)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ Laporan berhasil dikirim!\n\nSilakan pilih aksi selanjutnya:",
                reply_markup=reply_markup
            )
            
            logger.info(f"✅ {caption} berhasil dikirim")
        else:
            # Jika gagal, kirim pesan error dengan tombol kembali
            keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data=back_menu)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                f"❌ Gagal menampilkan {caption.lower()}.\nMohon coba lagi.",
                reply_markup=reply_markup
            )
            logger.error(f"❌ Gagal screenshot {caption}")
    except Exception as e:
        logger.error(f"❌ Error di {caption} handler: {e}")
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data=back_menu)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            f"❌ Gagal menampilkan {caption.lower()}.\nMohon coba lagi.",
            reply_markup=reply_markup
        )

# Fungsi test_scheduler dan handle_screenshot_command tetap ada untuk backward compatibility commands

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

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help - menampilkan daftar semua command yang tersedia"""
    await start(update, context)  # Gunakan fungsi start yang sama

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /menu - alias untuk /help"""
    await start(update, context)  # Gunakan fungsi start yang sama
