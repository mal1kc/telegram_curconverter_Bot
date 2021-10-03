
from os import getenv
from dotenv import load_dotenv
from src.get_curency import convert,CODES
from re import findall
from json import loads

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# for debug purposes
from pprint import pprint

# load environment variables(such as BOT_TOKEN) from .env file
load_dotenv()

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('''Help!
        usages examples // 
            -- <from_currency> <amount> <to_currency>
                # eur 1 usd --> 1 eur is ** usd
                # usd 1 eur --> 1 usd is ** eur 
                              ''')


def currency_convert(update: Update, context: CallbackContext) -> None:
    print(update.message.text)
    message_text = update.message.text.upper()
    extracted_currencies = findall(r'\w{3}',message_text)
    extracted_amount = findall(r'((\d{1,5})|([+-]?([0-9]*[.,])?[0-9]+))',message_text)
    try:
        if len(extracted_amount) > 1:
            # concat floating points
            extracted_amount = float(extracted_amount[0][0])+float(extracted_amount[1][0])
        else:
            # turn number to float
            extracted_amount = float(extracted_amount[0][0])
        if (extracted_currencies[0] in CODES.keys()) & (extracted_currencies[1] in CODES.keys()):
            result = loads(convert(extracted_currencies[0],extracted_currencies[1],extracted_amount))
            pprint(result)
            update.message.reply_text('{0:.2f} {1} is {2:.2f} {3} '.format(extracted_amount,result['from'],float(result['amount']),result['to']))
        else:
            update.message.reply_text(f'cannot find any currency like {extracted_currencies[0]} or {extracted_currencies[1]}')
    except Exception as exception:
        pprint(exception)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(getenv('BOT_TOKEN'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on message like eur 1 to usd  start currency_convert function

    dispatcher.add_handler(MessageHandler(Filters.regex(r'\w{3} ((\d{1,5})|([+-]?([0-9]*[.,])?[0-9]+)) \w{3}'), currency_convert))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
