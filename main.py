from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "7517278611:AAFD4-6ccU5ZHG0PmNncx7OrEz_U3xs0WDg"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = InlineKeyboardMarkup()
buton = InlineKeyboardButton(text="'Рассчитать норму калорий' ", callback_data="calories")
buton1 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kb.add(buton)
kb.add(buton1)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)


###
@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте')


@dp.message_handler(text='Рассчитать')
async def maim(message):
    await message.answer('Выберите опцию', reply_markup=kb)


###



@dp.callback_query_handler(text='formulas')
async def formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def qwerty(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()



@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    await message.answer(f"ваша норма калорий {result}")
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer("Введи команду /start,что бы начать наше общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
