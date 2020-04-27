#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from data import data
import re as regex
from datetime import datetime
all_user_data = dict()


# 1 su 2 fu 3 fd 4 sd

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO, STATION, PLATFORM, PTT, ACTIONSELECT, TRACKTRAIN = range(
    9)

stations = ['churchgate', 'marinelines', 'charniroad', 'grantroad', 'mumbaicentral', 'mahalaxmi', 'lowerparel', 'elphinstoneroad', 'dadar', 'matungaroad', 'mahim', 'bandra', 'kharroad',
            'santacruz', 'vileparle', 'andheri', 'jogeshwari', 'goregaon', 'malad', 'kandivali', 'borivali', 'dahisar', 'miraroad', 'bhayandar', 'naigaon', 'vasai', 'nalasopara', 'virar']
dplat = {
    'VIRAR <- (S)': 1, '-> CHURCHGATE (S)': 4, 'VIRAR <- (F)': 2, '-> CHURCHGATE (F)': 3
}


def start(bot, update):

    update.message.reply_text(
        '''Hi! My name is Rail It. I am here to help you. Send /cancel to stop talking to me.\nPlease may I know what station are you at?''')
    all_user_data[update.message.from_user.id] = {}

    return STATION


def station(bot, update):
    pfr = [['VIRAR <- (S)'], ['-> CHURCHGATE (S)'],
           ['VIRAR <- (F)'], ['-> CHURCHGATE (F)']]
    user = update.message.from_user
    logger.info("%s said he is at %s", user.first_name, update.message.text)
    stn = update.message.text.lower().replace(' ', '')
    # print(stn)
    # print(stations)
    if stn not in stations:
        update.message.reply_text("I am sorry. I don't think that's a station")
    else:
        all_user_data[user.id]['station'] = stn
        update.message.reply_text("""Cool! So which direction are you gonna travel>""",
                                  reply_markup=ReplyKeyboardMarkup(pfr, one_time_keyboard=True))
    return PLATFORM


def platform(bot, update):
    user = update.message.from_user
    logger.info("%s said wanna travel towards %s",
                user.first_name, update.message.text)
    # update.message.reply_text("Platform number %s serves %s trains going %s side.\n Please select one of the following actions.", update.message.text, pfsupd[int(update.message.text)][0],  )
    rep = update.message.text

    msgstr = ''
    if '(F)' in rep:
        msgstr += 'In a hurry I see! '
    msgstr += 'You should head to Platform Number '+str(dplat[rep])+'.'
    all_user_data[user.id]['platform'] = str(dplat[rep])
    msgstr += '\nPlease select one of the following actions'
    acl = [['1. Track Train'], ['2. Get info about Delays'],
           ['3. List all upcoming trains']]
    update.message.reply_text(
        msgstr, reply_markup=ReplyKeyboardMarkup(acl, one_time_keyboard=True))
    return ACTIONSELECT


def actionselect(bot, update):
    user = update.message.from_user
    ch = update.message.text
    m = regex.search('[1-3]', ch)
    ch = m.group(0)
    logger.info("%s selected %s", user.first_name, ch)
    if ch == "1":
        update.message.reply_text(
            "Please enter the scheduled time of the train")
        return TRACKTRAIN
    elif ch == "2":
        delaymsg = delayinfo(
            all_user_data[user.id]['station'], all_user_data[user.id]['platform'])
        update.message.reply_text(delaymsg)
    elif ch == "3":
        update.message.reply_text("All upcoming trains are: ")
        upcominglist = get_upcoming_trains(station, platform)


def tracktrain(bot, update):
    user = update.message.from_user
    txt = update.message.text.replace('.', ':')
    txt.lower()
    get_train_info(all_user_data[user.id]['station'],
                   all_user_data[user.id]['platform'], txt)


def get_train_info(station, platform, time):
    logger.info("getting train for %s station platform %s time %s",
                station, platform, time)


def get_upcoming_trains(station, platform):
    time = datetime.now().strftime('%Y-%m-%d %-I:%M%p').split()[1].lower()


def delayinfo(station, platform):
    logger.info("getting delay info for %s station %s platform",
                station, platform)
    return 'No delays! ;)'


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("761246133:AAG471ei8DYATbh3WLJK2wUoITDa5-cGq6U")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            STATION: [MessageHandler(Filters.text, station)],
            PLATFORM: [MessageHandler(Filters.text, platform)],
            ACTIONSELECT: [MessageHandler(Filters.text, actionselect)],
            TRACKTRAIN: [MessageHandler(Filters.text, tracktrain)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
