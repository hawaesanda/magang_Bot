import os
import tempfile
from telegram import Bot
from telegram.error import TelegramError

async def send_report_with_loading_cleanup(bot: Bot, chat_id: int, report_type: str, screenshot_path: str, loading_message):
    """
    Fungsi untuk mengirim report dengan screenshot dan cleanup temporary files
    
    Args:
        bot: Instance Bot telegram
        chat_id: ID chat tujuan
        report_type: Jenis report untuk caption
        screenshot_path: Path ke file screenshot
        loading_message: Message loading yang akan diedit/hapus
    """
    try:
        if screenshot_path and os.path.exists(screenshot_path):
            # Kirim screenshot dengan caption
            with open(screenshot_path, 'rb') as photo:
                caption = f"📊 Report {report_type} telah berhasil dibuat!"
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption
                )
            
            # Hapus loading message
            try:
                await loading_message.delete()
            except TelegramError:
                pass  # Ignore jika gagal hapus message
            
            # Cleanup file screenshot
            try:
                os.remove(screenshot_path)
                print(f"✅ File {screenshot_path} berhasil dihapus")
            except OSError as e:
                print(f"⚠️ Gagal menghapus file {screenshot_path}: {e}")
            
            # Cleanup temporary full screenshot files
            temp_dir = tempfile.gettempdir()
            temp_files = [f for f in os.listdir(temp_dir) if f.startswith("temp_full_") and f.endswith(".png")]
            for temp_file in temp_files:
                try:
                    os.remove(os.path.join(temp_dir, temp_file))
                    print(f"✅ Temporary file {temp_file} berhasil dihapus")
                except OSError:
                    pass  # Ignore jika gagal hapus
            
        else:
            # Edit loading message menjadi error message
            await loading_message.edit_text("❌ Gagal mengambil screenshot. Silakan coba lagi.")
            
    except Exception as e:
        print(f"❌ Error dalam send_report_with_loading_cleanup: {e}")
        try:
            await loading_message.edit_text("❌ Terjadi kesalahan saat mengirim report. Silakan coba lagi.")
        except TelegramError:
            pass
