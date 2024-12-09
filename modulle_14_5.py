from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import sqlite3
from crud_functions import initiate_db, get_all_products, add_user, cursor, is_included

initiate_db()
get_all_products()
cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)",
               (1, "Продукт 1", "Описание 1", 1*100))

cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)",
               (2, "Продукт 2", "Описание 2", 2*100))

cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)",
               (3, "Продукт 3", "Описание 3", 3*100))

cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)",
               (4, "Продукт 4", "Описание 4", 4*100))


api = "7851068097:AAHvhKaHq_29ZZoboHIcmhdruPaZJLROSmE"

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()

button_calc = KeyboardButton(text="Рассчитать")
button_info = KeyboardButton(text="Информация")
button_buy = KeyboardButton(text="Купить")
button_reg = KeyboardButton(text="Регистрация")

kb.add(button_calc)
kb.add(button_info)
kb.add(button_buy)
kb.add(button_reg)


ikb = InlineKeyboardMarkup()
in_button_calc = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button_get_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

ikb.add(in_button_calc)
ikb.add(in_button_get_formulas)



ikb_product_list = InlineKeyboardMarkup()

btn_p_first = InlineKeyboardButton(text="Product1", callback_data="product_buying")
btn_p_second = InlineKeyboardButton(text="Product2", callback_data="product_buying")
btn_p_third = InlineKeyboardButton(text="Product3", callback_data="product_buying")
btn_p_fourth = InlineKeyboardButton(text="Product4", callback_data="product_buying")

ikb_product_list.add(btn_p_first)
ikb_product_list.add(btn_p_second)
ikb_product_list.add(btn_p_third)
ikb_product_list.add(btn_p_fourth)



kb.resize_keyboard = True


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start_registration(message: types.Message):
    await message.answer("Введите 'Регистрация' для начала.")


@dp.message_handler(lambda message: message.text.lower() == 'регистрация')
async def sing_up(message: types.Message):
    await RegistrationState.username.set()
    await message.answer("Введите имя пользователя (только латинский алфавит):")


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя.")
    else:
        await state.update_data(username=message.text)
        await RegistrationState.email.set()
        await message.answer("Введите свой email:")


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await RegistrationState.age.set()
    await message.answer("Введите свой возраст:")


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    username = user_data.get('username')
    email = user_data.get('email')
    age = user_data.get('age')
    add_user(username, email, age)
    await message.answer("Регистрация завершена!")
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)



@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('.venv/files/Product1.png', 'rb') as img:
        cursor.execute("SELECT * FROM Products WHERE id == 1")
        first_args = cursor.fetchall()
        await message.answer(f'Название: {first_args[0][1]} | Описание: {first_args[0][2]} | Цена: {first_args[0][3]}')
        await message.answer_photo(img)

    with open('.venv/files/Product2.png', 'rb') as img:
        cursor.execute("SELECT * FROM Products WHERE id == 2")
        second_args = cursor.fetchall()
        await message.answer(f'Название: {second_args[0][1]} | Описание: {second_args[0][2]} | Цена: {second_args[0][3]}')
        await message.answer_photo(img)

    with open('.venv/files/Product3.png', 'rb') as img:
        cursor.execute("SELECT * FROM Products WHERE id == 3")
        third_args = cursor.fetchall()
        await message.answer(f'Название: {third_args[0][1]} | Описание: {third_args[0][2]} | Цена: {third_args[0][3]}')
        await message.answer_photo(img)

    with open('.venv/files/Product4.png', 'rb') as img:
        cursor.execute("SELECT * FROM Products WHERE id == 4")
        fourth_args = cursor.fetchall()
        await message.answer(f'Название: {fourth_args[0][1]} | Описание: {fourth_args[0][2]} | Цена: {fourth_args[0][3]}')
        await message.answer_photo(img)

    await message.answer("Выберите товар для покупки:", reply_markup=ikb_product_list)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Сайт из задания не работал, поэтому искал в инете:  (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5)
    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал в день.')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
