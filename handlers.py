import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime

import config
import utils

# --- Command: /start ---
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
    "Silakan pilih laporan yang ingin anda tampilkan:\n"
    "/msawsa - Laporan MSA/WSA\n"
    "/pilaten - Laporan PI LATEN\n"
    "/fulfillment_fbb - Laporan FULFILLMENT FBB\n"
    "/assurance_fbb - Laporan ASSURANCE FBB\n"
    "/score_credit - Laporan SCORE CREDIT\n"
    "/fulfillment_bges - Laporan FULFILLMENT BGES\n"
    "/assurance_bges - Laporan ASSURANCE BGES\n"
    "/msa_assurance - Laporan MSA ASSURANCE\n"
    "/msa_cnop - Laporan MSA CNOP\n"
    "/msa_quality - Laporan MSA QUALITY"
)
    
# --- Command: /msawsa ---
async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Memuat Laporan MSA/WSA.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, "full_dashboard.png", config.SECTION_COORDINATES["FULL_DASHBOARD"])
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="📊 Laporan MSA/WSA")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal menampilkan laporan MSA/WSA.\nMohon coba lagi.")

    # Menu 2 kolom
    keyboard = [
        [InlineKeyboardButton("FULFILLMENT_FBB", callback_data='FULFILLMENT_FBB'),
         InlineKeyboardButton("ASSURANCE_FBB", callback_data='ASSURANCE_FBB')],
        [InlineKeyboardButton("SCORE CREDIT", callback_data='SCORE_CREDIT'),
         InlineKeyboardButton("FULFILLMENT BGES", callback_data='FULFILLMENT_BGES')],
        [InlineKeyboardButton("ASSURANCE BGES", callback_data='ASSURANCE_BGES'),
         InlineKeyboardButton("MSA ASSURANCE", callback_data='MSA_ASSURANCE')],
        [InlineKeyboardButton("MSA CNOP", callback_data='MSA_CNOP'),
         InlineKeyboardButton("MSA QUALITY", callback_data='MSA_QUALITY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Pilih bagian Laporan lainnya untuk ditampilkan:", reply_markup=reply_markup)

# --- Callback: Handle Section ---
async def handle_section_crop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    section = query.data
    crop_box = config.SECTION_COORDINATES.get(section)

    if not crop_box:
        await query.edit_message_text("Section tidak ditemukan. Silakan coba lagi.")
        return

    # Edit pesan lama untuk hilangkan tombol (biar tidak bisa diklik ulang)
    await query.edit_message_text(f"Memuat Laporan: *{section.replace('_', ' ')}*", parse_mode="Markdown")

    # Ambil dan kirim gambar
    path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, f"{section}.png", crop_box)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=f, caption=section.replace("_", " "))
        os.remove(path)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text="❌ Gagal memuat laporan. Silahkan coba lagi.")

    # Kirim ulang pilihan section (di pesan baru)
    keyboard = [
        [InlineKeyboardButton("FULL DASHBOARD", callback_data='FULL_DASHBOARD')],
        [InlineKeyboardButton("FULFILLMENT FBB", callback_data='FULFILLMENT_FBB'),
         InlineKeyboardButton("ASSURANCE FBB", callback_data='ASSURANCE_FBB')],
        [InlineKeyboardButton("SCORE CREDIT", callback_data='SCORE_CREDIT'),
         InlineKeyboardButton("FULFILLMENT BGES", callback_data='FULFILLMENT_BGES')],
        [InlineKeyboardButton("ASSURANCE BGES", callback_data='ASSURANCE_BGES'),
         InlineKeyboardButton("MSA ASSURANCE", callback_data='MSA_ASSURANCE')],
        [InlineKeyboardButton("MSA CNOP", callback_data='MSA_CNOP'),
         InlineKeyboardButton("MSA QUALITY", callback_data='MSA_QUALITY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Pilih bagian Laporan lainnya untuk ditampilkan:",
        reply_markup=reply_markup
    )

# --- Command: /pilaten ---
# CROP_PILATEN = (480, 80, 1700, 1020)
async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Memuat Laporan PI LATEN.\nMohon Tunggu Sebentar.")

    path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PILATEN_URL, "pilaten.png", config.CROP_PILATEN)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="📊 Laporan PI LATEN")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal mengambil gambar PI LATEN. Mohon coba lagi.")

# command untuk per section
async def send_section_image(update: Update, context: ContextTypes.DEFAULT_TYPE, section_key: str, section_name: str):
    await update.message.reply_text(f"Memuat Laporan {section_name}...\nMohon tunggu sebentar.")
    path = await utils.get_looker_studio_screenshot(
        config.LOOKER_STUDIO_MSA_WSA_URL,
        f"{section_key}.png",
        config.SECTION_COORDINATES[section_key]
    )
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption=f"📊 Laporan {section_name}")
        os.remove(path)
    else:
        await update.message.reply_text(f"❌ Gagal memuat laporan {section_name}.")

# Berikut fungsi shortcut untuk tiap command
async def fulfillment_fbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "FULFILLMENT_FBB", "FULFILLMENT FBB")

async def assurance_fbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "ASSURANCE_FBB", "ASSURANCE FBB")

async def score_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "SCORE_CREDIT", "SCORE CREDIT")

async def fulfillment_bges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "FULFILLMENT_BGES", "FULFILLMENT BGES")

async def assurance_bges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "ASSURANCE_BGES", "ASSURANCE BGES")

async def msa_assurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "MSA_ASSURANCE", "MSA ASSURANCE")

async def msa_cnop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "MSA_CNOP", "MSA CNOP")

async def msa_quality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_section_image(update, context, "MSA_QUALITY", "MSA QUALITY")