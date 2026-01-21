from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateOrEditProfileStatesGroup(StatesGroup):
    height = State()
    weight = State()
    gender = State()
    age = State()
    level_of_activities = State()

class SearchProductsStatesGroup(StatesGroup):
    q = State()

class SearchRecipesStatesGroup(StatesGroup):
    q = State()

class AddToDiaryStatesGroup(StatesGroup):
    get_group = State()
    get_volume = State()
    get_date = State()

class MailingStatesGroup(StatesGroup):
    get_message = State()
    get_confirmation = State()

class UnBlockUserStatesGroup(StatesGroup):
    get_username = State()