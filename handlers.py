from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

animals = ['Кошка', 'Собака']
weight = ['1', '3', '5', '15', '25']


class RequestFood(StatesGroup):
    waiting_for_pet_choice = State()
    waiting_for_weight = State()


async def start_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button = "Выбрать корм"
    keyboard.add(button)
    await message.reply("""Здравствуйте! Здесь вы найдете лучший корм для вашего любимца!)\n 
Если у вас есть вопросы или предложения - напишите нашему менеджеру!\nКонтакты:""", reply_markup=keyboard)


async def food_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for animal in animals:
        keyboard.add(animal)
    await message.answer("Какой у вас питомец?", reply_markup=keyboard)
    await state.set_state(RequestFood.waiting_for_pet_choice.state)


async def size_chosen(message: types.Message, state: FSMContext):
    if message.text.capitalize() not in animals:
        await message.answer("Пожалуйста, выберите питомца, используя клавиатуру ниже.")
        return
    await state.update_data(animal=message.text.capitalize())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for size in weight:
        keyboard.add(size)
    await state.set_state(RequestFood.waiting_for_weight.state)
    await message.answer("Выберите нужный вес пачки корма (в килограммах)", reply_markup=keyboard)


async def product_output(message: types.Message, state: FSMContext):
    if message.text not in weight:
        await message.answer("Пожалуйста, выберите вес упаковки, используя клавиатуру ниже.")
        return

    data = await state.get_data()
    size = message.text
    await message.answer(f"Вот все доступные корма для {data['animal']} весом {size} килограм.",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start", state="*")
    dp.register_message_handler(food_start, regexp="Выбрать корм", state="*")
    dp.register_message_handler(food_start, commands="food", state="*")
    dp.register_message_handler(size_chosen, state=RequestFood.waiting_for_pet_choice)
    dp.register_message_handler(product_output, state=RequestFood.waiting_for_weight)
