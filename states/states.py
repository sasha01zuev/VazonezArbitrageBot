from aiogram.fsm.state import StatesGroup, State


# Пример группы состояний. Нет смысла один стейт в группе
class ExampleGroup(StatesGroup):
    ExampleState1 = State()
    ExampleState2 = State()


# Пример одиночного состояния
ExampleSoloState = State()
