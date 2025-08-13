from playwright.async_api import async_playwright
import config
from .base import crop_image

# Mapping section names ke crop boxes
SECTION_CROP_BOXES = {
    # MSA/WSA Sections
    "FULFILLMENT_FBB": (480, 200, 1200, 600),  # Section fulfillment FBB
    "ASSURANCE_FBB": (480, 600, 1200, 1000),   # Section assurance FBB  
    "SCORE_CREDIT": (1200, 200, 1700, 600),    # Section score credit
    "FULFILLMENT_BGES": (480, 1000, 1200, 1400), # Section fulfillment BGES
    "ASSURANCE_BGES": (1200, 600, 1700, 1000),  # Section assurance BGES
    "MSA_ASSURANCE": (480, 1400, 1200, 1800),   # Section MSA assurance
    "MSA_CNOP": (1200, 1000, 1700, 1400),       # Section MSA CNOP
    "MSA_QUALITY": (1200, 1400, 1700, 1800),    # Section MSA quality
    
    # Monitoring ticket sections
    "MONITORING_TOP": (480, 80, 1700, 500),     # Bagian atas monitoring
    "MONITORING_MIDDLE": (480, 500, 1700, 900), # Bagian tengah monitoring
    "MONITORING_BOTTOM": (480, 900, 1700, 1310), # Bagian bawah monitoring
}

async def get_section_screenshot(looker_studio_url: str, output_filename: str, section_name: str) -> str | None:
    """
    Ambil screenshot untuk section tertentu dari dashboard
    
    Args:
        looker_studio_url: URL dashboard Looker Studio
        output_filename: Nama file output
        section_name: Nama section yang akan di-screenshot
        
    Returns:
        Path file screenshot yang sudah di-crop, atau None jika gagal
    """
    # Cek apakah section name valid
    if section_name not in SECTION_CROP_BOXES:
        print(f"❌ Section '{section_name}' tidak ditemukan")
        return None
    
    crop_box = SECTION_CROP_BOXES[section_name]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print(f"🔧 Mengakses URL: {looker_studio_url}")
            await page.goto(looker_studio_url, timeout=60000)

            # Tunggu halaman dimuat sepenuhnya
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Scroll bertahap untuk memuat semua konten
            print("🔧 Scroll untuk memuat konten...")
            for i in range(15):
                scroll_position = (i + 1) * 200
                await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await page.wait_for_timeout(500)

            # Scroll ke paling bawah
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)

            # Kembali ke atas
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(3000)

            # Ambil screenshot full page
            print(f"🔧 Mengambil screenshot section {section_name}...")
            await page.set_viewport_size({"width": 1920, "height": 4000})
            await page.wait_for_timeout(2000)
            
            temp_full_path = f"temp_full_{output_filename}"
            await page.screenshot(path=temp_full_path, full_page=True)
            
            # Crop ke section yang diminta
            cropped_path = crop_image(temp_full_path, output_filename, crop_box)
            print(f"✅ Screenshot section {section_name} berhasil diambil dan di-crop.")
            return cropped_path
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot section {section_name}: {e}")
            return None
        finally:
            await browser.close()

async def get_screenshot_by_element(looker_studio_url: str, output_filename: str, element_selector: str) -> str | None:
    """
    Ambil screenshot dari elemen tertentu berdasarkan selector
    
    Args:
        looker_studio_url: URL dashboard Looker Studio
        output_filename: Nama file output
        element_selector: CSS selector untuk elemen yang akan di-screenshot
        
    Returns:
        Path file screenshot elemen, atau None jika gagal
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print(f"🔧 Mengakses URL: {looker_studio_url}")
            await page.goto(looker_studio_url, timeout=60000)

            # Tunggu halaman dimuat
            print("🔧 Tunggu halaman dimuat...")
            await page.wait_for_timeout(10000)

            # Tunggu elemen muncul
            print(f"🔧 Menunggu elemen: {element_selector}")
            await page.wait_for_selector(element_selector, timeout=20000)

            # Scroll ke elemen jika perlu
            element = page.locator(element_selector)
            await element.scroll_into_view_if_needed()
            await page.wait_for_timeout(2000)

            # Screenshot elemen
            print(f"🔧 Mengambil screenshot elemen...")
            await element.screenshot(path=output_filename)
            
            print(f"✅ Screenshot elemen berhasil diambil: {output_filename}")
            return output_filename
            
        except Exception as e:
            print(f"❌ Gagal mengambil screenshot elemen: {e}")
            return None
        finally:
            await browser.close()
