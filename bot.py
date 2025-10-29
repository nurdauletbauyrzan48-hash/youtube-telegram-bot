import telebot
import yt_dlp
import os

# Токеніңді осында қой
BOT_TOKEN = "8339569755:AAFkXi4EJsSqBN0yGFz7ItffJnKfwenY35M"
bot = telebot.TeleBot(BOT_TOKEN)

# Басты хабарлама
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "🎥 Сәлем! Маған YouTube сілтемесін жібер, мен видеоны жүктеп берем.")

# YouTube сілтемелерін ұстау
@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def download_youtube_video(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "📥 Видео жүктеліп жатыр, күте тұр...")

    try:
        # Жүктеу параметрлері
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            file_name = ydl.prepare_filename(info)

        # Видео жіберу
        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video, caption=f"✅ {video_title}")

        # Артық файлды өшіру
        os.remove(file_name)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Қате: {e}")

# Ботты іске қосу
bot.polling(none_stop=True)
