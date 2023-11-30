from psycopg2.extras import RealDictCursor
from datetime import datetime, date
from pandas import DataFrame
from psycopg2 import connect


DB_USERS_COLUMNS = [
    "id",
    "user_id",
    "username",
    "first_name",
    "last_name",
    "uik",
    "role",
    "register_date",
    "consultant_rating"
]

DB_TESTS_COLUMNS = [
    "id",
    "user_id",
    "test_name",
    "language",
    "is_finished",
    "result",
    "datetime"
]

DB_LOGS_COLUMNS = [
    "id",
    "user_id",
    "action",
    "datetime"
]


# КЛАСС: DataConvertor
# Создан для конвертации и загрузки данных в файлы
class DataConvertor:
    async def convert_to_exel(self, values, columns, file_name):
        file_path = f"data/{file_name}.xlsx"
        try:
            data_frame = DataFrame(values, columns=columns)
            data_frame.to_excel(file_path)
            return file_path
        except PermissionError:
            print("PermissionError")
            return file_path


# КЛАСС: DataBaseManager
# Класс родитель, создан для наследования и дальнейшего описания общих функций в одном классе предке.
class DataBaseManager:
    def __init__(self, config):
        self.config = config
        self._connection = None
        self._cursor = None

    async def set_connection(self):
        self._connection = connect(self.config)
        self._cursor = self._connection.cursor(cursor_factory=RealDictCursor)
        return self._connection

    async def close_connection(self):
        self._connection.close()


# КЛАСС: PostgresDataBaseManager
# Создан для работы с Postgres
class PostgresDataBaseManager(DataBaseManager):
    # --------------CREATE TABLES--------------
    async def create_users_table(self):
        await self.set_connection()
        create_users_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
            "id" serial PRIMARY KEY,
            "user_id" VARCHAR (50) UNIQUE NOT NULL,
            "username" VARCHAR (50),
            "first_name" VARCHAR (50),
            "last_name" VARCHAR (50),
            "uik" VARCHAR(50),
            "role" VARCHAR(50) NOT NULL DEFAULT "user",
            "register_date" VARCHAR(50) NOT NULL,
            "consultant_rating" SMALLINT
            );
        """

        self._cursor.execute(create_users_table_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def create_tests_table(self):
        await self.set_connection()
        create_tests_table_sql = """
            CREATE TABLE IF NOT EXISTS tests (
            "id" serial PRIMARY KEY, 
            "user_id" INT NOT NULL,
            "test_name" VARCHAR(50) NOT NULL,
            "language" VARCHAR(50) NOT NULL,
            "is_finished" VARCHAR(50) NOT NULL,
            "result" VARCHAR(50),
            "datetime" VARCHAR(50) NOT NULL,

            CONSTRAINT FK_tests_users FOREIGN KEY(user_id)
            REFERENCES users(id)
            );
        """

        self._cursor.execute(create_tests_table_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def create_logs_table(self):
        await self.set_connection()
        create_logs_table_sql = """
            CREATE TABLE IF NOT EXISTS logs (
            "id" serial PRIMARY KEY,
            "user_id" INT NOT NULL, 
            "action" VARCHAR(50) NOT NULL,
            "datetime" VARCHAR(50) NOT NULL,

            CONSTRAINT FK_logs_users FOREIGN KEY(user_id)
            REFERENCES users(id)
            );
        """

        self._cursor.execute(create_logs_table_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def create_medication_schedule_table(self):
        await self.set_connection()
        create_medication_schedule_table_sql = """
        CREATE TABLE IF NOT EXISTS medication_schedule (
        "id" serial PRIMARY KEY,
        "user_id" INT NOT NULL,
        "drug_name" VARCHAR(150) NOT NULL,
        "dose" VARCHAR(50) NOT NULL,
        "time" VARCHAR(50) NOT NULL,
        
        CONSTRAINT FK_medication_schedule_users FOREIGN KEY(user_id)
        REFERENCES users(id)
        );
        """

        self._cursor.execute(create_medication_schedule_table_sql)
        self._connection.commit()
        await self.close_connection()

    # ------------ACTIONS WITH USERS-------------

    async def add_user(self, user, uik):
        await self.set_connection()
        register_date = str(date.today())
        sql_add_user = \
            f"""
                INSERT INTO users(user_id, username, first_name, last_name, uik, role, register_date) 
                VALUES(
                '{user.id}', 
                '{user.username}', 
                '{user.first_name}', 
                '{user.last_name}', 
                '{uik}', 
                'user', 
                '{register_date}')
            """
        self._cursor.execute(sql_add_user)
        self._connection.commit()
        await self.close_connection()
        return True

    async def update_user_uik(self, user, uik):
        await self.set_connection()

        add_uik_to_user_sql = f"""
        UPDATE users SET uik = '{uik}' WHERE user_id = '{user.id}'
        """

        self._cursor.execute(add_uik_to_user_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def is_consultant_rated(self, user):
        await self.set_connection()

        is_consultant_rated_sql = f"""
        SELECT consultant_rating FROM users WHERE user_id = '{user.id}'
        """

        self._cursor.execute(is_consultant_rated_sql)
        result = self._cursor.fetchone()
        await self.close_connection()
        return bool(result["consultant_rating"])

    async def rate_consultant(self, user, rate: int):
        await self.set_connection()

        rate_consultant_sql = f"""
        UPDATE users SET consultant_rating = {rate} WHERE user_id = '{user.id}'
        """

        self._cursor.execute(rate_consultant_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def get_user(self, user_id):
        await self.set_connection()
        sql_get_user = f"SELECT * FROM users WHERE user_id = '{user_id}'"
        self._cursor.execute(sql_get_user)
        result = self._cursor.fetchone()
        await self.close_connection()
        return result

    async def get_all_users(self):
        await self.set_connection()
        sql_get_user = f"SELECT * FROM users"
        self._cursor.execute(sql_get_user)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    async def is_new_user(self, user):
        user_data = await self.get_user(user.id)
        return not user_data

    async def get_user_uik(self, user):
        user_data = await self.get_user(user.id)
        return user_data["uik"]

    async def change_user_role(self, user, new_role):
        user_data = await self.get_user(user.id)
        user_id = user_data["id"]
        await self.set_connection()
        change_user_role_sql = f"""
        UPDATE users SET role = '{new_role}' WHERE id = {user_id}
        """

        self._cursor.execute(change_user_role_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def get_current_consultant(self):
        await self.set_connection()

        get_current_consultant_sql = """
        SELECT * FROM users WHERE role = 'consultant'
        """

        self._cursor.execute(get_current_consultant_sql)
        result = self._cursor.fetchone()
        await self.close_connection()
        return result

    # ------------ACTIONS WITH LOGS----------------

    async def add_log(self, user, action):
        await self.set_connection()

        datetime_data = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        database_log_sql = f"""
        INSERT INTO logs (user_id, action, datetime) VALUES ({user}, '{action}', '{datetime_data}')
        """

        self._cursor.execute(database_log_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def get_all_logs(self):
        await self.set_connection()

        get_all_logs_results_sql = """
        SELECT * FROM logs
        """

        self._cursor.execute(get_all_logs_results_sql)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    # ------------ACTIONS WITH TESTS---------------

    async def add_test_results(self, test_result):
        await self.set_connection()

        add_new_test_result_sql = f"""
        INSERT INTO tests (
            user_id, test_name, 
            language, is_finished, 
            result, datetime) 
            
            VALUES(
                 {test_result["user_id"]}, 
                '{test_result["test_name"]}', 
                '{test_result["language"]}', 
                '{test_result["is_finished"]}', 
                '{test_result["result"]}', 
                '{test_result["datetime"]}')
        """

        self._cursor.execute(add_new_test_result_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def get_all_tests_results(self):
        await self.set_connection()

        get_all_tests_results_sql = """
        SELECT * FROM tests
        """

        self._cursor.execute(get_all_tests_results_sql)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    # ---------------DOWNLOAD TABLES----------------

    async def download_users_table(self):
        file_name = "users"
        users = await self.get_all_users()
        return await DataConvertor().convert_to_exel(users, DB_USERS_COLUMNS, file_name)

# ----------------------------------------------ANALYTICS TOOLS-------------------------------------
    async def get_all_users_count(self):
        users = await self.get_all_users()
        return len(users)

    async def get_average_consultant_rating(self):
        await self.set_connection()
        get_consultant_ratings_sql = f"""
        SELECT consultant_rating FROM users WHERE consultant_rating IS NOT NULL
        """
        self._cursor.execute(get_consultant_ratings_sql)
        result = self._cursor.fetchall()

        overall_rating = 0
        for rating in range(len(result)):
            overall_rating += result[rating]["consultant_rating"]

        try:
            overall_rating = overall_rating / len(result)

        except ZeroDivisionError:
            return 0

        return overall_rating

    async def get_users_count_in_month(self, period):
        await self.set_connection()

        get_users_count_in_month_sql = f"""
        SELECT * FROM users WHERE register_date LIKE '%{period}%'
        """

        self._cursor.execute(get_users_count_in_month_sql)
        result = self._cursor.fetchall()
        await self.close_connection()
        return len(result)

    async def get_count_contacted_consultant(self, period):
        await self.set_connection()
        get_count_contacted_consultant_sql = f"""
        SELECT COUNT(user_id) FROM logs WHERE action LIKE '%Начал взаимодействие с консультантом!%' AND datetime LIKE '%{period}%'
        """
        self._cursor.execute(get_count_contacted_consultant_sql)
        result = self._cursor.fetchone()
        await self.close_connection()
        return result["count"]

    async def get_assessment_finished_statistic(self, assessment_name, period=None):
        await self.set_connection()
        if period is not None:
            separator = "-"
            period = period.split(separator)
            period = f"{period[1]}/{period[0]}"

            sql = f"""
            SELECT COUNT(is_finished) 
            FROM tests 
            WHERE is_finished = 'True' 
            AND datetime LIKE '%{period}%' 
            AND test_name = '{assessment_name}'
            """

        else:
            sql = f"""
            SELECT COUNT(is_finished) FROM tests WHERE is_finished = 'True' AND test_name = '{assessment_name}'
            """

        self._cursor.execute(sql)
        result = self._cursor.fetchone()
        await self.close_connection()
        return result["count"]

    async def get_assessment_started_statistic(self, assessment_name, period=None):
        await self.set_connection()
        if period is not None:
            separator = "-"
            period = period.split(separator)
            period = f"{period[1]}/{period[0]}"

            sql = f"""
            SELECT COUNT(action) 
            FROM logs 
            WHERE action LIKE '%Начал тест: {assessment_name}%' 
            AND datetime LIKE '%{period}%' 
            """

        else:
            sql = f"""
            SELECT COUNT(action) 
            FROM logs 
            WHERE action LIKE '%Начал тест: {assessment_name}%' 
            """

        self._cursor.execute(sql)
        result = self._cursor.fetchone()
        await self.close_connection()
        return result["count"]

# -------------------------------------- ACTIONS WITH MEDICATION SCHEDULE ------------------------
    async def add_medication_schedule_reminder(self, user, drug_name, time, dose):
        await self.set_connection()
        add_registration_sql = f"""
        INSERT INTO medication_schedule (user_id, drug_name, dose, time) 
        VALUES ({user}, '{drug_name}', '{dose}', '{time}')
        """
        self._cursor.execute(add_registration_sql)
        self._connection.commit()
        await self.close_connection()

    async def get_users_medication_schedule_reminders(self, user):
        await self.set_connection()
        get_users_registrations_sql = f"""
        SELECT * FROM medication_schedule WHERE user_id = {user} 
        """
        self._cursor.execute(get_users_registrations_sql)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    async def delete_medication_schedule_reminder(self, reminder_id, user_id):
        await self.set_connection()
        delete_medication_schedule_reminder_sql = f"""
        DELETE FROM medication_schedule WHERE id = {reminder_id} AND user_id = {user_id}
        """
        self._cursor.execute(delete_medication_schedule_reminder_sql)
        self._connection.commit()
        await self.close_connection()

    async def modify_medication_schedule_reminder(self, reminder_id, user_id, drug_name, dose, time):
        await self.set_connection()
        modify_medication_schedule_reminder_sql = f"""
        UPDATE medication_schedule SET drug_name = '{drug_name}', dose = '{dose}', time = '{time}' WHERE id = {reminder_id} AND user_id = {user_id}
        """
        self._cursor.execute(modify_medication_schedule_reminder_sql)
        self._connection.commit()
        await self.close_connection()

    async def get_taking_meds_history(self, user_id):
        await self.set_connection()
        get_taking_meds_history_sql = f"""
        SELECT * FROM logs WHERE user_id = {user_id} AND action LIKE '%препарат принят%'
        """
        self._cursor.execute(get_taking_meds_history_sql)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    async def get_last_inserted_id(self, table_name):
        await self.set_connection()
        get_last_inserted_id_sql = f"""
        SELECT MAX(id) FROM {table_name}     
        """
        self._cursor.execute(get_last_inserted_id_sql)
        result = self._cursor.fetchone()
        await self.close_connection()
        return int(result["max"])
