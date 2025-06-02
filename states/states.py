from aiogram.fsm.state import StatesGroup, State


# Пример группы состояний. Нет смысла один стейт в группе
class ExampleGroup(StatesGroup):
    ExampleState1 = State()
    ExampleState2 = State()


# Пример одиночного состояния
ExampleSoloState = State()


class SetSpreadGroup(StatesGroup):
    SetMaxSpread = State()
    SetMinSpread = State()


class SetProfitGroup(StatesGroup):
    SetMaxProfit = State()
    SetMinProfit = State()


class SetVolumeGroup(StatesGroup):
    SetMaxVolume = State()
    SetMinVolume = State()
