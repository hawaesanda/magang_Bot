import pytz
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Konfigurasi ---
TOKEN = os.getenv("TOKEN")
TARGET_CHAT_ID_RAW = os.getenv("TARGET_CHAT_ID")

# Parse TARGET_CHAT_ID menjadi list untuk multiple chat
if TARGET_CHAT_ID_RAW:
    TARGET_CHAT_IDS = [chat_id.strip() for chat_id in TARGET_CHAT_ID_RAW.split(",")]
else:
    TARGET_CHAT_IDS = []

# Backward compatibility - gunakan chat ID pertama sebagai default
TARGET_CHAT_ID = TARGET_CHAT_IDS[0] if TARGET_CHAT_IDS else None

# Timezone
TIMEZONE = pytz.timezone("Asia/Jakarta")

# MSA WSA dan Pilaten
LOOKER_STUDIO_MSA_WSA_URL = os.getenv("LOOKER_STUDIO_MSA_WSA_URL")
LOOKER_STUDIO_PILATEN_URL = os.getenv("LOOKER_STUDIO_PILATEN_URL")
CROP_MSAWSA = (350, 80, 1580, 1020)
CROP_PILATEN = (480, 80, 1700, 1020)

# Monitoring Ticket
CROP_MONITORING = (480, 80, 1700, 2500)
HSA_LIST_MONITORING = [
    "HSA KEPANJEN",
    "HSA BLIMBING",
    "HSA BATU",
    "HSA KLOJEN",
    "HSA MALANG",
    "HSA SINGOSARI",
    "HSA TUREN"
]

# ASSURANCE URLs
LOOKER_STUDIO_MONITORING = os.getenv("LOOKER_STUDIO_MONITORING")
LOOKER_STUDIO_CLOSED_TICKET = os.getenv("LOOKER_STUDIO_CLOSED_TICKET")
LOOKER_STUDIO_UNSPEC = os.getenv("LOOKER_STUDIO_UNSPEC")

# PROVISIONING URLs
LOOKER_STUDIO_FUNNELING = os.getenv("LOOKER_STUDIO_FUNNELING")
LOOKER_STUDIO_DETAIL_KENDALA_PSB = os.getenv("LOOKER_STUDIO_DETAIL_KENDALA_PSB")
LOOKER_STUDIO_DETAIL_WO = os.getenv("LOOKER_STUDIO_DETAIL_WO")

# INDBIZ URLs
LOOKER_STUDIO_FUNNELING_INDBIZ = os.getenv("LOOKER_STUDIO_FUNNELING_INDBIZ")
LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ = os.getenv("LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ")
LOOKER_STUDIO_DETAIL_WO_INDBIZ = os.getenv("LOOKER_STUDIO_DETAIL_WO_INDBIZ")

# B2B URLs
LOOKER_STUDIO_MONITORING_TICKET_B2B = os.getenv("LOOKER_STUDIO_MONITORING_TICKET_B2B")
LOOKER_STUDIO_PERFORMANCE = os.getenv("LOOKER_STUDIO_PERFORMANCE")

# IM3AS URLs
LOOKER_STUDIO_IM3AS = os.getenv("LOOKER_STUDIO_IM3AS")

# Crop settings untuk setiap dashboard
CROP_DEFAULT = (480, 80, 1700, 1020)


# Daftar section dan posisi crop-nya (left, top, right, bottom)
# SECTION_COORDINATES = {
#     "FULL_DASHBOARD": (480, 80, 1700, 1020),  # keseluruhan canvas
#     "FULFILLMENT_FBB": (485, 80, 820, 370),   # baris 1 kolom 1
#     "ASSURANCE_FBB": (800, 170, 1210, 525),    # baris 1 kolom 2
#     "SCORE_CREDIT": (1200, 170, 1700, 330),    # baris 1 kolom 3
#     "FULFILLMENT_BGES": (485, 360, 820, 620), # baris 2 kolom 1
#     "ASSURANCE_BGES": (485, 620, 810, 990),  # baris 2 kolom 2
#     "MSA_ASSURANCE": (1205, 330, 1690, 690),  # baris 2 kolom 3
#     "MSA_CNOP": (800, 515, 1210, 998),        # baris 3 kolom 1
#     "MSA_QUALITY": (1205, 696, 1685, 995)    # baris 3 kolom 3
# }
