from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

kb = [
    [KeyboardButton(text="Login"), KeyboardButton(text="Register")]
]

keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Choose Button")

check = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Submit", callback_data="submit")],
    [InlineKeyboardButton(text="Obuna", url="https://t.me/pdp_channel")]
])
