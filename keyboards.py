from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from config import channels

subscribe_markup = InlineKeyboardMarkup(row_width=2)
subscribe_markup.add(*[InlineKeyboardButton(channel.get("name", f"Канал {i}"),
                                            url=("https://t.me/" + channel["link"][1:]) if channel["link"].startswith(
                                                "@") else channel["link"]) for i, channel in enumerate(channels, 1)])
subscribe_markup.add(InlineKeyboardButton("✔️ Проверить", callback_data="check"))

menu_markup = InlineKeyboardMarkup(row_width=1)
menu_markup.add(InlineKeyboardButton(text="🍏 Узнать калорийность", callback_data="product_calories"),
                InlineKeyboardButton(text="🧮 Вычислить норму калорий", callback_data="person_calories"))
menu_markup.row(InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
                InlineKeyboardButton(text="👨‍💻 О нас", callback_data="about_us"))

product_calories_markup = InlineKeyboardMarkup(row_width=2)
product_calories_markup.add(InlineKeyboardButton(text="🍎 Калорийность продуктов", callback_data="products"))
product_calories_markup.add(InlineKeyboardButton(text="📝 Рецепты", callback_data="recipes"))
product_calories_markup.add(InlineKeyboardButton(text="❤️ Избранное", callback_data="favourites"),
                            InlineKeyboardButton(text="✍️ Мой дневник", callback_data="diary"),
                            InlineKeyboardButton(text="🏠 Меню", callback_data="menu"))

products_markup = InlineKeyboardMarkup(row_width=2)
products_markup.add(InlineKeyboardButton(text="📋 Список", callback_data="productscategories1_0_0"),
                    InlineKeyboardButton(text="🔍 Поиск", callback_data="search_products"),
                    InlineKeyboardButton(text="🔙 Назад", callback_data="product_calories"),
                    InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

recipes_markup = InlineKeyboardMarkup(row_width=2)
recipes_markup.add(InlineKeyboardButton(text="📋 Список", callback_data="recipescategories_0_0"),
                   InlineKeyboardButton(text="🔍 Поиск", callback_data="search_recipes"),
                   InlineKeyboardButton(text="🔙 Назад", callback_data="product_calories"),
                   InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

to_products_or_menu_markup = InlineKeyboardMarkup(row_width=2)
to_products_or_menu_markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data="products"),
                               InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

to_recipes_or_menu_markup = InlineKeyboardMarkup(row_width=2)
to_recipes_or_menu_markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data="recipes"),
                              InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

favourites_markup = InlineKeyboardMarkup(row_width=2)
favourites_markup.add(InlineKeyboardButton("🍎 Продукты", callback_data="favproducts_0_0"),
                      InlineKeyboardButton("📝 Рецепты", callback_data="favrecipes_0_0"),
                      InlineKeyboardButton(text="🔙 Назад", callback_data="product_calories"),
                      InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

choose_the_group_markup = InlineKeyboardMarkup(row_width=2)
choose_the_group_markup.add(InlineKeyboardButton(text="🍳 Завтрак", callback_data="breakfast"),
                            InlineKeyboardButton(text="🍜 Обед", callback_data="lunch"),
                            InlineKeyboardButton(text="🍝 Ужин", callback_data="dinner"),
                            InlineKeyboardButton(text="🍎 Перекус", callback_data="snack"))
choose_the_group_markup.add(InlineKeyboardButton(text="✖️ Отмена", callback_data="cancel"))

person_calories_markup = InlineKeyboardMarkup(row_width=1)
person_calories_markup.add(InlineKeyboardButton(text="🍱 Расчет калорий", callback_data="calories_count"),
                           InlineKeyboardButton(text="🧍 Расчет идеального веса и ИМТ", callback_data="imt_count"),
                           InlineKeyboardButton(text="👤 Мои данные", callback_data="my_profile"),
                           InlineKeyboardButton(text="🏠 Меню", callback_data="menu"))

to_menu_person_profile_markup = InlineKeyboardMarkup(row_width=1)
to_menu_person_profile_markup.add(InlineKeyboardButton(text="👤 Мои параметры", callback_data="my_profile"))
to_menu_person_profile_markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data="person_calories"),
                                  InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

create_user_profile_markup = InlineKeyboardMarkup(row_width=1)
create_user_profile_markup.add(InlineKeyboardButton(text="📝 Добавить данные", callback_data="create_or_edit_profile"))
create_user_profile_markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data="person_calories"),
                               InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

edit_user_profile_markup = InlineKeyboardMarkup(row_width=1)
edit_user_profile_markup.add(InlineKeyboardButton(text="📝 Изменить данные", callback_data="create_or_edit_profile"),
                             InlineKeyboardButton(text="🏃 Изменить свой уровень активности",
                                                  callback_data="edit_level_of_activities"))
edit_user_profile_markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data="person_calories"),
                             InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

finish_create_user_profile_markup = InlineKeyboardMarkup(row_width=1)
finish_create_user_profile_markup.add(
    InlineKeyboardButton(text="📝 Добавить данные", callback_data="finish_create_profile"))
finish_create_user_profile_markup.row(InlineKeyboardButton(text="🔙 Назад", callback_data="person_calories"),
                                      InlineKeyboardButton(text="🏠 В меню", callback_data="menu"))

choose_the_gender_markup = InlineKeyboardMarkup(row_width=2)
choose_the_gender_markup.add(InlineKeyboardButton(text="👨‍🦰 Мужчина", callback_data="male"),
                             InlineKeyboardButton(text="👩‍🦰 Женщина", callback_data="female"),
                             InlineKeyboardButton(text="✖️ Отмена", callback_data="cancel"))

choose_level_of_activities_markup = InlineKeyboardMarkup(row_width=3)
choose_level_of_activities_markup.add(InlineKeyboardButton(text="Минимальный", callback_data="0"),
                                      InlineKeyboardButton(text="Низкий", callback_data="1"),
                                      InlineKeyboardButton(text="Средний", callback_data="2"),
                                      InlineKeyboardButton(text="Высокий", callback_data="3"),
                                      InlineKeyboardButton(text="Очень высокий", callback_data="4"))
choose_level_of_activities_markup.add(InlineKeyboardButton(text="Как выбрать уровень физической активности?",
                                                           callback_data="how_choose_level_of_activities"))
choose_level_of_activities_markup.add(InlineKeyboardButton(text="✖️ Отмена", callback_data="cancel"))

to_choose_level_of_activities_markup = InlineKeyboardMarkup(row_width=1)
to_choose_level_of_activities_markup.add(
    InlineKeyboardButton(text="🔙 Назад", callback_data="to_choose_level_of_activities"))

to_menu_markup = InlineKeyboardMarkup(row_width=1)
to_menu_markup.add(InlineKeyboardButton(text="🏠 Меню", callback_data="menu"))

stats_markup = InlineKeyboardMarkup(row_width=1)
stats_markup.add(InlineKeyboardButton("👥 Кол-во пользователей", callback_data="count_of_users"),
                 InlineKeyboardButton("📈 Основная статистика", callback_data="main_stats"),
                 InlineKeyboardButton(text="🏠 Меню", callback_data="menu"))

count_of_users_markup = InlineKeyboardMarkup(row_width=2)
count_of_users_markup.add(InlineKeyboardButton(text="🔙 Назад", callback_data="stats_photo"),
                          InlineKeyboardButton(text="🏠 Меню", callback_data="menu_photo"))

main_stats_markup = InlineKeyboardMarkup(row_width=2)
main_stats_markup.add(InlineKeyboardButton(text="🔙 Назад", callback_data="stats"),
                      InlineKeyboardButton(text="🏠 Меню", callback_data="menu"))

cancel_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
cancel_markup.add(KeyboardButton(text="✖️ Отмена"))

remove_markup = ReplyKeyboardRemove()

admin_panel_markup = InlineKeyboardMarkup(row_width=1)
admin_panel_markup.add(InlineKeyboardButton("📨 Рассылки", callback_data="mailings"),
                       InlineKeyboardButton("👥 Пользователи", callback_data="users"),
                       InlineKeyboardButton("🖥 Логи", callback_data="logs"))

mailings_markup = InlineKeyboardMarkup(row_width=1)
mailings_markup.add(InlineKeyboardButton(text="🆕 Создать рассылку", callback_data="create_mailing"),
                    InlineKeyboardButton(text="🔙 Назад", callback_data="admin_panel"))

mailings_markup_with_last = InlineKeyboardMarkup(row_width=1)
mailings_markup_with_last.add(InlineKeyboardButton(text="🆕 Создать рассылку", callback_data="create_mailing"),
                              InlineKeyboardButton(text="📨 Прошлые рассылки", callback_data="lastmailings_0_0"),
                              InlineKeyboardButton(text="🔙 Назад", callback_data="admin_panel"))

users_markup = InlineKeyboardMarkup(row_width=1)
users_markup.add(InlineKeyboardButton(text="📋 Список пользователей", callback_data="userslist"),
                 InlineKeyboardButton(text="📋 Список заблокированных пользователей", callback_data="blockusers_0_0"),
                 InlineKeyboardButton(text="🙅‍♂️ Заблокировать пользователя", callback_data="block_user"),
                 InlineKeyboardButton(text="🤵 Разблокировать пользователя", callback_data="unblock_user"),
                 InlineKeyboardButton(text="🔙 Назад", callback_data="admin_panel"))

users_list_markup = InlineKeyboardMarkup(row_width=3)
users_list_markup.add(InlineKeyboardButton("txt", callback_data="userslist_txt"),
                      InlineKeyboardButton("html", callback_data="userslist_html"),
                      InlineKeyboardButton("json", callback_data="userslist_json"),
                      InlineKeyboardButton("xlsx", callback_data="userslist_xlsx"))
users_list_markup.add(InlineKeyboardButton(text="🔙 Назад", callback_data="users"),
                      InlineKeyboardButton(text="🏠 Админская панель", callback_data="admin_panel"))

confirmation_markup = InlineKeyboardMarkup(row_width=2)
confirmation_markup.add(InlineKeyboardButton("❌ Нет", callback_data="no"),
                        InlineKeyboardButton("✅ Да", callback_data="yes"))
