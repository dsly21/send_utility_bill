import os
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
COLD_WATER_TARIFF = 37.40
ELECTRICITY_TARIFF = 3.75


async def get_utility_values(input_message: str, utility_type: str):
    utility_list = list(filter((lambda i: i.isdigit()), input_message.split(' ')))

    for i in utility_list:
        if utility_type == 'electricity' and len(i) == 5:
            return i
        return i


async def calculate_utility(input_utility_value: int, utility_type_tariff: int):
    return input_utility_value * utility_type_tariff


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am a bot that can respond to messages containing the phrase'
                              ' "counter readings". Send me a message to get started!')


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()
    if 'показания' in message_text:

        cold_water_sum_to_pay = await get_utility_values(message_text, 'water')
        electricity_sum_to_pay = await get_utility_values(message_text, 'electricity')

        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f'За холодную воду {cold_water_sum_to_pay}, за электричество {electricity_sum_to_pay}',
        )


# Define the main function that runs the bot
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT, handle_messages)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
