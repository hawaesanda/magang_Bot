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

        # Untuk monitoring ticket, gunakan fungsi khusus
        if "monitoring" in output_filename.lower():
            await context.close()
            return await take_monitoring_ticket_screenshot(output_filename)
        
        # Untuk closed ticket, gunakan fungsi khusus
        if "closed" in output_filename.lower():
            await context.close()
            return await take_closed_ticket_screenshot(output_filename)
        
        # Untuk unspec, gunakan fungsi khusus
        if "unspec" in output_filename.lower():
            await context.close()
            return await take_unspec_screenshot(output_filename)
        
        # Untuk funneling, gunakan fungsi khusus
        if "funneling" in output_filename.lower():
            await context.close()
            # Untuk funneling indbiz, gunakan URL yang berbeda
            if "indbiz" in output_filename.lower():
                return await take_funneling_indbiz_screenshot(output_filename)
            else:
                return await take_funneling_screenshot(output_filename)
        
        # Untuk detail kendala psb, gunakan fungsi khusus
        if "detail_kendala_psb" in output_filename.lower():
            await context.close()
            return await take_detail_kendala_psb_screenshot(output_filename)
        
        # Untuk detail wo, gunakan fungsi khusus
        if "detail_wo" in output_filename.lower():
            await context.close()
            # Untuk detail wo indbiz, gunakan URL yang berbeda
            if "indbiz" in output_filename.lower():
                return await take_detail_wo_indbiz_screenshot(output_filename)
            else:
                return await take_detail_wo_screenshot(output_filename)

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
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_MONITORING, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya dengan pendekatan yang lebih sederhana
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)  # Tunggu 10 detik untuk halaman dimuat sepenuhnya

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=MONITORING TICKET", timeout=20000)
                print("🔧 Judul MONITORING TICKET ditemukan")
            except:
                print("🔧 Judul tidak ditemukan, lanjut screenshot...")

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)  # Tunggu sebentar di setiap scroll

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)  # Tunggu lebih lama di bawah

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk menampilkan bagian yang penting saja
            # Berdasarkan layout: header + KPI + charts + sebagian tabel
            crop_box = (480, 80, 1700, 1310)   # Crop dari atas sampai sekitar baris ke-1200px
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot monitoring ticket berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot monitoring ticket: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot closed ticket khusus ---
async def take_closed_ticket_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Closed Ticket Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_CLOSED_TICKET, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=TICKET CLOSED MALANG", timeout=20000)
                print("🔧 Judul TICKET CLOSED MALANG ditemukan")
            except:
                print("🔧 Judul tidak ditemukan, lanjut screenshot...")

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk closed ticket
            # Berdasarkan layout: header + filter + KPI metrics + charts + sebagian tabel
            crop_box = (480, 80, 1700, 1310)   # Crop dari atas sampai sekitar baris ke-1200px
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot closed ticket berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot closed ticket: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot unspec khusus ---
async def take_unspec_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Unspec Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_UNSPEC, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=UNSPEC MALANG", timeout=20000)
                print("🔧 Judul UNSPEC MALANG ditemukan")
            except:
                print("🔧 Judul tidak ditemukan, lanjut screenshot...")

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk unspec
            # Berdasarkan layout: header + filter + KPI metrics + charts + tabel
            crop_box = (480, 80, 1700, 1310)   # Crop untuk menampilkan area dashboard utama
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot unspec berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot unspec: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot funneling khusus ---
async def take_funneling_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Funneling Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_FUNNELING, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk funneling - area yang lebih luas untuk menangkap semua elemen
            # Mencakup: header, date picker, pie chart, semua KPI metrics, arrows, dan tabel
            crop_box = (480, 80, 1700, 1310)   # Crop yang lebih luas untuk dashboard funneling
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot funneling berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot funneling: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot funneling indbiz khusus ---
async def take_funneling_indbiz_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Funneling INDBIZ Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_FUNNELING_INDBIZ, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk funneling indbiz - area yang lebih luas untuk menangkap semua elemen
            # Mencakup: header, date picker, pie chart, semua KPI metrics, arrows, dan tabel
            crop_box = (480, 80, 1700, 1310)   # Crop yang lebih luas untuk dashboard funneling
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot funneling indbiz berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot funneling indbiz: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot detail kendala PSB khusus ---
async def take_detail_kendala_psb_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Detail Kendala PSB Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_DETAIL_KENDALA_PSB, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk detail kendala PSB - area yang lebih luas
            # Mencakup: header, filter, charts, dan tabel detail
            crop_box = (480, 80, 1700, 1310)   # Crop yang lebih luas untuk dashboard funneling
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot detail kendala PSB berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot detail kendala PSB: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot detail WO khusus ---
async def take_detail_wo_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Detail WO Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_DETAIL_WO, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk detail WO - area yang lebih luas
            # Mencakup: header, filter, charts, dan tabel detail
            crop_box = (480, 80, 1700, 1310)   # Crop yang lebih luas untuk dashboard funneling
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot detail WO berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot detail WO: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot detail WO INDBIZ khusus ---
async def take_detail_wo_indbiz_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Detail WO INDBIZ Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_DETAIL_WO_INDBIZ, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):  # 20 kali scroll
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(800)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(8000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page dengan viewport besar
            print("🔧 Mengambil screenshot...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop screenshot untuk detail WO INDBIZ - area yang lebih luas
            # Mencakup: header, filter, charts, dan tabel detail
            crop_box = (480, 80, 1700, 1310)   # Crop yang lebih luas untuk dashboard funneling
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot detail WO INDBIZ berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot detail WO INDBIZ: {e}")
            return None
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
