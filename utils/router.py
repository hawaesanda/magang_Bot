import logging
import config
from .base import init_browser

# Import semua fungsi screenshot khusus
from .assurance import take_monitoring_ticket_screenshot, take_monitoring_ticket_per_hsa_screenshot, take_closed_ticket_screenshot, take_unspec_screenshot
from .provisioning import take_funneling_screenshot, take_detail_kendala_psb_screenshot, take_detail_wo_screenshot
from .indbiz import take_funneling_indbiz_screenshot, take_detail_kendala_indbiz_screenshot, take_detail_wo_indbiz_screenshot
from .b2b import take_monitoring_ticket_b2b_screenshot, take_performance_b2b_screenshot
from .imjas import take_imjas_screenshot
from .reports import take_msawsa_screenshot, take_pilaten_screenshot

logger = logging.getLogger(__name__)

# --- Fungsi Screenshot Umum ---
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str, crop_box: tuple[int, int, int, int] | None) -> str | None:
    # Untuk MSA/WSA, gunakan fungsi khusus dengan loading yang lebih robust
    if "msawsa" in output_filename.lower():
        return await take_msawsa_screenshot(output_filename)
        
    # Untuk PI LATEN, gunakan fungsi khusus
    if "pilaten" in output_filename.lower():
        return await take_pilaten_screenshot(output_filename)

    # Untuk dashboard lain, gunakan persistent browser
    global persistent_browser
    await init_browser()

    temp_path = f"full_{output_filename}"

    try:
        from .base import persistent_browser
        context = await persistent_browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto(looker_studio_url, timeout=60000)

        # Tunggu agar semua grafik dan elemen muncul
        await page.wait_for_timeout(7000)

        # Untuk monitoring ticket B2B, gunakan fungsi khusus
        if "monitoring_ticket_b2b" in output_filename.lower():
            await context.close()
            return await take_monitoring_ticket_b2b_screenshot(output_filename)
        
        # Untuk monitoring ticket, cek apakah ada HSA spesifik
        if "monitoring" in output_filename.lower():
            await context.close()
            # Cek apakah ada HSA spesifik di filename
            for hsa in config.HSA_LIST_MONITORING:
                hsa_key = hsa.replace("HSA ", "").lower()  # "KEPANJEN", "BLIMBING", dll
                if hsa_key in output_filename.lower():
                    return await take_monitoring_ticket_per_hsa_screenshot(hsa, output_filename)
            # Jika tidak ada HSA spesifik, gunakan monitoring umum
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
        
        # Untuk detail kendala indbiz, gunakan fungsi khusus
        if "detail_kendala_indbiz" in output_filename.lower():
            await context.close()
            return await take_detail_kendala_indbiz_screenshot(output_filename)
        
        # Untuk detail wo, gunakan fungsi khusus
        if "detail_wo" in output_filename.lower():
            await context.close()
            # Untuk detail wo indbiz, gunakan URL yang berbeda
            if "indbiz" in output_filename.lower():
                return await take_detail_wo_indbiz_screenshot(output_filename)
            else:
                return await take_detail_wo_screenshot(output_filename)
        
        # Untuk IMJAS, gunakan fungsi khusus
        if "imjas" in output_filename.lower():
            await context.close()
            return await take_imjas_screenshot(output_filename)
        
        # Untuk performance, gunakan fungsi khusus
        if "performance" in output_filename.lower():
            await context.close()
            return await take_performance_b2b_screenshot(output_filename)

        await page.screenshot(path=temp_path, full_page=True)
        await context.close()

        # Jika crop_box diberikan, lakukan crop
        if crop_box:
            from .base import crop_image
            cropped_path = crop_image(temp_path, output_filename, crop_box)
            return cropped_path
        else:
            return temp_path

    except Exception as e:
        logger.error(f"❌ Gagal ambil screenshot dengan persistent browser: {e}")
        return None
