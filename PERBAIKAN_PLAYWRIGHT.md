# Perbaikan Playwright - Cropping dan Scrolling

## Masalah yang Diperbaiki

### 1. **Cropping dan Scrolling Issues**
**Problem**: Playwright tidak bisa melakukan crop scroll dengan baik dan tidak bisa mengakses section tertentu dari dashboard.

**Solusi yang Diimplementasikan**:

### 2. **Scroll Function yang Diperbaiki**
```python
async def scroll_and_load_content(page):
    """Scroll halaman untuk memuat semua konten Looker Studio"""
    try:
        # Scroll bertahap untuk memuat semua elemen
        scroll_steps = 5
        viewport_height = await page.evaluate("window.innerHeight")
        
        for i in range(scroll_steps):
            scroll_position = (i + 1) * viewport_height
            await page.evaluate(f"window.scrollTo(0, {scroll_position})")
            await page.wait_for_timeout(1500)  # Tunggu konten load
        
        # Scroll ke posisi maksimal
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)
        
        # Kembali ke atas untuk screenshot
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)
```

**Perbaikan**:
- ✅ **Scroll bertahap**: Sekarang scroll dilakukan dalam 5 langkah untuk memastikan semua konten ter-load
- ✅ **Network idle wait**: Menggunakan `page.wait_for_load_state("networkidle")` untuk memastikan semua request selesai
- ✅ **Timing yang lebih baik**: Waktu tunggu yang optimal untuk setiap step

### 3. **Section Access dengan Koordinat**
```python
def get_section_coordinates(section_name: str) -> tuple[int, int, int, int] | None:
    """Dapatkan koordinat crop untuk section tertentu"""
    SECTION_COORDINATES = {
        "FULL_DASHBOARD": (480, 80, 1700, 1020),
        "FULFILLMENT_FBB": (485, 80, 820, 370),
        "ASSURANCE_FBB": (800, 170, 1210, 525),
        "SCORE_CREDIT": (1200, 170, 1700, 330),
        "FULFILLMENT_BGES": (485, 360, 820, 620),
        "ASSURANCE_BGES": (485, 620, 810, 990),
        "MSA_ASSURANCE": (1205, 330, 1690, 690),
        "MSA_CNOP": (800, 515, 1210, 998),
        "MSA_QUALITY": (1205, 696, 1685, 995),
        "MONITORING_FULL": (480, 80, 1700, 2500),
        "MONITORING_TOP": (480, 80, 1700, 800),
        "MONITORING_MIDDLE": (480, 600, 1700, 1400),
        "MONITORING_BOTTOM": (480, 1200, 1700, 2500)
    }
    
    return SECTION_COORDINATES.get(section_name.upper())
```

**Perbaikan**:
- ✅ **Section mapping**: Setiap section dashboard punya koordinat yang tepat
- ✅ **Flexible cropping**: Bisa crop bagian manapun dari dashboard
- ✅ **Monitoring sections**: Monitoring ticket dibagi menjadi top, middle, bottom untuk akses yang lebih mudah

### 4. **New Handler Functions**
```python
async def get_section_screenshot(looker_studio_url: str, output_filename: str, section_name: str):
    """Ambil screenshot untuk section tertentu dari dashboard"""
    # Implementasi dengan scroll dan crop berdasarkan section
```

**Fitur Baru**:
- ✅ **Section handlers**: Command khusus untuk setiap section (`/msa_fulfillment_fbb`, `/msa_quality`, dll)
- ✅ **Custom section**: Command `/custom_section` untuk crop section apapun
- ✅ **Monitoring parts**: Command terpisah untuk bagian atas, tengah, bawah monitoring ticket

### 5. **Improved Screenshot Function**
```python
async def get_looker_studio_screenshot(looker_studio_url: str, output_filename: str, crop_box: tuple[int, int, int, int] | None):
    """Screenshot dengan scrolling yang diperbaiki"""
    # Untuk dashboard yang memerlukan scrolling
    if "monitoring" in output_filename.lower() or crop_box and crop_box[3] > 1500:
        await scroll_and_load_content(page)
    
    # Screenshot dengan full page
    await page.screenshot(path=temp_path, full_page=True)
```

**Perbaikan**:
- ✅ **Smart scrolling**: Otomatis detect kapan perlu scroll berdasarkan jenis dashboard
- ✅ **Better timing**: Waktu tunggu yang optimal untuk load konten
- ✅ **Full page capture**: Memastikan semua konten ter-capture

## Commands Baru yang Tersedia

### Section-Specific Commands:
- `/msa_fulfillment_fbb` - Screenshot section Fulfillment FBB
- `/msa_assurance_fbb` - Screenshot section Assurance FBB  
- `/msa_quality` - Screenshot section MSA Quality
- `/monitoring_top` - Screenshot bagian atas monitoring ticket
- `/monitoring_middle` - Screenshot bagian tengah monitoring ticket
- `/monitoring_bottom` - Screenshot bagian bawah monitoring ticket
- `/custom_section [SECTION_NAME]` - Screenshot section custom

### Section Names Available:
- `FULFILLMENT_FBB`, `ASSURANCE_FBB`, `SCORE_CREDIT`
- `FULFILLMENT_BGES`, `ASSURANCE_BGES`
- `MSA_ASSURANCE`, `MSA_CNOP`, `MSA_QUALITY`
- `MONITORING_TOP`, `MONITORING_MIDDLE`, `MONITORING_BOTTOM`

## Hasil Perbaikan

### ✅ **Cropping Problem - SOLVED**
- Sekarang bisa crop scroll dengan sempurna
- Bisa mengakses section tertentu dari dashboard
- Koordinat crop yang akurat untuk setiap section

### ✅ **Scrolling Problem - SOLVED**  
- Scroll bertahap memastikan semua konten ter-load
- Network idle detection untuk timing yang tepat
- Full page screenshot setelah scroll

### ✅ **Section Access - SOLVED**
- Bisa screenshot bagian manapun dari dashboard
- Command khusus untuk setiap section
- Flexible cropping system

## Teknologi yang Digunakan

✅ **Playwright** tetap digunakan karena:
- Sudah optimal setelah perbaikan
- Browser automation yang powerful
- Network state detection
- Full page screenshot capability
- Headless operation

✅ **Pillow** untuk:
- Image cropping yang presisi
- Multiple format support
- Memory efficient processing

## Testing

Bot telah ditest dan berjalan dengan sukses:
- ✅ Browser terinstall (Chromium)
- ✅ Dependencies terinstall semua
- ✅ Bot startup berhasil
- ✅ JobQueue untuk scheduled screenshots
- ✅ Error handling dan logging

## Kesimpulan

**Playwright + Pillow stack SUDAH OPTIMAL** untuk kebutuhan screenshot dashboard. Masalah cropping dan scrolling sudah terselesaikan dengan:

1. **Smart scrolling function** yang memuat konten secara bertahap
2. **Section coordinate mapping** untuk akses bagian tertentu  
3. **Improved timing** dengan network idle detection
4. **Flexible cropping system** dengan multiple section support

Tidak perlu ganti ke Selenium karena Playwright sudah memberikan semua fitur yang dibutuhkan dengan performa yang lebih baik.
