from playwright.async_api import async_playwright
import config
from .base import crop_image

# --- Fungsi untuk screenshot MSA/WSA (versi sederhana) ---
async def take_msawsa_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            await page.goto(config.LOOKER_STUDIO_MSA_WSA_URL, timeout=60000)
            
            # Wait sederhana seperti dashboard lain
            await page.wait_for_timeout(7000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop menggunakan crop box standar
            crop_box = (350, 80, 1570, 1020)  # Crop standar seperti dashboard lain
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot MSA/WSA: {e}")
            return None
        finally:
            await browser.close()

# --- Fungsi untuk screenshot PI LATEN (versi sederhana) ---
async def take_pilaten_screenshot(filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            await page.goto(config.LOOKER_STUDIO_PILATEN_URL, timeout=60000)
            
            # Wait sederhana seperti dashboard lain
            await page.wait_for_timeout(7000)
            
            # Ambil screenshot full page dulu
            temp_full_path = f"temp_full_{filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop menggunakan crop box standar
            crop_box = (480, 80, 1700, 1310)  # Crop standar seperti dashboard lain
            
            cropped_path = crop_image(temp_full_path, filename, crop_box)
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot PI LATEN: {e}")
            return None
        finally:
            await browser.close()
