from playwright.async_api import async_playwright
import config
from .base import crop_image

# --- Fungsi untuk screenshot funneling ---
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

            # Tunggu elemen judul muncul 
            try:
                await page.wait_for_selector("text=Funnel Sales", timeout=20000)
                print("🔧 Judul Funnel Sales ditemukan")
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
            
            # Crop screenshot untuk menampilkan bagian funneling yang penting
            crop_box = (480, 80, 1700, 1310)   # Crop standar
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot funneling berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot funneling: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot detail kendala PSB ---
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

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=KENDALA PSB", timeout=20000)
                print("🔧 Judul KENDALA PSB ditemukan")
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
            
            # Crop screenshot untuk detail kendala PSB
            crop_box = (480, 80, 1700, 1310)   # Crop standar
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot detail kendala PSB berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot detail kendala PSB: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot detail WO ---
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

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=WO", timeout=20000)
                print("🔧 Judul WO ditemukan")
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
            
            # Crop screenshot untuk detail WO
            crop_box = (480, 80, 1700, 1310)   # Crop standar
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot detail WO berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot detail WO: {e}")
            return None
        finally:
            await browser.close()
