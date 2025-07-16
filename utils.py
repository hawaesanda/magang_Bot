import os
import logging
from PIL import Image
from playwright.async_api import async_playwright
import config

# Persistent browser instance
persistent_browser = None
logger = logging.getLogger(__name__)

async def init_browser():
    global persistent_browser
    if persistent_browser is None:
        playwright = await async_playwright().start()
        persistent_browser = await playwright.chromium.launch(headless=True)
        logger.info("✅ Persistent browser started.")

# --- Fungsi Crop ---
def crop_image(input_path: str, output_path: str, crop_box: tuple[int, int, int, int]) -> str:
    try:
        with Image.open(input_path) as img:
            cropped = img.crop(crop_box)
            cropped.save(output_path)
        os.remove(input_path)
        return output_path
    except Exception as e:
        logger.error(f"❌ Gagal crop gambar: {e}")
        return input_path
    
# --- Fungsi Screenshot ---
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str, crop_box: tuple[int, int, int, int]) -> str | None:
    global persistent_browser
    await init_browser()

    temp_path = f"full_{output_filename}"

    try:
        context = await persistent_browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto(looker_studio_url, timeout=60000)
        await page.wait_for_timeout(7000)
        await page.screenshot(path=temp_path, full_page=True)
        await context.close()

        cropped_path = crop_image(temp_path, output_filename, crop_box)
        return cropped_path

    except Exception as e:
        logger.error(f"❌ Gagal ambil screenshot dengan persistent browser: {e}")
        return None
    
