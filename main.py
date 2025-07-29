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
    app.add_handler(CommandHandler("test_scheduler", handlers.test_scheduler))
    app.add_handler(CommandHandler("msawsa", handlers.msawsa))
    app.add_handler(CommandHandler("pilaten", handlers.pilaten))
    app.add_handler(CommandHandler("monitoring_ticket", handlers.monitoring))
    
    # ASSURANCE handlers
    app.add_handler(CommandHandler("closed_ticket", handlers.closed_ticket))
    app.add_handler(CommandHandler("unspec", handlers.unspec))
    
    # PROVISIONING handlers
    app.add_handler(CommandHandler("funneling", handlers.funneling))
    app.add_handler(CommandHandler("detail_kendala_psb", handlers.detail_kendala_psb))
    app.add_handler(CommandHandler("detail_wo", handlers.detail_wo))
    
    # INDBIZ handlers
    app.add_handler(CommandHandler("funneling_indbiz", handlers.funneling_indbiz))
    app.add_handler(CommandHandler("detail_kendala_indbiz", handlers.detail_kendala_indbiz))
    app.add_handler(CommandHandler("detail_wo_indbiz", handlers.detail_wo_indbiz))
    
    # B2B handlers
    app.add_handler(CommandHandler("monitoring_ticket_b2b", handlers.monitoring_ticket_b2b))
    app.add_handler(CommandHandler("performance", handlers.performance))
    
    # IM3AS handler
    app.add_handler(CommandHandler("im3as", handlers.im3as))

    # Jadwal otomatis pukul 10:00, 14:00, 17:00
    job_queue = app.job_queue
    job_queue.run_daily(scheduler.scheduled_snapshots, time=dt_time(10, 0, tzinfo=config.TIMEZONE), name="job_pukul_10")
    job_queue.run_daily(scheduler.scheduled_snapshots, time=dt_time(15, 0, tzinfo=config.TIMEZONE ), name="job_pukul_15")
    job_queue.run_daily(scheduler.scheduled_snapshots, time=dt_time(17, 0, tzinfo=config.TIMEZONE), name="job_pukul_17")

    logging.info("✅ Bot dimulai...")
    app.run_polling()

if __name__ == "__main__":
    main()
