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

# --- Fungsi untuk menangani Looker Studio ---
async def handle_looker_studio_loading(page):
    """
    Fungsi khusus untuk menangani loading dan scrolling pada Looker Studio
    """
    try:
        # Tunggu elemen dashboard muncul
        await page.wait_for_selector('iframe, [data-testid="dashboard"], canvas, svg', timeout=30000)
        
        # Tunggu loading selesai
        await page.wait_for_load_state('networkidle', timeout=30000)
        
        # Dapatkan informasi viewport dan konten
        content_info = await get_viewport_and_content_info(page)
        logger.info(f"📏 Content info: {content_info}")
        
        # Jika konten sangat panjang, gunakan strategi scroll yang berbeda
        if content_info['contentHeight'] > content_info['viewportHeight'] * 5:
            logger.info("📜 Konten sangat panjang, menggunakan scroll cepat")
            scroll_step = 500
            delay_ms = 200
        else:
            scroll_step = 200
            delay_ms = 300
        
        # Scroll bertahap untuk trigger lazy loading
        await page.evaluate(f"""
            async () => {{
                const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                
                // Scroll down slowly to trigger all lazy loaded content
                const scrollStep = {scroll_step};
                const delayMs = {delay_ms};
                const totalHeight = {content_info['contentHeight']};
                
                console.log('Starting scroll process, total height:', totalHeight);
                
                for (let i = 0; i < totalHeight; i += scrollStep) {{
                    window.scrollTo(0, i);
                    await delay(delayMs);
                }}
                
                // Scroll to bottom and wait
                window.scrollTo(0, totalHeight);
                await delay(3000);
                
                // Try to trigger any remaining lazy content by scrolling back up
                for (let i = totalHeight; i >= 0; i -= scrollStep * 2) {{
                    window.scrollTo(0, i);
                    await delay(delayMs / 2);
                }}
                
                // Final scroll to top
                window.scrollTo(0, 0);
                await delay(2000);
                
                console.log('Scroll process completed');
            }}
        """)
        
        # Tunggu setelah scroll
        await page.wait_for_timeout(5000)
        
        # Coba click pada area dashboard jika diperlukan (untuk activate)
        try:
            await page.mouse.move(960, 540)  # Move to center
            await page.mouse.click(960, 540)
            await page.wait_for_timeout(2000)
        except:
            pass
            
    except Exception as e:
        logger.warning(f"⚠️ Warning saat handle Looker Studio: {e}")

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
        context = await persistent_browser.new_context(
            viewport={"width": 1920, "height": 1080},
            # Menambahkan user agent untuk menghindari deteksi bot
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Set timeout yang lebih panjang
        page.set_default_timeout(90000)
        
        await page.goto(looker_studio_url, timeout=90000, wait_until="networkidle")
        
        # Gunakan fungsi khusus untuk Looker Studio
        await handle_looker_studio_loading(page)
        
        # Ambil screenshot dengan full page
        await page.screenshot(path=temp_path, full_page=True, timeout=60000)
        await context.close()

        cropped_path = crop_image(temp_path, output_filename, crop_box)
        return cropped_path

    except Exception as e:
        logger.error(f"❌ Gagal ambil screenshot dengan persistent browser: {e}")
        try:
            await context.close()
        except:
            pass
        return None

async def get_viewport_and_content_info(page):
    """
    Mendapatkan informasi viewport dan konten untuk optimasi scroll
    """
    return await page.evaluate("""
        () => {
            return {
                viewportHeight: window.innerHeight,
                viewportWidth: window.innerWidth,
                contentHeight: Math.max(
                    document.body.scrollHeight,
                    document.documentElement.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.offsetHeight,
                    document.body.clientHeight,
                    document.documentElement.clientHeight
                ),
                contentWidth: Math.max(
                    document.body.scrollWidth,
                    document.documentElement.scrollWidth,
                    document.body.offsetWidth,
                    document.documentElement.offsetWidth,
                    document.body.clientWidth,
                    document.documentElement.clientWidth
                )
            };
        }
    """)
    
