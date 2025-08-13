import os
import logging
from PIL import Image
from playwright.async_api import async_playwright

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
