import os
from pytimeparse import parse

from dotenv import load_dotenv
import ptbot


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

bot = ptbot.Bot(TELEGRAM_TOKEN)


def reply(chat_id, text):
    seconds = parse(text)
    message_id = bot.send_message(chat_id, create_progress_message(seconds, seconds))
    remaining_time = seconds

    def update_timer():
        nonlocal remaining_time

        if remaining_time > 0:
            progress_message = create_progress_message(seconds, remaining_time)

            try:
                bot.update_message(chat_id, message_id, progress_message)
            except Exception as e:
                print(f"Ошибка при обновлении сообщения: {e}")

            remaining_time -= 1
            bot.create_timer(1, update_timer)
        else:
            bot.send_message(chat_id, "Время вышло!")

    bot.create_timer(1, update_timer)


def create_progress_message(total_seconds, remaining_seconds):
    progress_bar = render_progressbar(total_seconds, remaining_seconds)
    return f"Осталось секунд: {remaining_seconds}\n{progress_bar}"


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):

    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f"{prefix} |{pbar}| {percent}% {suffix}"


if __name__ == "__main__":
    bot.reply_on_message(reply)
    bot.run_bot()
