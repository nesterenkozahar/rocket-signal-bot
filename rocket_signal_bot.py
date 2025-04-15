import random
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# ==== НАСТРОЙКИ ====
API_TOKEN = os.getenv('API_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# ==== ИНИЦИАЛИЗАЦИЯ ====
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ==== КНОПКИ ====
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(KeyboardButton("🚀 Сгенерировать сигнал"))

# ==== ФУНКЦИИ ====
def generate_fake_signal():
    entry_point = round(random.uniform(1.20, 1.80), 2)
    exit_point = round(entry_point + random.uniform(0.20, 0.60), 2)
    delay = random.randint(10, 60)  # задержка до запуска (секунды)
    return f"🚀 *Сигнал Ракета 1win!*\n\\n🕐 Через: {delay} секунд\\n🎯 Вход до: {entry_point}x\\n🏁 Выход до: {exit_point}x\\n\\nУдачи! 🍀"

# ==== ХЕНДЛЕРЫ ====
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Привет, админ! Добро пожаловать.", reply_markup=admin_keyboard)
    else:
        await message.answer("Этот бот закрыт для общего доступа.")

@dp.message_handler(commands=['signal'])
async def cmd_signal(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У тебя нет доступа к этой команде.")
    signal = generate_fake_signal()
    await message.answer(signal, parse_mode="Markdown")

@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Админ-панель:", reply_markup=admin_keyboard)

@dp.message_handler(lambda message: message.text == "🚀 Сгенерировать сигнал")
async def generate_signal_button(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        signal = generate_fake_signal()
        await message.answer(signal, parse_mode="Markdown")

# ==== ЗАПУСК ====
if __name__ == '__main__':
    print("Бот запущен")
    executor.start_polling(dp, skip_updates=True)