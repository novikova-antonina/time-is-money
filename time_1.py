import os

from dotenv import load_dotenv
from pytimeparse import parse
import ptbot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

bot = ptbot.Bot(TELEGRAM_TOKEN)


def reply(chat_id, text):
    input_seconds = parse(text)
    if not input_seconds:
        bot.send_message(
            chat_id, "Пожалуйста, укажите корректное время (например, '1m30s')."
        )
        return

    message_id = bot.send_message(chat_id, "Таймер запущен")
    bot.create_countdown(
        input_seconds,
        notify,
        chat_id=chat_id,
        message_id=message_id,
        total_seconds=input_seconds,
    )


def notify(secs_left, chat_id, message_id, total_seconds):
    remaining_time = format_time(secs_left)
    progress_bar = render_progressbar(total_seconds, total_seconds - secs_left)
    bot.update_message(
        chat_id, message_id, f"Осталось времени: {remaining_time}\n{progress_bar}"
    )
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло!")


def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02}:{remaining_seconds:02}"


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def main():

    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == "__main__":
    main()
