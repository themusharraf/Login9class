import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.fsm.context import FSMContext
from buttons import keyboard, check
from form import Login, Facebook, Form, DataUser
from root import TOKEN, CHAT_ID

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer_photo(photo="https://images.app.goo.gl/cdLna1RTt8a82Rw89",
                               caption=f"Assalomu alekum kanalga obuna buling! {message.from_user.full_name}",
                               reply_markup=check)


@dp.callback_query(F.data == "submit")
async def callback_submit(call: CallbackQuery, bot: Bot):
    user_status = await bot.get_chat_member(chat_id=CHAT_ID, user_id=call.from_user.id)
    if user_status.status != "left":
        await bot.send_message(
            call.from_user.id, "✅"
        )
        await call.message.answer("Login or Register", reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text="Siz kanalga obuna bulmagansiz!", reply_markup=check)
        text = ("Kanalga obuna bo'lmagansiz ⚠️"
                )
        show_alert = True
        await call.answer(text, show_alert=show_alert)



    @dp.message()
    async def reg(message: Message, state: FSMContext):
        if message.text == "Register":
            await state.set_state(Form.name)
            await message.answer("Enter name")
        elif message.text == "Login":
            await state.set_state(Login.username)
            await message.answer("Enter username: ")
        elif message.text == "Ariz yuborish":
            await state.set_state(Facebook.fullname)
            await message.answer("Enter fullname: ")


@dp.message(Form.name)
async def usernames(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.username)
    await message.answer("Enter username")


@dp.message(Form.username)
async def passwords(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await message.answer("Enter password")


@dp.message(Form.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "You have successfully",
    )
    name = data.get("name", "Unknown")
    username = data.get("username", "Unknown")
    password = data.get("password", "Unknown")

    DataUser["username"] = username
    DataUser["password"] = password

    matn = f"🧑‍💻 Name: {name}\n⚡️ Username: {username}\n🔐 Password: {password}"
    btn = [
        [types.KeyboardButton(text="Ariz yuborish")]
    ]
    key = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
    await message.answer(text=matn, reply_markup=key)


@dp.message(Login.username)
async def login(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Login.password)
    await message.answer("Enter password: ")


@dp.message(Login.password)
async def finsh(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Login.finish)
    userdata = await state.get_data()
    await state.clear()
    username = userdata.get("username", "Unknown")
    password = userdata.get("password", "Unknown")
    if username == DataUser["username"] and password == DataUser["password"]:
        btn = [
            [types.KeyboardButton(text="Ariz yuborish")]
        ]
        key = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
        await message.answer("You have successfully login ✅", reply_markup=key)
    else:
        await message.answer("Invalid username or password ⁉️")


@dp.message(Facebook.fullname)
async def facebook(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(Facebook.phone)
    await message.answer("Enter your phone: ")


@dp.message(Facebook.phone)
async def facebook(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Facebook.address)
    await message.answer("Enter your address: ")


@dp.message(Facebook.address)
async def facebook(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Facebook.child)
    await message.answer("your child`s fullname: ")


@dp.message(Facebook.child)
async def facebook(message: Message, state: FSMContext):
    await state.update_data(child=message.text)
    await state.set_state(Facebook.sinf)
    await message.answer("Child`s class: ")


@dp.message(Facebook.sinf)
async def facebook(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(sinf=message.text)
    await state.set_state(Facebook.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer("Ariza qubul qilindi !")  # noqa
    fullname = data.get("fullname", "Unknown")
    phone = data.get("phone", "Unknown")
    address = data.get("address", "Unknown")
    child = data.get("child", "Unknown")
    sinf = data.get("sinf", "Unknown")  # noqa

    await message.answer(
        f"⚡️Fullname: {fullname}\n📞Phone: {phone}\n🗺Address: {address}\n👩Child: {child}\n🙎‍♂️Class: {sinf}")
    await bot.send_message(chat_id=CHAT_ID,
                           text=f"⚡️Fullname: {fullname}\n📞Phone: {phone}\n🗺Address: {address}\n👩Child: {child}\n🙎‍♂️Class: {sinf}")


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
