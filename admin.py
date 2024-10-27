from aiogram import Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
import aiosqlite
from aiogram.fsm.context import FSMContext

ADMIN_ID = 7182216385  # Замените на ваш реальный ID администратора

# Функция для старта админ-панели
async def admin_start(message: Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Рассылка", callback_data="broadcast")],
            [InlineKeyboardButton(text="Логи", callback_data="logs")],
        ])
        await message.answer("Добро пожаловать в админ-панель!\nВыберите действие:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет доступа к админ-панели.")

# Начало процесса рассылки
async def broadcast_start(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id == ADMIN_ID:
        await callback_query.message.answer("Введите сообщение для рассылки:")
        await state.update_data(broadcast_next=True)

# Реализация рассылки всем пользователям
async def broadcast_message(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("broadcast_next"):
        return

    await state.update_data(broadcast_next=False)  # Сброс состояния после запуска рассылки

    # Подключаемся к базе данных и получаем всех пользователей
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT user_id FROM users WHERE is_active=1") as cursor:
            async for row in cursor:
                user_id = row[0]
                try:
                    await message.bot.send_message(user_id, message.text)
                    print(f"Сообщение отправлено пользователю: {user_id}")
                except Exception as e:
                    # Обработка ошибок при отправке сообщения
                    print(f"Ошибка при отправке пользователю {user_id}: {e}")

    await message.answer("Сообщение разослано всем активным пользователям.")

# Обработчик callback для рассылки
async def admin_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "broadcast":
        await broadcast_start(callback_query, state)

#команд админа
def register_admin_handlers(dp: Dispatcher):
    dp.message.register(admin_start, Command("admin"))
    dp.message.register(broadcast_message)

    #callback для админ-панели
    dp.callback_query.register(admin_callback_handler)

