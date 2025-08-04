import os
import logging
from PIL import Image
from playwright.async_api import async_playwright
from telegram import Update
from telegram.ext import ContextTypes
import config

# Persistent browser instance
persistent_browser = None
logger = logging.getLogger(__name__)

# --- Inisialisasi browser ---
async def init_browser():
    global persistent_browser
    if persistent_browser is None:
        playwright = await async_playwright().start()
        persistent_browser = await playwright.chromium.launch(headless=True)
        logger.info("✅ Persistent browser started.")

# --- Fungsi Crop Gambar ---
def crop_image(input_path: str, output_path: str, crop_box: tuple[int, int, int, int]) -> str:
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            left, top, right, bottom = crop_box

            # Batasi agar tidak melebihi ukuran gambar
            right = min(right, width)
            bottom = min(bottom, height)

            cropped = img.crop((left, top, right, bottom))
            cropped.save(output_path)

        os.remove(input_path)
        return output_path
    except Exception as e:
        logger.error(f"❌ Gagal crop gambar: {e}")
        return input_path

# --- Fungsi Screenshot Umum ---
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str, crop_box: tuple[int, int, int, int] | None) -> str | None:
    global persistent_browser
    await init_browser()

    temp_path = f"full_{output_filename}"

    try:
        context = await persistent_browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto(looker_studio_url, timeout=60000)

        # Tunggu agar semua grafik dan elemen muncul
        await page.wait_for_timeout(7000)

        # Untuk monitoring ticket, pastikan semua konten ter-load
        if "monitoring" in output_filename.lower():
            # Scroll ke bawah untuk memuat semua data
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            # Scroll kembali ke atas
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(2000)

        await page.screenshot(path=temp_path, full_page=True)
        await context.close()

        # Jika crop_box diberikan, lakukan crop
        if crop_box:
            cropped_path = crop_image(temp_path, output_filename, crop_box)
            return cropped_path
        else:
            return temp_path

    except Exception as e:
        logger.error(f"❌ Gagal ambil screenshot dengan persistent browser: {e}")
        return None

# --- Fungsi untuk screenshot monitoring ticket khusus ---
async def take_monitoring_ticket_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(config.LOOKER_STUDIO_MONITORING, timeout=60000)

            # Tunggu elemen utama muncul
            await page.wait_for_selector("text=MONITORING TICKET", timeout=15000)
            await page.wait_for_timeout(3000)

            # Scroll ke bawah agar Looker Studio load semua elemen
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Ubah viewport sesuai tinggi halaman
            scroll_height = await page.evaluate("document.body.scrollHeight")
            await page.set_viewport_size({"width": 1920, "height": scroll_height})

            # Ambil screenshot full
            await page.screenshot(path=filename, full_page=True)
            print("✅ Screenshot berhasil diambil.")
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot monitoring ticket: {e}")
        finally:
            await browser.close()

# --- Fungsi helper untuk mengirim laporan dengan menghapus pesan loading ---
async def send_report_with_loading_cleanup(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                         loading_message: str, screenshot_url: str, 
                                         filename: str, crop_box: tuple[int, int, int, int] | None,
                                         caption: str):
    """
    Mengirim laporan dengan menghapus pesan loading setelah gambar terkirim
    """
    # Kirim pesan loading
    loading_msg = await update.message.reply_text(loading_message, parse_mode="Markdown")
    
    try:
        # Ambil screenshot
        path = await get_looker_studio_screenshot(screenshot_url, filename, crop_box)
        
        if path and os.path.exists(path):
            # Kirim gambar
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption=caption)
            
            # Hapus file gambar
            os.remove(path)
            
            # Hapus pesan loading
            await context.bot.delete_message(
                chat_id=update.effective_chat.id, 
                message_id=loading_msg.message_id
            )
            
            return True
        else:
            # Jika gagal, edit pesan loading menjadi pesan error
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=loading_msg.message_id,
                text="❌ Gagal menampilkan laporan.\nMohon coba lagi."
            )
            return False
            
    except Exception as e:
        logger.error(f"❌ Error saat mengirim laporan: {e}")
        # Jika terjadi error, edit pesan loading menjadi pesan error
        try:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=loading_msg.message_id,
                text="❌ Gagal menampilkan laporan.\nMohon coba lagi."
            )
        except:
            pass
        return False
