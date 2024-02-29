from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    username = State()
    password = State()
    finish = State()


class Login(StatesGroup):
    username = State()
    password = State()
    finish = State()


class Facebook(StatesGroup):
    fullname = State()
    phone = State()
    address = State()
    child = State()
    sinf = State()  # noqa
    finish = State()


DataUser = {
    "username": "",
    "password": ""
}