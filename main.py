import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import time as dt_time
import config
import handlers
import scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("msawsa", handlers.msawsa))
    app.add_handler(CommandHandler("pilaten", handlers.pilaten))
    app.add_handler(CommandHandler("monitoring", handlers.monitoring))

    # Jadwal otomatis pukul 10:00, 14:00, 17:00
    job_queue = app.job_queue
    job_queue.run_daily(scheduler.scheduled_snapshots, time=dt_time(10, 0, tzinfo=config.TIMEZONE), name="job_pukul_10")
    job_queue.run_daily(scheduler.scheduled_snapshots, time=dt_time(14, 0, tzinfo=config.TIMEZONE ), name="job_pukul_14")
    job_queue.run_daily(scheduler.scheduled_snapshots, time=dt_time(15, 0, tzinfo=config.TIMEZONE), name="job_pukul_17")

    logging.info("✅ Bot dimulai...")
    app.run_polling()

if __name__ == "__main__":
    main()
