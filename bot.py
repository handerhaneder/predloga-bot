import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, CREATOR_ID
from database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database()


def get_main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text="📨 Послать запрос на совместный блог")]]
    if user_id == CREATOR_ID:
        buttons.append([KeyboardButton(text="📋 Посмотреть запросы")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в <b>писмо хандеру</b>!\n\n"
        "Хочешь вести совместный блог? Отправь запрос — и я передам его создателю.\n\n"
        "Выбери действие ниже ",
        parse_mode="HTML",
        reply_markup=get_main_keyboard(message.from_user.id)
    )


@dp.message(F.text == "📨 Послать запрос на совместный блог")
async def send_request(message: types.Message):
    user = message.from_user

    # Collect user info
    username = f"@{user.username}" if user.username else "нет username"
    full_name = user.full_name or "нет имени"
    user_id = user.id

    # Save request to DB
    db.add_request(user_id=user_id, full_name=full_name, username=username)

    # Notify creator
    try:
        await bot.send_message(
            chat_id=CREATOR_ID,
            text=(
                f"🔔 <b>Новый запрос на совместный блог!</b>\n\n"
                f"👤 Имя: {full_name}\n"
                f"🔗 Username: {username}\n"
                f"🆔 ID: <code>{user_id}</code>\n\n"
                f"<a href='tg://user?id={user_id}'>📩 Написать напрямую</a>"
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.warning(f"Не удалось уведомить создателя: {e}")

    await message.answer(
        "✅ <b>Запрос отправлен!</b>\n\n"
        "Создатель блога получил твои контактные данные и скоро свяжется с тобой. 🎉",
        parse_mode="HTML"
    )


@dp.message(F.text == "📋 Посмотреть запросы")
async def view_requests(message: types.Message):
    if message.from_user.id != CREATOR_ID:
        await message.answer("⛔ У тебя нет доступа к этой функции.")
        return

    requests = db.get_all_requests()

    if not requests:
        await message.answer("📭 Запросов пока нет.")
        return

    text = f"📋 <b>Все запросы ({len(requests)}):</b>\n\n"
    for i, req in enumerate(requests, 1):
        text += (
            f"{i}. 👤 <b>{req['full_name']}</b>\n"
            f"   🔗 {req['username']}\n"
            f"   🆔 <code>{req['user_id']}</code>\n"
            f"   <a href='tg://user?id={req['user_id']}'>📩 Написать</a>\n"
            f"   📅 {req['date']}\n\n"
        )

    # Split if too long
    if len(text) > 4000:
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for chunk in chunks:
            await message.answer(chunk, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)


async def main():
    logger.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
