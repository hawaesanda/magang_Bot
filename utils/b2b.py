from playwright.async_api import async_playwright
import config
from .base import crop_image

# --- Fungsi untuk screenshot monitoring ticket B2B ---
async def take_monitoring_ticket_b2b_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Monitoring Ticket B2B Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_MONITORING_TICKET_B2B, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=MONITORING TICKET B2B", timeout=20000)
                print("🔧 Judul MONITORING TICKET B2B ditemukan")
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
            
            # Crop screenshot untuk monitoring ticket B2B
            crop_box = (480, 80, 1700, 1310)   # Crop standar
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot monitoring ticket B2B berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot monitoring ticket B2B: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot performance B2B ---
async def take_performance_b2b_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Performance B2B Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_PERFORMANCE, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=PERFORMANCE B2B", timeout=20000)
                print("🔧 Judul PERFORMANCE B2B ditemukan")
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
            
            # Crop screenshot untuk performance B2B
            crop_box = (480, 80, 1700, 1310)   # Crop standar
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot performance B2B berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot performance B2B: {e}")
            return None
        finally:
            await browser.close()
