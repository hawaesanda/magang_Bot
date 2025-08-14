from playwright.async_api import async_playwright
import config
from .base import crop_image

# --- Fungsi untuk screenshot monitoring ticket khusus ---
async def take_monitoring_ticket_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("🔧 Mulai mengakses URL Looker Studio...")
            await page.goto(config.LOOKER_STUDIO_MONITORING, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=MONITORING TICKET", timeout=20000)
                print("🔧 Judul MONITORING TICKET ditemukan")
            except:
                print("🔧 Judul tidak ditemukan, lanjut screenshot...")

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Mulai scroll untuk memuat konten...")
            for i in range(20):
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
            
            # Jika ada crop_box, lakukan crop. Jika tidak, gunakan full page
            if config.CROP_MONITORING:
                cropped_path = crop_image(temp_full_path, filename, config.CROP_MONITORING)
                print("✅ Screenshot MONITORING TICKET berhasil diambil dan di-crop.")
                return cropped_path
            else:
                print("✅ Screenshot MONITORING TICKET berhasil diambil (full page).")
                return temp_full_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot monitoring ticket: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot monitoring ticket per HSA ---
async def take_monitoring_ticket_per_hsa_screenshot(hsa_name: str, filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print(f"🔧 Mulai mengakses URL Looker Studio untuk {hsa_name}...")
            await page.goto(config.LOOKER_STUDIO_MONITORING, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen judul muncul
            try:
                await page.wait_for_selector("text=MONITORING TICKET", timeout=20000)
                print("🔧 Judul MONITORING TICKET ditemukan")
            except:
                print("🔧 Judul tidak ditemukan, lanjut dengan filter...")

            # Cari dan klik filter HSA
            print(f"🔧 Mencari filter untuk {hsa_name}...")
            try:
                # Tunggu filter muncul
                await page.wait_for_timeout(5000)
                
                # Cari dan klik HSA yang diminta
                hsa_filter = await page.wait_for_selector(f"text={hsa_name}", timeout=15000)
                if hsa_filter:
                    await hsa_filter.click()
                    print(f"🔧 Filter {hsa_name} berhasil diklik")
                    await page.wait_for_timeout(5000)  # Tunggu data ter-filter
                else:
                    print(f"⚠️ Filter {hsa_name} tidak ditemukan")
            except Exception as e:
                print(f"⚠️ Gagal mengatur filter {hsa_name}: {e}")

            # Scroll bertahap untuk memuat semua konten yang ter-filter
            print("🔧 Mulai scroll untuk memuat konten ter-filter...")
            for i in range(15):  # Lebih sedikit scroll karena data sudah ter-filter
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(600)

            # Scroll ke paling bawah
            print("🔧 Scroll ke paling bawah...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)

            # Kembali ke atas untuk screenshot
            print("🔧 Kembali ke atas untuk screenshot...")
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot
            print(f"🔧 Mengambil screenshot untuk {hsa_name}...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Gunakan setting yang sama dengan monitoring ticket umum
            if config.CROP_MONITORING:
                cropped_path = crop_image(temp_full_path, filename, config.CROP_MONITORING)
                print(f"✅ Screenshot MONITORING TICKET {hsa_name} berhasil diambil dan di-crop.")
                return cropped_path
            else:
                print(f"✅ Screenshot MONITORING TICKET {hsa_name} berhasil diambil (full page).")
                return temp_full_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot monitoring ticket {hsa_name}: {e}")
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
            for i in range(20):
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
            crop_box = (480, 80, 1700, 1310)
            
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
            for i in range(20):
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
            crop_box = (480, 80, 1700, 1310)
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            print("✅ Screenshot unspec berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot unspec: {e}")
            return None
        finally:
            await browser.close()
