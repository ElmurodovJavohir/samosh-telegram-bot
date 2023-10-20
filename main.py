import logging
from typing import Dict
from db import get_category_all, get_category_id_by_name, get_category_product
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


logger = logging.getLogger(__name__)

CAT_CHOOSING, PRODUCT, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['☎️ Biz bilan aloqa', '🛍 Buyurtma berish'],
    ['✍️ Fikr bildirish', '⚙️ Sozlamalar'],
]
main_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


# def facts_to_str(user_data: Dict[str, str]) -> str:
#     """Helper function for formatting the gathered user info."""
#     facts = [f'{key} - {value}' for key, value in user_data.items()]
#     return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Davom etamizmi? 😉",
        reply_markup=main_markup,
    )
    return ConversationHandler.END


def category(update: Update, context: CallbackContext) -> int:
    categories = get_category_all()
    categories_keyboard = []
    for i in range(0, len(categories), 2):

        categories_keyboard.append(
            [cat.title for cat in categories[i:i+2]]
        )
    categories_markup = ReplyKeyboardMarkup(
        categories_keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Kerakli kategoriyani tanlang:",
        reply_markup=categories_markup,
    )

    return CAT_CHOOSING


def cat_choosing(update: Update, context: CallbackContext) -> int:
    category = get_category_id_by_name(update.message.text)
    if category:
        products = get_category_product(category.id)
        products_keyboard = []
        for i in range(0, len(products), 2):

            products_keyboard.append(
                [product.title for product in products[i:i+2]]
            )
        products_markup = ReplyKeyboardMarkup(
            products_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "Kerakli mahsulotni tanlang.",
            reply_markup=products_markup,
        )
        return PRODUCT
    else:
        categories = get_category_all()

        categories_keyboard = []
        for i in range(0, len(categories), 2):

            categories_keyboard.append(
                [cat.title for cat in categories[i:i+2]]
            )
        categories_markup = ReplyKeyboardMarkup(
            categories_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "unday kategoriya mavjud emas, Kerakli kategoriyani tanlang:",
            reply_markup=categories_markup,
        )

        return CAT_CHOOSING


def product(update: Update, context: CallbackContext) -> int:
    category = get_category_product(update.message.text)
    if category:
        update.message.reply_text(
            category.id,
        )

    else:
        categories = get_category_all()

        categories_keyboard = []
        for i in range(0, len(categories), 2):

            categories_keyboard.append(
                [cat.title for cat in categories[i:i+2]]
            )
        categories_markup = ReplyKeyboardMarkup(
            categories_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "unday kategoriya mavjud emas, Kerakli kategoriyani tanlang:",
            reply_markup=categories_markup,
        )

        return CAT_CHOOSING


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("6531447481:AAEXuCv5_ntHp6-ThTtPwzOeXsbaOa_kbXM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.text("🛍 Buyurtma berish"), category),
        ],
        states={
            CAT_CHOOSING: [
                MessageHandler(
                    Filters.text & ~Filters.command, cat_choosing
                ),

            ],
            PRODUCT: [
                MessageHandler(
                    Filters.text & ~Filters.command, product
                ),

            ],
            # TYPING_CHOICE: [
            #     MessageHandler(
            #         Filters.text & ~(Filters.command | Filters.regex(
            #             '^Done$')), regular_choice
            #     )
            # ],
            # TYPING_REPLY: [
            #     MessageHandler(
            #         Filters.text & ~(Filters.command |
            #                          Filters.regex('^Done$')),
            #         received_information,
            #     )
            # ],
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(Filters.text("🛍 Buyurtma berish"), category),

            # MessageHandler(Filters.regex('^Done$'), done)
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
