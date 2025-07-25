# Bot Command Documentation

## Commands List

### General Commands
- `/start` - Menampilkan menu utama dengan semua command yang tersedia

### ASSURANCE
- `/monitoring_ticket` - Screenshot monitoring ticket HSA
- `/closed_ticket` - Screenshot closed ticket dashboard
- `/unspec` - Screenshot UNSPEC dashboard

### PROVISIONING
- `/funneling` - Screenshot funneling dashboard
- `/detail_kendala_psb` - Screenshot detail kendala PSB
- `/detail_wo` - Screenshot detail WO (Work Order)

### INDBIZ
- `/funneling_indbiz` - Screenshot funneling dashboard untuk INDBIZ
- `/detail_kendala_indbiz` - Screenshot detail kendala INDBIZ
- `/detail_wo_indbiz` - Screenshot detail WO INDBIZ

### B2B
- `/monitoring_ticket_b2b` - Screenshot monitoring ticket B2B
- `/performance` - Screenshot performance dashboard

### IM3AS
- `/im3as` - Screenshot dashboard IM3AS

### Other Reports
- `/msawsa` - Screenshot laporan MSA/WSA
- `/pilaten` - Screenshot laporan PI LATEN

## Konfigurasi URL

Pastikan untuk mengupdate URL yang sesuai di `config.py`:

```python
# Update URL-URL berikut dengan URL Looker Studio yang benar:
LOOKER_STUDIO_MONITORING_TICKET = "URL_ANDA_DISINI"
LOOKER_STUDIO_FUNNELING_INDBIZ = "URL_ANDA_DISINI"
LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ = "URL_ANDA_DISINI"
LOOKER_STUDIO_DETAIL_WO_INDBIZ = "URL_ANDA_DISINI"
LOOKER_STUDIO_MONITORING_TICKET_B2B = "URL_ANDA_DISINI"
LOOKER_STUDIO_PERFORMANCE = "URL_ANDA_DISINI"
LOOKER_STUDIO_IM3AS = "URL_ANDA_DISINI"
```

## Notes
- Semua command menggunakan screenshot dengan crop default `(480, 80, 1700, 1020)`
- Setiap handler memiliki error handling dan logging
- File screenshot otomatis dihapus setelah dikirim ke chat
- Bot akan mengirim pesan loading sebelum mengambil screenshot
