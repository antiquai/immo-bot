import logging
import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from db_controller import fetch_data, fetch_latest_flats, sync_with_site

# Te reach database-file everywhere
normalize_db_path = os.path.dirname(os.path.abspath(__file__))

# Loading environments variables: API Token, URL ---
load_dotenv()

token = os.getenv("BOT_TOKEN")
url = os.getenv("url")

# Connecting Bot via API ---
bot = Bot(token=token)
dp = Dispatcher()

# Keyboard under Input field ---
def get_reply_keyboard():
    buttons = [
        [KeyboardButton(text="🏙️ List of cities -- Coming SOON")],
        [KeyboardButton(text="📊 Full flats list"), KeyboardButton(text="🔄 Update list")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие в меню"
    )
    # resize_keyboard=True - make buttons smaller and compatible for user experience
    # input_field_placeholder - text in input field, tip

    return keyboard

# Prepare answer in message format ---
def format_message(exm):
    # Master answer
    message = '<b>Flats List for recent time: </b>\n\n'

    # Formate every item of the list in specific design
    for i, (href, price, time) in enumerate(exm, start=1):
        message += (
            f'<a href="{href}"> Flat {i} </a> - {price}\n'
        )

    return message

###

# Logic of Bot answers ----

# Reply on Start Bot or /start Command
@dp.message(CommandStart())
async def command_start_handler(message) -> None:
    await message.answer(f"<b>Hello, {(message.from_user.full_name)}! 👋</b>\n I´m gonna provide you some Flats in Hamburg!\n(new fetchers coming soon)", parse_mode ="HTML", reply_markup=get_reply_keyboard())

# Reply on "Flat list"-button
@dp.message(F.text == '📊 Full flats list')
async def get_info_handler(message: types.Message):

    sync_with_site(url)

    flats = fetch_data(url)
    formate = format_message(flats)

    await message.answer(formate, parse_mode="HTML")

# Reply on "Update list"-button
@dp.message(F.text == "🔄 Update list")
async def update_handler(message: types.Message):
    await message.answer('<b>Got it!</b> Checking for new ads...', parse_mode="HTML")

    new_flats = sync_with_site(url)
    await asyncio.sleep(2)

    if not new_flats:
        recent_data = fetch_latest_flats(5)
        formate = format_message(recent_data)
        await message.answer('<b>No new flats found since last check.</b>', parse_mode="HTML")
        await asyncio.sleep(1)
        await message.answer(f"<b>Last 5 added:</b>\n\n{formate}", parse_mode="HTML")
    else:
        format_update = format_message(new_flats)
        await message.answer(f'<b>Found {len(new_flats)} new flats!</b>', parse_mode="HTML")
        await message.answer(format_update, parse_mode="HTML")



# Compiling of Bot ++ Logging --
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
