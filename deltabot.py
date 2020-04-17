from telegram.ext import Updater, CommandHandler
import telegram
from utils.file_handlers import keep_a_record, is_already_exist
from utils.scrapers import get_results
from utils.toolkits import get_uploader_url
import time

DEBUG = False


def test_leechx(bot: telegram.bot.Bot, update: telegram.update.Update):
    for leech_bot in leech_bots:
        for msg in test_downs:
            bot.send_message(
                triggerx_chat_id[0], f"/mirror@{leech_bot}_leechx_bot {msg}"
            )


def uploader(bot: telegram.Bot, update: telegram.Update):
    """
    [Name] [[Stop=2]...]
    :param bot:
    :param update:
    :return:
    """
    if DEBUG:
        bot.send_message(triggerx_chat_id[0], f"Update: {update}")

    cmd = update.message.text.split(" ")
    url = get_uploader_url(cmd[1])
    stop = 2
    if len(cmd) == 3:
        stop = int(cmd[2])
    if DEBUG:
        bot.send_message(triggerx_chat_id[0], f"URL: {url} \nStop: {stop}")
    actual_paginator(bot, url, stop)


def paginator(bot, update):
    pass


def actual_paginator(bot: telegram.Bot, url: str, stop: int):
    results = dict()
    num_results = 0
    for page in range(stop):
        for thing in get_results(url + f"/{page+1}/"):
            # if not is_already_exist("QxR", str(thing)):
            #     keep_a_record("QxR", str(thing))
            print(thing)
            num_results += 1
            results[num_results] = thing
        bot.send_message(triggerx_chat_id[-1], f"Page {page+1} scraped!")

    group = 0
    idx = 0
    for result in results.values():
        idx += 1
        print(idx)
        bot.send_message(triggerx_chat_id[group], str(result["follow_url"]))
        if idx / 18 == 1:
            group += 1
            group = group % 3
            idx = 0
            print("*" * 10 + f"Shifted to Group {group}" + "*" * 10)
        time.sleep(1.2)


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
    triggerx_chat_id = [-1001415869464, -1001283315074, -1001388834609]
    main()
