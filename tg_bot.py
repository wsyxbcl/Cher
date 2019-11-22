#!/usr/bin/env python3
import datetime
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

def gen_gcal_url(action, text, dates, ctz, details, location):
    """
    Generate event url for google calendar.
    https://github.com/InteractionDesignFoundation/add-event-to-calendar-docs/blob/master/services/google.md
    """
    # 'Asia/Shanghai'
    # 'TEMPLATE'
    base_url = "https://calendar.google.com/calendar/render"
    gcal_url = base_url+"?action={}&text={}&dates={}&details={}&location={}&ctz={}".format(
        action, text, dates, details, location, ctz)
    return gcal_url
    
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="REPORT SITUATION.")
    logger.info("Start from " + str(update.message.from_user.id))

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
            lec_time_gcal = datetime.datetime.strptime(d['time'], 
                '%Y-%m-%d %H:%M:%S').strftime('%Y%m%dTo%H%M%S')
            lec_gcal = gen_gcal_url(action='TEMPLATE', text=d['title'], 
                dates=lec_time_gcal+'/'+lec_time_gcal, ctz='Asia/Shanghai', 
                details=d['url'], location=d['loc']) 
            lectures_md = lectures_md + "{} {} {} \n [{}]({})\n [ADD TO GCAL]({})".format(
                d['time'], d['loc'], d['lecturer'], d['title'], d['url'], lec_gcal)
        bot.send_message(chat_id=update.message.chat_id,  parse_mode=ParseMode.MARKDOWN,
                         text=lectures_md, disable_web_page_preview=True)
    logger.info("Request lectures from " + str(update.message.from_user.id))

def calcmass(bot, update, args):
    """
    Mass calculator.
    Using a refined version of Calcmass (https://github.com/wsyxbcl/Calcmass)
    """
    if len(args) >= 1:
        try:
            text_mass = ''.join(c+': {:.2f} g/mol \n'.format(massof(c)) for c in args)
            update.message.reply_text(text_mass)
        except ValueError:
            update.message.reply_text("Unknown element")
    else:
        update.message.reply_text("Usage: /calcmass <compound>")
    logger.info("Calcmass from " + str(update.message.from_user.id))

def calccap(bot, update, args):
    """
    Capacity calculator.
    Calculate theoritical capacity of given material.
    """
    if len(args) == 1:
        try:
            mass = massof(args[0])
            cap = (96485 * 1000) / (3600 * mass) # mAh/g
            text_cap = '{:.2f} mAh/g per #electron \n'.format(cap)
            update.message.reply_text(text_cap)
        except ValueError:
            update.message.reply_text("Unknown element")
    else:
        update.message.reply_text("Usage: /calccap <compound>")
    logger.info("Calccap from " + str(update.message.from_user.id))


def inline_google(bot, update):
    query = update.inline_query.query
    username = update.inline_query.from_user.username
    if not query:
        return
    gsearch_result = list(search(query, stop=1))[0]
    results = list()
    results.append(
        InlineQueryResultArticle(
            id="gsearch_cher",
            title='google search',
            description=query, 
            input_message_content=InputTextMessageContent(username+': <code>google </code>'+
                query+'\n'+gsearch_result, 
                parse_mode=ParseMode.HTML)
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)
    logger.info("Inline query from "+str(update.inline_query.from_user.id))

# Add handlers to dispatcher
updater.dispatcher.add_handler(tg.InlineQueryHandler(inline_google))
updater.dispatcher.add_handler(tg.CommandHandler('start', start))
updater.dispatcher.add_handler(tg.CommandHandler('list_lectures', list_lectures))
updater.dispatcher.add_handler(tg.CommandHandler('calcmass', calcmass, pass_args=True))
updater.dispatcher.add_handler(tg.CommandHandler('calccap', calccap, pass_args=True))

updater.start_polling()
updater.idle()
