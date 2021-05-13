#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 23:39:01 2021

@author: LordViola
"""

import logging
from threading import Thread
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

#from  bot2 import cspattern
from  bot3 import cspattern


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def signals(update: Update, context: CallbackContext) -> None:
    thread = cspattern('Thread', context.bot, update.message.from_user.id)
    thread.start()
    thread.join()


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1564604813:AAGK0Tj3_Ow1mP2SH8-oo05cCuP0bwSv6GY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("bot1", signals, run_async=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
