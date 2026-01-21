import sqlite3


class Database:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.db.cursor()

    def register_activity(self, chat_id, func_name, datetime_of_action, date_of_action):
        self.cursor.execute(
            "INSERT INTO user_activities (chat_id, func_name, datetime_of_action, date_of_action) VALUES (?, ?, ?, ?)",
            (chat_id, func_name, datetime_of_action, date_of_action))
        self.db.commit()

    def clear_user_activities(self, datetime):
        self.cursor.execute(
            "DELETE FROM user_activities WHERE datetime_of_action <= ?", (datetime,))
        self.db.commit()

    def get_count_from_user_activities(self, func_names):
        self.cursor.execute(
            f"SELECT id FROM user_activities WHERE func_name IN ({', '.join('?' * len(func_names))}) GROUP BY chat_id",
            func_names)
        result = self.cursor.fetchall()
        return len(result)

    def get_count_from_user_activities_in_date(self, func_names, date):
        self.cursor.execute(
            f"SELECT id FROM user_activities WHERE func_name IN ({', '.join('?' * len(func_names))}) AND date_of_action = ? GROUP BY chat_id",
            (*func_names, date))
        result = self.cursor.fetchall()
        return len(result)

    def add_user(self, chat_id, name, username, register_datetime, register_date):
        self.cursor.execute(
            "INSERT INTO users (chat_id, name, username, register_datetime, register_date) VALUES (?, ?, ?, ?, ?)",
            (chat_id, name, username, register_datetime, register_date))
        self.db.commit()

    def update_names_in_users(self, user_id, username, full_name):
        self.cursor.execute("UPDATE users SET username = ?, name = ? WHERE id = ?", (username, full_name, user_id))
        self.db.commit()

    def update_username_in_users(self, username):
        self.cursor.execute("UPDATE users SET username = ? WHERE username = ?", (None, username))
        self.db.commit()

    def is_user_exists(self, chat_id):
        self.cursor.execute("SELECT ? IN (SELECT chat_id FROM users)", (chat_id,))
        result = self.cursor.fetchone()
        return result[0]

    def is_user_exists_by_username(self, username):
        self.cursor.execute("SELECT ? IN (SELECT username FROM users WHERE username IS NOT NULL)", (username,))
        result = self.cursor.fetchone()
        return result[0]

    def get_count_of_users(self):
        self.cursor.execute("SELECT COUNT(id) AS count_of_users FROM users")
        result = self.cursor.fetchone()[0]
        return result

    def get_count_of_users_without_admins(self, admins):
        self.cursor.execute(
            f"SELECT COUNT(id) AS count_of_users FROM users WHERE chat_id NOT IN ({', '.join('?' * len(admins))})",
            admins)
        result = self.cursor.fetchone()[0]
        return result

    def get_count_of_users_in_date(self, date):
        self.cursor.execute(
            "SELECT COUNT(id) AS count_of_users FROM users WHERE register_date = ?", (date,))
        result = self.cursor.fetchone()[0]
        return result

    def get_count_of_users_before_date(self, date):
        self.cursor.execute(
            "SELECT COUNT(id) AS count_of_users FROM users WHERE register_date <= ?", (date,))
        result = self.cursor.fetchone()[0]
        return result

    def get_count_of_users_who_have_a_profile(self):
        self.cursor.execute(
            "SELECT COUNT(id) AS count_of_users FROM users WHERE height IS NOT NULL AND weight IS NOT NULL AND (age IS NOT NULL or gender IS NOT NULL) AND level_of_activities IS NOT NULL")
        result = self.cursor.fetchone()[0]
        return result

    def get_count_of_users_who_use_fav(self):
        self.cursor.execute(
            "SELECT DISTINCT user_id FROM products_users")
        result1 = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT DISTINCT user_id FROM recipes_users")
        result2 = self.cursor.fetchall()

        return len(list(set(result1 + result2)))

    def get_count_of_users_who_diary(self, date=None):
        if not date:
            self.cursor.execute("SELECT DISTINCT user_id FROM diary")
        else:
            self.cursor.execute("SELECT DISTINCT user_id FROM diary WHERE date_to_add = ?", (date, ))

        result = self.cursor.fetchall()

        return len(result)

    def get_user_id_and_datetime_with_chat_id(self, chat_id):
        self.cursor.execute(
            "SELECT id, register_datetime FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        return result

    def get_username_by_chat_id(self, chat_id):
        self.cursor.execute("SELECT id, username FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        return result

    def get_names_by_id(self, user_id):
        self.cursor.execute("SELECT name, username FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result

    def get_user_info_by_id(self, user_id):
        self.cursor.execute("SELECT id, chat_id, username, name, register_datetime FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result

    def get_user_info_by_username(self, username):
        self.cursor.execute("SELECT id, chat_id, name, register_datetime FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result

    def get_not_is_sent_users(self, mailing_id):
        self.cursor.execute(
            "SELECT users.chat_id, users.last_message FROM users WHERE users.id NOT IN (SELECT mailings_users.user_id FROM mailings_users WHERE mailings_users.mailing_id = ?) AND users.register_datetime < (SELECT mailings.create_datetime FROM mailings WHERE id = ?)",
            (mailing_id, mailing_id))
        result = self.cursor.fetchall()
        return result

    def get_all_chat_ids(self):
        self.cursor.execute("SELECT chat_id FROM users")
        result = self.cursor.fetchall()
        return result

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        return result

    def update_last_message(self, chat_id, datetime):
        self.cursor.execute("UPDATE users SET last_message = ? WHERE chat_id = ?", (datetime, chat_id))
        self.db.commit()

    def add_user_weight_and_height(self, chat_id, height, weight):
        self.cursor.execute(
            "UPDATE users SET height = ?, weight = ? WHERE chat_id = ?", (height, weight, chat_id))
        self.db.commit()

    def add_end_of_user_profile(self, chat_id, age, born_date, gender, level_of_activities):
        self.cursor.execute(
            "UPDATE users SET age = ?, born_date = ?, gender = ?, level_of_activities = ? WHERE chat_id = ?",
            (age, born_date, gender, level_of_activities, chat_id))
        self.db.commit()

    def add_level_of_activities(self, chat_id, level_of_activities):
        self.cursor.execute("UPDATE users SET level_of_activities = ? WHERE chat_id = ?",
                            (level_of_activities, chat_id))
        self.db.commit()

    def add_user_profile(self, chat_id, height, weight, age, born_date, gender, level_of_activities):
        self.cursor.execute(
            "UPDATE users SET height = ?, weight = ?, age = ?, born_date = ?, gender = ?, level_of_activities = ? WHERE chat_id = ?",
            (height, weight, age, born_date, gender, level_of_activities, chat_id))
        self.db.commit()

    def have_user_a_profile(self, chat_id):
        user_profile = self.get_user_profile(chat_id)

        if all([*user_profile[:2], any(user_profile[2:4]), user_profile[4], user_profile[5] is not None]):
            return 2
        elif any([*user_profile[:2], any(user_profile[2:4]), user_profile[4], user_profile[5] is not None]):
            return 1
        return 0

    def get_user_profile(self, chat_id):
        self.cursor.execute(
            "SELECT height, weight, age, born_date, gender, level_of_activities FROM users WHERE chat_id = ?",
            (chat_id,))
        result = self.cursor.fetchone()
        return result

    def update_end_message(self, end_message, chat_id):
        if end_message != self.get_end_message(chat_id):
            self.cursor.execute(
                "UPDATE users SET end_message = ? WHERE chat_id = ?", (end_message, chat_id))
            self.db.commit()

    def get_end_message(self, chat_id):
        self.cursor.execute(
            "SELECT end_message FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_all_categories1(self):
        self.cursor.execute("SELECT * FROM categories_1")
        result = self.cursor.fetchall()
        return result

    def get_categories_1_id(self, categories_2_id):
        self.cursor.execute(
            "SELECT categories_1_id FROM categories_2 WHERE id = ?", (categories_2_id,))
        result = self.cursor.fetchone()[0]
        return result

    def get_categories2(self, categories_1_id):
        self.cursor.execute(
            "SELECT id, name, link FROM categories_2 WHERE categories_1_id = ?", (categories_1_id,))
        result = self.cursor.fetchall()
        return result

    def get_categories_2_id(self, product_id):
        self.cursor.execute(
            "SELECT categories_2_id FROM products WHERE id = ?", (product_id,))
        result = self.cursor.fetchone()[0]
        return result

    def get_products(self, categories_2_id):
        self.cursor.execute(
            "SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE categories_2_id = ?",
            (categories_2_id,))
        result = self.cursor.fetchall()
        return result

    def get_products_by_search(self, q):
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE name LIKE '{q.lower()}' or name LIKE '{q.capitalize()}' or name LIKE '{q}' ORDER BY length(name)")
        result1 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE name LIKE '{q.lower()} %' or name LIKE '{q.capitalize()} %' or name LIKE '{q} %' ORDER BY length(name)")
        result2 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE name LIKE '% {q.lower()}' or name LIKE '% {q.capitalize()}' or name LIKE '% {q}' ORDER BY length(name)")
        result3 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE name LIKE '{q.lower()}%' or name LIKE '{q.capitalize()}%' or name LIKE '{q}%' ORDER BY length(name)")
        result4 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE name LIKE '%{q.lower()}' or name LIKE '%{q.capitalize()}' or name LIKE '%{q}' ORDER BY length(name)")
        result5 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories FROM products WHERE name LIKE '%{q.lower()}%' or name LIKE '%{q.capitalize()}%' or name LIKE '%{q}%' ORDER BY length(name)")
        result6 = self.cursor.fetchall()

        result = self.__delete_same(
            [*result1, *result2, *result3, *result4, *result5, *result6])
        return result

    def get_all_recipes_categories(self):
        self.cursor.execute("SELECT * FROM recipes_categories")
        result = self.cursor.fetchall()
        return result

    def get_recipes(self, category_id):
        self.cursor.execute(
            "SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE recipes_categories_id = ?",
            (category_id,))
        result = self.cursor.fetchall()
        return result

    def get_recipes_by_search(self, q):
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE name LIKE '{q.lower()}' or name LIKE '{q.capitalize()}' or name LIKE '{q}' ORDER BY length(name)")
        result1 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE name LIKE '{q.lower()} %' or name LIKE '{q.capitalize()} %' or name LIKE '{q} %' ORDER BY length(name)")
        result2 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE name LIKE '% {q.lower()}' or name LIKE '% {q.capitalize()}' or name LIKE '% {q}' ORDER BY length(name)")
        result3 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE name LIKE '{q.lower()}%' or name LIKE '{q.capitalize()}%' or name LIKE '{q}%' ORDER BY length(name)")
        result4 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE name LIKE '%{q.lower()}' or name LIKE '%{q.capitalize()}' or name LIKE '%{q}' ORDER BY length(name)")
        result5 = self.cursor.fetchall()
        self.cursor.execute(
            f"SELECT id, name, img, link, proteins, fats, carbohydrates, calories, telegraph_url FROM recipes WHERE name LIKE '%{q.lower()}%' or name LIKE '%{q.capitalize()}%' or name LIKE '%{q}%' ORDER BY length(name)")
        result6 = self.cursor.fetchall()

        result = self.__delete_same(
            [*result1, *result2, *result3, *result4, *result5, *result6])
        return result

    @staticmethod
    def __delete_same(l):
        result_l = []
        for i in l:
            if i not in result_l:
                result_l.append(i)
        return result_l

    def add_mailing(self, message_id, chat_id, all_count, create_datetime, type):
        self.cursor.execute(
            f"INSERT INTO mailings (message_id, chat_id, all_count, success_count, create_datetime, type) VALUES (?, ?, ?, 0, ?, ?)",
            (message_id, chat_id, all_count, create_datetime, type))
        self.db.commit()

    def update_success_count_in_mailing(self, message_id):
        self.cursor.execute(
            "UPDATE mailings SET success_count = success_count + 1 WHERE message_id = ?", (message_id,))
        self.db.commit()

    def update_type_in_mailings(self, mailing_id, type_):
        self.cursor.execute(
            "UPDATE mailings SET type = ? WHERE id = ?", (type_, mailing_id))
        self.db.commit()

    def get_last_mailings(self):
        self.cursor.execute(
            "SELECT id, create_datetime, message_id, chat_id, all_count, success_count, type FROM mailings")
        result = self.cursor.fetchall()
        result.reverse()
        return result

    def get_last_active_mailings(self):
        self.cursor.execute(
            "SELECT id, create_datetime, message_id, chat_id, all_count, success_count, type FROM mailings WHERE all_count != success_count AND type = 1")
        result = self.cursor.fetchall()
        result.reverse()
        return result

    def get_type_of_mailing_by_message_id(self, message_id):
        self.cursor.execute(
            "SELECT type FROM mailings WHERE message_id = ?", (message_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_type_of_mailing_by_mailing_id(self, mailing_id):
        self.cursor.execute(
            "SELECT type FROM mailings WHERE id = ?", (mailing_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_success_count_in_mailing(self, mailing_id):
        self.cursor.execute(
            "SELECT success_count FROM mailings WHERE id = ?", (mailing_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_not_send_mailings(self, user_id, datetime):
        self.cursor.execute(
            "SELECT mailings.id, mailings.message_id, mailings.chat_id FROM mailings WHERE mailings.id NOT IN (SELECT mailings_users.mailing_id FROM mailings_users WHERE mailings_users.user_id = ?) AND mailings.type = 1 AND mailings.create_datetime > ?",
            (user_id, datetime))
        result = self.cursor.fetchall()
        return result

    def add_mailings_users(self, message_id, chat_id):
        self.cursor.execute(
            "INSERT INTO mailings_users (mailing_id, user_id) VALUES ((SELECT id FROM mailings WHERE message_id = ?), (SELECT id FROM users WHERE chat_id = ?))",
            (message_id, chat_id))
        self.db.commit()

    def add_mailings_users_with_mailing_id(self, mailing_id, user_id):
        self.cursor.execute(
            "INSERT INTO mailings_users (mailing_id, user_id) VALUES (?, (SELECT id FROM users WHERE chat_id = ?))",
            (mailing_id, user_id))
        self.db.commit()

    def add_mailings_users_with_mailing_id_and_user_id(self, mailing_id, user_id):
        self.cursor.execute(
            "INSERT INTO mailings_users (mailing_id, user_id) VALUES (?, ?)", (mailing_id, user_id))
        self.db.commit()

    def is_user_had_sent_notion(self, mailing_id, user_id):
        self.cursor.execute(
            "SELECT (SELECT users.id FROM users WHERE users.chat_id = ?) IN (SELECT mailings_users.user_id FROM mailings_users WHERE mailings_users.mailing_id = ?)",
            (user_id, mailing_id))
        result = self.cursor.fetchone()

        return result[0]

    def is_user_had_sent_notion_without_mailing_id(self, message_id, user_id):
        self.cursor.execute(
            "SELECT (SELECT users.id FROM users WHERE users.chat_id = ?) IN (SELECT mailings_users.user_id FROM mailings_users WHERE mailings_users.mailing_id = (SELECT mailings.id FROM mailings WHERE mailings.message_id = ?))",
            (user_id, message_id))
        result = self.cursor.fetchone()

        return result[0]

    def add_end_of_mailing(self, text, chat_id):
        self.cursor.execute(
            "INSERT INTO end_of_mailings (text_of_message, user_id) VALUES (?, (SELECT id FROM users WHERE chat_id = ?))",
            (text, chat_id))
        self.db.commit()

    def del_end_of_mailing(self, end_of_mailing_id):
        self.cursor.execute(
            "DELETE FROM end_of_mailings WHERE id = ?", (end_of_mailing_id,))
        self.db.commit()

    def get_ends_of_mailings(self, chat_id):
        self.cursor.execute(
            "SELECT id, text_of_message FROM end_of_mailings WHERE user_id = (SELECT id FROM users WHERE chat_id = ?)",
            (chat_id,))
        result = self.cursor.fetchall()
        return result

    def add_block(self, user_id=None, username=None, block_datetime=None):
        self.cursor.execute(
            "INSERT INTO block_users (user_id, username, block_datetime) VALUES (?, ?, ?)",
            (user_id, username, block_datetime))
        self.db.commit()

    def update_block(self, block_id, block_datetime):
        self.cursor.execute("UPDATE block_users SET active = 1, block_datetime = ? WHERE id = ?",
                            (block_datetime, block_id))
        self.db.commit()

    def update_block_by_username(self, username, block_datetime):
        self.cursor.execute("UPDATE block_users SET active = 1, block_datetime = ? WHERE username = ?",
                            (block_datetime, username))
        self.db.commit()

    def update_username_in_block(self, user_id, username):
        self.cursor.execute("UPDATE block_users SET username = ? WHERE user_id = ?", (username, user_id))
        self.db.commit()

    def update_username_in_block_set_null(self, username):
        self.cursor.execute("UPDATE block_users SET username = ? WHERE username = ?", (None, username))
        self.db.commit()

    def update_user_id_in_block(self, username, user_id):
        self.cursor.execute("UPDATE block_users SET user_id = ? WHERE username = ?", (user_id, username))
        self.db.commit()

    def del_block_by_username(self, username, block_datetime):
        self.cursor.execute("UPDATE block_users SET active = 0, block_datetime = ? WHERE username = ?",
                            (block_datetime, username))
        self.db.commit()

    def del_block_by_id(self, block_id, block_datetime):
        self.cursor.execute("UPDATE block_users SET active = 0, block_datetime = ? WHERE id = ?",
                            (block_datetime, block_id))
        self.db.commit()

    def delete_from_block(self, username):
        self.cursor.execute("DELETE FROM block_users WHERE username = ?", (username,))
        self.db.commit()

    def del_null_block(self):
        self.cursor.execute("DELETE FROM block_users WHERE user_id IS NULL AND username IS NULL")
        self.db.commit()

    def is_user_block(self, block_id):
        self.cursor.execute("SELECT active FROM block_users WHERE id = ?", (block_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def is_user_in_block(self, username):
        self.cursor.execute(f"SELECT ? IN (SELECT username FROM block_users WHERE username IS NOT NULL)", (username,))
        result = self.cursor.fetchone()
        return result[0]

    def get_block_user_id(self, block_id):
        self.cursor.execute("SELECT user_id FROM block_users WHERE id = ?", (block_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return False

    def get_block_datetime(self, block_id):
        self.cursor.execute("SELECT block_datetime FROM block_users WHERE id = ?", (block_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_block_usernames(self):
        self.cursor.execute("SELECT username FROM block_users WHERE active = 1")
        result = self.cursor.fetchall()
        return result

    def get_block_chat_ids(self):
        self.cursor.execute(
            "SELECT users.chat_id FROM users JOIN block_users ON users.id = block_users.user_id WHERE active = 1")
        result = self.cursor.fetchall()
        return result

    def get_block_users(self):
        self.cursor.execute(
            "SELECT block_users.id, IIF(block_users.username IS NOT NULL, '@' || block_users.username, block_users.username), users.name, users.id, users.chat_id, users.register_datetime FROM users RIGHT JOIN block_users ON users.id = block_users.user_id ORDER BY block_users.block_datetime DESC")
        result = self.cursor.fetchall()
        return result

    def add_favorite_product(self, chat_id, product_id, dt):
        self.cursor.execute("INSERT INTO products_users VALUES (?, (SELECT id FROM users WHERE chat_id = ?), ?)",
                            (product_id, chat_id, dt))
        self.db.commit()

    def add_favorite_recipe(self, chat_id, recipe_id, dt):
        self.cursor.execute("INSERT INTO recipes_users VALUES (?, (SELECT id FROM users WHERE chat_id = ?), ?)",
                            (recipe_id, chat_id, dt))
        self.db.commit()

    def del_favorite_product(self, chat_id, product_id):
        self.cursor.execute(
            "DELETE FROM products_users WHERE product_id = ? AND user_id = (SELECT id FROM users WHERE chat_id = ?)",
            (product_id, chat_id))
        self.db.commit()

    def del_favorite_recipe(self, chat_id, recipe_id):
        self.cursor.execute(
            "DELETE FROM recipes_users WHERE recipe_id = ? AND user_id = (SELECT id FROM users WHERE chat_id = ?)",
            (recipe_id, chat_id))
        self.db.commit()

    def is_product_favorite(self, chat_id, product_id):
        self.cursor.execute(
            "SELECT * FROM products_users WHERE product_id = ? AND user_id = (SELECT id FROM users WHERE chat_id = ?)",
            (product_id, chat_id))
        result = self.cursor.fetchone()
        return bool(result)

    def is_recipe_favorite(self, chat_id, recipe_id):
        self.cursor.execute(
            "SELECT * FROM recipes_users WHERE recipe_id = ? AND user_id = (SELECT id FROM users WHERE chat_id = ?)",
            (recipe_id, chat_id))
        result = self.cursor.fetchone()
        return bool(result)

    def get_favorites_products(self, chat_id):
        self.cursor.execute(
            "SELECT products.id, products.name, products.img, products.link, products.proteins, products.fats, products.carbohydrates, products.calories FROM products JOIN products_users ON products_users.product_id = products.id WHERE products_users.user_id = (SELECT users.id FROM users WHERE users.chat_id = ?) ORDER BY products_users.datetime_to_add DESC",
            (chat_id,))
        result = self.cursor.fetchall()
        return result

    def get_favorites_recipes(self, chat_id):
        self.cursor.execute(
            "SELECT recipes.id, recipes.name, recipes.img, recipes.link, recipes.proteins, recipes.fats, recipes.carbohydrates, recipes.calories, recipes.telegraph_url FROM recipes JOIN recipes_users ON recipes_users.recipe_id = recipes.id WHERE recipes_users.user_id = (SELECT users.id FROM users WHERE users.chat_id = ?) ORDER BY recipes_users.datetime_to_add DESC",
            (chat_id,))
        result = self.cursor.fetchall()
        return result

    def add_to_diary(self, product_id, recipe_id, chat_id, volume, group, date_to_add):
        self.cursor.execute(
            "INSERT INTO diary (product_id, recipe_id, user_id, volume, \"group\", date_to_add) VALUES (?, ?, (SELECT id FROM users WHERE chat_id = ?), ?, ?, ?)",
            (product_id, recipe_id, chat_id, volume, group, date_to_add))
        self.db.commit()

    def edit_diary(self, diary_id, volume, group, date_to_add):
        if not all(map(lambda x: x == "not_edit", [volume, group, date_to_add])):
            query = []
            params = []

            if volume != "not_edit":
                query.append("volume = ?")
                params.append(volume)

            if group != "not_edit":
                query.append("\"group\" = ?")
                params.append(group)

            if date_to_add != "not_edit":
                query.append("date_to_add = ?")
                params.append(date_to_add)

            self.cursor.execute("UPDATE diary SET " + ", ".join(query) +  "WHERE id = ?", params + [diary_id])
            self.db.commit()

    def del_from_diary(self, diary_id):
        self.cursor.execute("DELETE FROM diary WHERE id = ?", (diary_id,))
        self.db.commit()

    def get_diary(self, chat_id, date_to_add):
        self.cursor.execute(
            "SELECT diary.volume, diary.\"group\", IIF(products.name IS NULL, recipes.name, products.name) AS name, IIF(products.proteins IS NULL, recipes.proteins, products.proteins) AS proteins, IIF(products.fats IS NULL, recipes.fats, products.fats) AS fats, IIF(products.carbohydrates IS NULL, recipes.carbohydrates, products.carbohydrates) AS carbohydrates, IIF(products.calories IS NULL, recipes.calories, products.calories) AS calories FROM diary LEFT JOIN products ON diary.product_id = products.id LEFT JOIN recipes ON diary.recipe_id = recipes.id WHERE diary.user_id = (SELECT id FROM users WHERE chat_id = ?) AND date_to_add = ?",
            (chat_id, date_to_add))
        result = self.cursor.fetchall()
        return result

    def get_diary_with_group(self, chat_id, date_to_add, group):
        self.cursor.execute(
            "SELECT diary.id, diary.volume, IIF(products.name IS NULL, recipes.name, products.name) AS name, IIF(products.proteins IS NULL, recipes.proteins, products.proteins) AS proteins, IIF(products.fats IS NULL, recipes.fats, products.fats) AS fats, IIF(products.carbohydrates IS NULL, recipes.carbohydrates, products.carbohydrates) AS carbohydrates, IIF(products.calories IS NULL, recipes.calories, products.calories) AS calories FROM diary LEFT JOIN products ON diary.product_id = products.id LEFT JOIN recipes ON diary.recipe_id = recipes.id WHERE diary.user_id = (SELECT id FROM users WHERE chat_id = ?) AND date_to_add = ? AND  diary.\"group\" = ?",
            (chat_id, date_to_add, group))
        result = self.cursor.fetchall()
        return result

    def get_diary_by_id(self, diary_id):
        self.cursor.execute(
            "SELECT diary.volume, diary.\"group\", IIF(products.name IS NULL, recipes.name, products.name) AS name, IIF(products.proteins IS NULL, recipes.proteins, products.proteins) AS proteins, IIF(products.fats IS NULL, recipes.fats, products.fats) AS fats, IIF(products.carbohydrates IS NULL, recipes.carbohydrates, products.carbohydrates) AS carbohydrates, IIF(products.calories IS NULL, recipes.calories, products.calories) AS calories, diary.date_to_add FROM diary LEFT JOIN products ON diary.product_id = products.id LEFT JOIN recipes ON diary.recipe_id = recipes.id WHERE diary.id = ?",
            (diary_id, ))
        result = self.cursor.fetchone()
        return result
