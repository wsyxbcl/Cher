#!/usr/bin/env python3
import logging
import configparser
import json

from telegram import ParseMode
import telegram.ext as tg
from telegram.error import TelegramError

from crawler import get_lectures_XMU, load_lectures

config = configparser.ConfigParser()
config.read('./config.ini')
bot_token = config['telegram']['token']

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
logger = logging.getLogger(__name__)

updater = tg.Updater(token=bot_token)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is Cher.")
    logger.debug("Start from " + str(update.message.from_user.id))

def list_lectures(bot, update):
    # bot.send_message(chat_id=update.message.chat_id, text=str(get_lectures_XMU()))
    # Offline version
    lectures = load_lectures('./data/lectures.json')
    lectures_md = ''
    for l in lectures:
        d = json.loads(l)
        lectures_md = lectures_md + "{} {} {} \n [{}]({})\n".format(d['time'], d['loc'], d['lecturer'], d['title'], d['url'])
    bot.send_message(chat_id=update.message.chat_id,  parse_mode=ParseMode.MARKDOWN,
                     text=lectures_md)
    logger.debug("Start from " + str(update.message.from_user.id))


# Add handlers to dispatcher
updater.dispatcher.add_handler(tg.CommandHandler('start', start))
updater.dispatcher.add_handler(tg.CommandHandler('list_lectures', list_lectures))
updater.start_polling()
updater.idle()