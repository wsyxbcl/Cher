#!/usr/bin/env python3
import logging
import configparser
import json

from telegram import ParseMode, InlineQueryResultArticle, InputTextMessageContent
import telegram.ext as tg
from telegram.error import TelegramError
from calcmass.mass import massof
from googlesearch import search

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
    bot.send_message(chat_id=update.message.chat_id, text="REPORT SITUATION.")
    logger.debug("Start from " + str(update.message.from_user.id))

def list_lectures(bot, update):
    lectures = get_lectures_XMU()
    # Offline version
    # lectures = load_lectures('./data/lectures.json')
    if not lectures:
        bot.send_message(chat_id=update.message.chat_id, text="Empty request.")
    else:
        lectures_md = ''
        for l in lectures:
            d = json.loads(l)
            lectures_md = lectures_md + "{} {} {} \n [{}]({})\n".format(
                d['time'], d['loc'], d['lecturer'], d['title'], d['url'])
        bot.send_message(chat_id=update.message.chat_id,  parse_mode=ParseMode.MARKDOWN,
                         text=lectures_md, disable_web_page_preview=True)
    logger.debug("Start from " + str(update.message.from_user.id))

def calcmass(bot, update, args):
    """
    Mass calculator.
    Using a refined version of Calcmass (https://github.com/wsyxbcl/Calcmass)
    """
    text_mass = ''.join(c+': {:.2f} g/mol \n'.format(massof(c)) for c in args)
    bot.send_message(chat_id=update.message.chat_id, text=text_mass)

def inline_google(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='google search',
            input_message_content=InputTextMessageContent(list(search(query, stop=1))[0])
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)

# Add handlers to dispatcher
updater.dispatcher.add_handler(tg.InlineQueryHandler(inline_google))
updater.dispatcher.add_handler(tg.CommandHandler('start', start))
updater.dispatcher.add_handler(tg.CommandHandler('list_lectures', list_lectures))
updater.dispatcher.add_handler(tg.CommandHandler('calcmass', calcmass, pass_args=True))

updater.start_polling()
updater.idle()