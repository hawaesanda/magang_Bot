import os
import logging
import pytz
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import TOKEN
import utils
from scheduler import scheduled_snapshots
from handlers import (
    start, msawsa, pilaten, handle_section_crop,
    fulfillment_fbb, assurance_fbb, score_credit,
    fulfillment_bges, assurance_bges, msa_assurance,
    msa_cnop, msa_quality
)

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Main Bot ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("msawsa", msawsa))
    app.add_handler(CommandHandler("pilaten", pilaten))
    app.add_handler(CallbackQueryHandler(handle_section_crop))
    app.add_handler(CommandHandler("fulfillment_fbb", fulfillment_fbb))
    app.add_handler(CommandHandler("assurance_fbb", assurance_fbb))
    app.add_handler(CommandHandler("score_credit", score_credit))
    app.add_handler(CommandHandler("fulfillment_bges", fulfillment_bges))
    app.add_handler(CommandHandler("assurance_bges", assurance_bges))
    app.add_handler(CommandHandler("msa_assurance", msa_assurance))
    app.add_handler(CommandHandler("msa_cnop", msa_cnop))
    app.add_handler(CommandHandler("msa_quality", msa_quality))


    job_queue = app.job_queue
    job_queue.run_repeating(scheduled_snapshots, interval=3600, first=0)  # update setiap 1 jam akan mengirim ss otomatis

    logger.info("✅ Bot dimulai...")
    app.run_polling()

if __name__ == "__main__":
    main()
