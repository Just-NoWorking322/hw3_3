from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

router = Router()

def get_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Помощь")
    builder.button(text="Контакты")
    builder.adjust(2) 
    return builder.as_markup(resize_keyboard=True)

def get_inline_keyboard():
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть сайт", url="https://animego.org/anime/sharlotta-713"
                )
            ]
        ]
    )
    return inline_keyboard

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
       """Привет! Рад вас приветствовать в нашем TG боте 
        Выберите /game чтобы сыграть в игру
        Выберите /help чтоб узнать о нас по-больше
        """,
        reply_markup=get_reply_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Используйте команды:\n"
        "/start - начать работу\n"
        "/help - показать справку\n\n"
        "Используйте кнопки ниже для взаимодействия!",
        reply_markup=get_inline_keyboard()
    )
    

random_number = random.randint(1, 3)

@router.message(Command('game'))
async def start(message: types.Message):
    global random_number
    random_number = random.randint(1, 3) 
    await message.answer("Я загадал число от 1 до 3, угадайте!")

@router.message()
async def guess_number(message: types.Message):
    global random_number
    try:
        user_guess = int(message.text)
        if 1 <= user_guess <= 3:
            if user_guess == random_number:
                await message.answer("Правильно! Вы отгадали!")
                random_number = random.randint(1, 3)  
            else:
                await message.answer("Неправильно, попробуйте еще раз!")
        else:
            await message.answer("Пожалуйста, введите число от 1 до 3.")
    except ValueError:
        await message.answer("Это не число! Введите число от 1 до 3.")


@router.message(lambda message: message.text == "Контакты")
async def contacts_handler(message: types.Message):
    await message.answer("Наши контакты:\nТелефон: +996 504 07 77 00\nEmail: alisherbolotbekov03@gmail.com")

@router.message(lambda message: message.text == "Помощь")
async def help_button_handler(message: types.Message):
    await cmd_help(message)

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())