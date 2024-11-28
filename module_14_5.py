from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from crud_functions import *


get_all_products()
api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="Рассчитать")],
    [KeyboardButton(text="Информация")],
    [KeyboardButton(text='Купить')],
    [KeyboardButton(text='Регистрация')]
    ],
    resize_keyboard=True
        )

kb_inline = InlineKeyboardMarkup()
button_formula = InlineKeyboardButton(text='Формулы расчёта',  callback_data='formulas')
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kb_inline.add(button_calories)
kb_inline.add(button_formula)

kb_shop_inline = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
button_2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
button_3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
button_4 = InlineKeyboardButton(text='Product4', callback_data="product_buying")
kb_shop_inline.add(button_1)
kb_shop_inline.add(button_2)
kb_shop_inline.add(button_3)
kb_shop_inline.add(button_4)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb_inline)

@dp.message_handler(text = 'Информация')
async def InFo(message):
    await message.answer("Тут скоро появится информация!")

@dp.message_handler(text= 'Купить')
async def get_buying_list(message):
    products = get_all_products()
    if products:
        for product in products:
            id, title, description, price = product
            await message.answer(f'Название: {title}| Описание: {description}| Цена: {price}')
            with open(f'product_{id}.jpg', 'rb') as img:
                await message.answer_photo(img)
        await message.answer('Выберите продукт для покупки:', reply_markup=kb_shop_inline)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = start_menu)
    await message.answer('Введите "Рассчитать" что бы начать рассчет вашей нормы каллорий')

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if not is_included(username):
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя:")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Ваш баланс: {1000}')
    data = await state.get_data()
    result = add_user(data['username'], data['email'], data['age'])
    if result:
        await message.answer("Регистрация успешна!")
        await state.finish()
    else:
        await message.answer("Ошибка при регистрации. Попробуйте снова.")
        await state.finish()
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight= message.text)
    await message.answer('Введите пол "м" или "ж":')
    await UserState.sex.set()

@dp.message_handler(state= UserState.sex)
async def send_calories(message, state):
    await state.update_data(sex= message.text)
    data = await state.get_data()
    if data["sex"].lower() == "м":
        calories_men = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
        await message.answer(f'Ваша норма колорий: {calories_men}')
    if data["sex"].lower() == "ж":
        calories_women = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
        await message.answer(f'Ваша норма колорий: {calories_women}')
        await state.finish()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
                              ' \nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)