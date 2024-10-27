from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command


async def shop(message: Message):
    """
    Display the available products in the shop. This function sends a message with a list
    of products that users can buy, each with a button for purchasing.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить товар 1", callback_data="buy_1")],
        [InlineKeyboardButton(text="Купить товар 2", callback_data="buy_2")],
    ])
    await message.answer("В магазине доступны следующие товары:", reply_markup=keyboard)


async def handle_purchase(callback_query):
    """
    Handle the purchase logic when a user clicks on the buy button.
    """
    if callback_query.data == "buy_1":
        await callback_query.message.answer("Вы купили товар 1!")
    elif callback_query.data == "buy_2":
        await callback_query.message.answer("Вы купили товар 2!")
    await callback_query.answer()


# хз как доделать
def register_shop_handlers(dp: Dispatcher):
    """
    Registers shop-related commands and callback handlers.
    """
    dp.message.register(shop, Command('shop'))
    dp.callback_query.register(handle_purchase)
