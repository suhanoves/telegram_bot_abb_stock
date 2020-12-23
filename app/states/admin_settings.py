from aiogram.dispatcher.filters.state import StatesGroup, State


class AddUser(StatesGroup):
    AddUser = State()
    AddFirstName = State()
    AddLastName = State()
    AddUsername = State()
    AddPhone = State()
    AddEmail = State()
    AddIsAllowed = State()
    AddIsAdmin = State()


class ChangeUserParams(StatesGroup):
    GetUser = State()
    ChooseParams = State()
    ChangeFirstName = State()
    ChangeLastName = State()
    ChangeUsername = State()
    ChangePhone = State()
    ChangeEmail = State()
    ChangeIsAllowed = State()
    ChangeIsAdmin = State()


class DelUser(StatesGroup):
    GetUser = State()
    ConfirmDel = State()
