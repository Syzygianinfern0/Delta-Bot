from telegram.ext import Updater, CommandHandler
import telegram


def test_leechx(bot: telegram.bot.Bot, update: telegram.update.Update):
    for leech_bot in leech_bots:
        for msg in test_downs:
            bot.send_message(leechx_chat_id, f"/mirror@{leech_bot}_leechx_bot {msg}")


def uploader(bot, update):
    actual_paginator(bot, None, None)


def paginator(bot, update):
    pass


def actual_paginator(bot, url, stop):
    pass


def main():
    updater = Updater("910267145:AAFIwWP72YWpA2X76sR8T6CYMP9Fr4Exa7Y")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("test_leechx", test_leechx))
    dp.add_handler(CommandHandler("paginator", paginator))
    dp.add_handler(CommandHandler("uploader", uploader))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    leech_bots = ["alpha", "beta", "gamma"]
    test_downs = [
        "https://speed.hetzner.de/1GB.bin",
        "https://speed.hetzner.de/100MB.bin",
    ]
    leechx_chat_id = -1001415869464
    main()
