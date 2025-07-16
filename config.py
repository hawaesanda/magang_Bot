import pytz

# --- Konfigurasi ---
TOKEN = "7941038639:AAGOUrsa05AbgV46g-WmLszUig26Fd-tIDk"
LOOKER_STUDIO_MSA_WSA_URL = "https://lookerstudio.google.com/s/i3tlaggtDik"
LOOKER_STUDIO_PILATEN_URL = "https://lookerstudio.google.com/s/s2yRKBhqWME"
TARGET_CHAT_ID = "1003337187"

# Timezone
TIMEZONE = pytz.timezone("Asia/Jakarta")

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
CROP_MSAWSA = (480, 80, 1700, 1020)
CROP_PILATEN = (480, 80, 1700, 1020)
