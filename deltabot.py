import datetime
import pprint
import time

import requests
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
    paste_name = str(update.message.date + datetime.timedelta(hours=5, minutes=30))
    actual_paginator(bot, url, stop, paste_name)


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
    paste_name = str(update.message.date + datetime.timedelta(hours=5, minutes=30))
    actual_paginator(bot, url, stop, paste_name)


def actual_paginator(bot: telegram.Bot, url: str, stop: int, paste_name: str):
    results = dict()
    num_results = 0
    for page in range(stop):
        skips = list()
        for thing in get_results(url + f"/{page + 1}/", bot):
            info = {field: thing[field] for field in ["magnet", "follow_url"]}
            if is_already_exist("logs.txt", str(info['follow_url']).split('/')[-2]):
                if DEBUG:
                    bot.send_message(debugx_chat_id, f"Skipping ```{str(info['follow_url']).split('/')[-2]}```",
                                     parse_mode="Markdown")
                skips.append(str(info['follow_url']).split('/')[-2])
            else:
                keep_a_record("logs.txt", str(info))
                print(str(info['follow_url']).split('/')[-2])
                if DEBUG:
                    bot.send_message(debugx_chat_id, info['follow_url'])

                num_results += 1
                results[num_results] = thing
        skips_str = '```' + '```\n```'.join(skips) + '```'
        bot.send_message(debugx_chat_id, f"Page {page + 1} scraped!"
                                         f"\nSkips ({len(skips)}): {skips_str}", parse_mode="Markdown")
    flood_my_dict(bot, results)
    paste_code = paste_data.copy()
    paste_code['api_paste_code'] = str(pprint.pformat(results))
    paste_code['api_paste_name'] = paste_name
    res = requests.post(paste_url, paste_code, headers=header)
    bot.send_message(debugx_chat_id, f"Scraped data at {res.content.decode('utf-8')}")


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
    bot.send_document(debugx_chat_id, open('logs.txt', 'rb'))


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
