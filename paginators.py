import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date, timedelta
import calendar

class Paginator:
    def __init__(self, data, callback_prefix, back_callback, type, width, second_type, item_prefix=None, height=None, category_id=None, back_button: str = "⏪", next_button: str = "⏩"):
        self.__data = data
        self.__callback_prefix = callback_prefix
        self.__item_prefix = item_prefix
        self.__back_callback = back_callback
        self.__type = type
        self.__width = width
        self.__height = height
        self.__category_id = category_id
        self.__second_type = second_type
        self.__back_button = back_button
        self.__next_button = next_button

    def __get_page_info_buttons(self, current_page):
        if self.__type == "list" or self.__type == "itemlist":
            if len(self.__data) % (self.__height * self.__width) == 0:
                count_of_pages = len(self.__data) // (self.__height * self.__width) - 1
            else:
                count_of_pages = math.floor(len(self.__data) / (self.__height * self.__width))
        else:
            count_of_pages = len(self.__data) - 1

        buttons = []
        if count_of_pages != 0:
            if current_page != 0:
                buttons.append(InlineKeyboardButton(text=self.__back_button,
                                                    callback_data=f"{self.__callback_prefix}_{current_page - 1}"))

            buttons.append(InlineKeyboardButton(text=f"{current_page + 1}/{count_of_pages + 1}", callback_data="_"))

            if current_page != count_of_pages:
                buttons.append(InlineKeyboardButton(text=self.__next_button,
                                                    callback_data=f"{self.__callback_prefix}_{current_page + 1}"))

        return buttons

    def __get_page_data_buttons(self, current_page, item_pages, option):
        if self.__type == "list":
            data = self.__data[
                   current_page * self.__width * self.__height:(current_page + 1) * self.__width * self.__height]
            item_pages = item_pages[
                         current_page * self.__width * self.__height:(current_page + 1) * self.__width * self.__height]

            return [InlineKeyboardButton(text=d[1], callback_data=f"{self.__item_prefix}_{d[0]}_{item_pages[i]}") for
                    i, d in enumerate(data)]
        elif self.__type == 'itemlist':
            data = self.__data[
                   current_page * self.__width * self.__height:(current_page + 1) * self.__width * self.__height]
            item_pages = item_pages[
                         current_page * self.__width * self.__height:(current_page + 1) * self.__width * self.__height]

            return [InlineKeyboardButton(text=d[1] if d[1] else d[2],
                                         callback_data=f"{self.__item_prefix}_{self.__category_id}_{item_pages[i]}") for
                    i, d in enumerate(data)]
        else:
            if self.__second_type == "mailings":
                if option == 0:
                    return [InlineKeyboardButton(text="➡️ Возобновить", callback_data=f"restartmailing_{self.__data[current_page][0]}_{current_page}")]
                elif option == 1:
                    return [InlineKeyboardButton(text="✖️ Отменить", callback_data=f"cancelmailing_{self.__data[current_page][0]}_{current_page}")]
                return []
            elif self.__second_type == "blockusers":
                if option == True:
                    return [InlineKeyboardButton(text="🤵 Разблокировать", callback_data=f"unblockuser_{self.__data[current_page][0]}_{current_page}")]
                elif option == False:
                    return [InlineKeyboardButton(text="🙅‍♂️ Заблокировать", callback_data=f"blockuser_{self.__data[current_page][0]}_{current_page}")]
                return []
            else:
                buttons = [InlineKeyboardButton(text="✍️ Записать", callback_data=f"adddiary_{self.__second_type}_{self.__data[current_page][0]}_{current_page}")]

                if not option:
                    return buttons + [InlineKeyboardButton(text="➕ Добавить в избранное",
                                                callback_data=f"addfavorite_{self.__second_type}_{self.__data[current_page][0]}_{current_page}")]

                return buttons + [InlineKeyboardButton(text="❌ Удалить из избранного",
                                            callback_data=f"delfavorite_{self.__second_type}_{self.__data[current_page][0]}_{current_page}")]

    def get_page_keyboard(self, data, item_pages=None, option=None):
        current_page = self.__format_page(data)
        data_page_buttons = self.__get_page_data_buttons(current_page, item_pages, option)
        info_page_buttons = self.__get_page_info_buttons(current_page)

        markup = InlineKeyboardMarkup(row_width=self.__width)
        markup.add(*data_page_buttons)
        markup.row(*info_page_buttons)
        if self.__second_type == "products" or self.__second_type == "recipes":
            markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data=self.__back_callback),
                   InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))
        else:
            markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data=self.__back_callback),
                   InlineKeyboardButton(text="🏠 Админская панель", callback_data="admin_panel"))


        return markup

    def __format_page(self, current_page):
        if isinstance(current_page, str):
            return int(current_page.split("_")[-1])
        return current_page

    def get_data(self):
        return self.__data

    def get_page_by_data_ind(self, data_ind):
        return int(data_ind / (self.__height * self.__width))

    @property
    def back_callback(self):
        return self.__back_callback

    @back_callback.setter
    def back_callback(self, value):
        self.__back_callback = value

class PaginatorDiary:
    @classmethod
    def init(cls, callback_prefix, back_callback, row_width=1, back_button: str = "⏪", next_button: str = "⏩"):
        cls.__callback_prefix = callback_prefix
        cls.__back_callback = back_callback
        cls.__row_width = row_width
        cls.__back_button = back_button
        cls.__next_button = next_button

    @classmethod
    def __get_page_info_buttons(cls, current_date):
        return [InlineKeyboardButton(text=cls.__back_button, callback_data=f"{cls.__callback_prefix}_{current_date - timedelta(days=1)}"), InlineKeyboardButton(text=f"{current_date}", callback_data="_"), InlineKeyboardButton(text=cls.__next_button, callback_data=f"{cls.__callback_prefix}_{current_date + timedelta(days=1)}")]

    @classmethod
    def __get_page_data_buttons(cls, current_date, flag):
        if flag:
            return [InlineKeyboardButton(text="✏️ Изменить", callback_data=f"editdiary_{current_date}")]
        return []

    @classmethod
    def get_page_keyboard(cls, data, flag):
        current_data = cls.__format_page(data)
        data_page_buttons = cls.__get_page_data_buttons(current_data, flag)
        info_page_buttons = cls.__get_page_info_buttons(current_data)

        markup = InlineKeyboardMarkup(row_width=cls.__row_width)
        markup.add(*data_page_buttons)
        markup.row(*info_page_buttons)
        markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data=cls.__back_callback),
                   InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

        return markup

    @staticmethod
    def __format_page(current_data):
        if isinstance(current_data, str):
            return date.fromisoformat(current_data)
        return current_data


class PaginatorCalendar:
    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @classmethod
    def init(cls, callback_prefix, row_width=1, back_button: str = "⏪", next_button: str = "⏩"):
        cls.__callback_prefix = callback_prefix
        cls.__row_width = row_width
        cls.__back_button = back_button
        cls.__next_button = next_button

    @classmethod
    def __get_page_info_buttons(cls, current_date):
        return [InlineKeyboardButton(text=cls.__back_button,
                                     callback_data=f"{cls.__callback_prefix}_{cls.add_months(current_date, -1)}"),
                InlineKeyboardButton(text=f"{current_date.month if (len(str(current_date.month)) > 1) else f'0{current_date.month}'}.{current_date.year}", callback_data="_"),
                InlineKeyboardButton(text=cls.__next_button,
                                     callback_data=f"{cls.__callback_prefix}_{(cls.add_months(current_date, 1))}")]

    @classmethod
    def __get_page_data_buttons(cls, current_date):
        week_day, last_day = calendar.monthrange(current_date.year, current_date.month)

        before_date = cls.add_months(current_date, -1)
        before_date = date(before_date.year, before_date.month, calendar.monthrange(before_date.year, before_date.month)[1])
        last_date = date(current_date.year, current_date.month, last_day)

        markup = [InlineKeyboardButton((before_date - timedelta(days=days)).strftime('%d.%m'), callback_data=f"choosedate_{before_date - timedelta(days=days)}") for days in range(week_day - 1, -1, -1)] + [InlineKeyboardButton(str(day + 1), callback_data=f"choosedate_{current_date.strftime('%Y-%m')}-{day + 1 if len(str(day + 1)) > 1 else f'0{day + 1}'}") for day in range(last_day)]

        if len(markup) % 7 != 0:
            markup += [InlineKeyboardButton((last_date + timedelta(days=days)).strftime('%d.%m'), callback_data=f"choosedate_{last_date + timedelta(days=days)}") for days in range(1, (36 if len(markup) < 36 else 43)- len(markup))]

        return markup

    @classmethod
    def get_page_keyboard(cls, data, back_callback):
        current_data = cls.__format_page(data)
        data_page_buttons = cls.__get_page_data_buttons(current_data)
        info_page_buttons = cls.__get_page_info_buttons(current_data)

        markup = InlineKeyboardMarkup(row_width=cls.__row_width)
        markup.add(*data_page_buttons)
        markup.row(*info_page_buttons)
        markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data=back_callback),
                   InlineKeyboardButton(text="✖️ Отмена", callback_data="cancel"))

        return markup

    @staticmethod
    def __format_page(current_data):
        if isinstance(current_data, str):
            return date.fromisoformat(current_data)
        return current_data