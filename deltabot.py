import pprint
import time

import telegram
from telegram.ext import Updater, CommandHandler

from configs import *
from utils.file_handlers import is_already_exist, keep_a_record
from utils.scrapers import get_results
from utils.toolkits import get_uploader_url

DEBUG = False


def test_leechx(bot: telegram.bot.Bot, update: telegram.update.Update):
    bot.send_message(debugx_chat_id, f"Triggered from {update.effective_chat}")
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
    # if DEBUG:
    #     bot.send_message(triggerx_chat_id[0], f"Update: {update}")

    cmd = update.message.text.split(" ")
    url = get_uploader_url(cmd[1])
    stop = 2
    if len(cmd) == 3:
        stop = int(cmd[2])
    if DEBUG:
        bot.send_message(debugx_chat_id, f"URL: {url} \nStop: {stop}")
    actual_paginator(bot, url, stop)


def paginator(bot: telegram.Bot, update: telegram.Update):
    """
    [Link_to_page_1] [[Stop=2]...]
    :param bot:
    :param update:
    :return:
    """
    if DEBUG:
        bot.send_message(debugx_chat_id, f"Update: {update}")

    cmd = update.message.text.split(" ")
    url: str = cmd[1]
    if url.endswith("/1/"):
        url = url[:-3]
    if url.endswith("/"):
        url = url[:-1]
    stop = 2
    if len(cmd) == 3:
        stop = int(cmd[2])
    if DEBUG:
        bot.send_message(debugx_chat_id, f"URL: {url} \nStop: {stop}")
    actual_paginator(bot, url, stop)


def actual_paginator(bot: telegram.Bot, url: str, stop: int):
    results = dict()
    num_results = 0
    for page in range(stop):
        for thing in get_results(url + f"/{page + 1}/", bot):
            # TODO: Keep Track :(
            info = {field: thing[field] for field in ["magnet", "follow_url"]}
            if not is_already_exist("logs", str(info)):
                keep_a_record("logs", str(info))
            print(info['follow_url'])
            if DEBUG:
                bot.send_message(debugx_chat_id, info['follow_url'])

            num_results += 1
            results[num_results] = thing
        bot.send_message(triggerx_chat_id[-1], f"Page {page + 1} scraped!")
    flood_my_dict(bot, results)
    bot.send_message(debugx_chat_id, pprint.pformat(results))


def flood_my_dict(bot, results):
    group = 0
    idx = 0
    for result in results.values():
        idx += 1
        print(idx)
        leech_cmd = f"/mirror@{leech_bots[idx % 3]}_leechx_bot "
        bot.send_message(triggerx_chat_id[group], leech_cmd + str(result["magnet"]))
        if idx / 18 == 1:
            group += 1
            group = group % 3
            idx = 0
            print("*" * 10 + f"Shifted to Group {group}" + "*" * 10)
        time.sleep(1.2)


def logs(bot: telegram.Bot, update: telegram.Update):
    bot.send_document(debugx_chat_id, open('logs', 'rb'))


def main():
    updater = Updater("910267145:AAFIwWP72YWpA2X76sR8T6CYMP9Fr4Exa7Y")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("test_leechx", test_leechx))
    dp.add_handler(CommandHandler("paginator", paginator))
    dp.add_handler(CommandHandler("uploader", uploader))
    dp.add_handler(CommandHandler("logs", logs))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
