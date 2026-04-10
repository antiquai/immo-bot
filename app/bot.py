import logging
import os
import asyncio
import time

from parser import data_parser as d_p
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import sqlite3
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from db_controller import db_insert

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
        [KeyboardButton(text="🏙️ List of cities")],
        [KeyboardButton(text="📊 Full flats list"), KeyboardButton(text="🔄 Update list")]
    ]
    # resize_keyboard=True - make buttons smaller and compatible for user experience
    # input_field_placeholder - text in input field, tip
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие в меню"
    )
    return keyboard

# Fetching recent list from Database ---
def fetch_data(link):
    # Try setch data from DB. If there no DB use function from __db_controller.py__
    db_path = os.path.join(normalize_db_path, "data.db")

    def get_records():
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM flats')
            return cursor.fetchall()
    try:
        return get_records()
        
    except (sqlite3.OperationalError, sqlite3.DatabaseError):
        db_insert(d_p(link))
        return get_records()

# Updating list , and returning them if there are some new ---
def update_flats(link):
    # Parse site with function from __parser.py__
    data = d_p(link)

    db_path = os.path.join(normalize_db_path, "data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    before = cursor.connection.total_changes

    cursor.executemany(
        "INSERT OR IGNORE INTO flats (link, price) VALUES (?, ?)",
        [(l, p) for p, l in data]
    )

    # Fetching possible new Links after updating
    new_count = cursor.connection.total_changes - before

    conn.commit()
    conn.close()

    # Return amount of new Links (integer)
    return new_count

def fetch_latest_flats(lim):
    db_path = os.path.join(normalize_db_path, "data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Search every element in arrange of (maybe) new founded links
    cursor.execute("""
        SELECT link, price, created_at
        FROM flats
        ORDER BY created_at DESC
        LIMIT ?
    """, (lim,))

    data = cursor.fetchall()

    conn.close()

    return data

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
    flats = fetch_data(url)
    formate = format_message(flats)

    await message.answer(formate, parse_mode="HTML")

# Reply on "Update list"-button
@dp.message(F.text == "🔄 Update list")
async def update_handler(message: types.Message):
    await message.answer('<b>Got it!</b>, im gonna try to refresh it', parse_mode="HTML")

    await asyncio.sleep(2)

    new_count = update_flats(url)

    if new_count == 0:
        recent_data = fetch_latest_flats(5)
        formate = format_message(recent_data)
        await message.answer('<b>There is no new flats, please try again later, or see latest List! :) </b>', parse_mode="HTML")
        await asyncio.sleep(1)
        await message.answer(f"<b>{formate}</b>\n\n", parse_mode="HTML")
    else:
        new_flats = fetch_latest_flats(new_count)
        format_update = format_message(new_flats)
        await message.answer(f'<b>Found {new_count} new flats!</b>', parse_mode="HTML")
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
