from psycopg2.extras import RealDictCursor
from pandas import DataFrame
from psycopg2 import connect
from datetime import datetime

DB_USERS_COLUMNS = ["id", "user_id", "username", "first_name", "last_name", "uik", "role"]
DB_TESTS_COLUMNS = ["id", "user_id", "test_name", "language", "is_finished", "result", "datetime"]
DB_LOGS_COLUMNS = ["id", "user_id", "action", "datetime"]

# КЛАСС: DataConvertor
# Создан для конвертации и загрузки данных в файлы
class DataConvertor:
    async def convert_to_exel(self, values, columns, file_name):
        file_path = f"data/database_backup/{file_name}.xlsx"
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
        self._connection = connect\
            (
                f"""
                    dbname={self.config['dbname']}
                    user={self.config['user']}
                    password={self.config['password']}
                    host={self.config['host']}
                    port={self.config['port']}
                """
            )
        self._cursor = self._connection.cursor(cursor_factory=RealDictCursor)
        return self._connection

    async def close_connection(self):
        self._connection.close()

# КЛАСС: PostgresDataBaseManager
# Создан для работы с Postgres
class PostgresDataBaseManager(DataBaseManager):
    #--------------CREATE TABLES--------------
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
            "role" VARCHAR(50) NOT NULL DEFAULT "user"
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

    #------------ACTIONS WITH USERS-------------

    async def add_user(self, user, uik):
        await self.set_connection()
        sql_add_user = \
            f"""
                INSERT INTO users(user_id, username, first_name, last_name, uik) 
                VALUES('{user.id}', '{user.username}', '{user.first_name}', '{user.last_name}', '{uik}')
            """
        self._cursor.execute(sql_add_user)
        self._connection.commit()
        await self.close_connection()
        await self.download_users_table()
        return True

    async def get_user(self, user):
        await self.set_connection()
        sql_get_user = f"SELECT * FROM users WHERE user_id = '{user.id}'"
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
        user_data = await self.get_user(user)
        return not user_data

    async def get_user_uik(self, user):
        user_data = await self.get_user(user)
        return user_data["uik"]

    async def change_user_role(self, user, new_role):
        user_data = await self.get_user(user)
        user_id = user_data["id"]
        await self.set_connection()
        change_user_role_sql = f"""
        UPDATE users SET role = '{new_role}' WHERE id = {user_id}
        """
        self._cursor.execute(change_user_role_sql)
        self._connection.commit()
        await self.close_connection()
        return True
    #------------ACTIONS WITH LOGS----------------

    async def database_log(self, user, action):
        await self.set_connection()
        datetime_data = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        database_log_sql = f"""
            INSERT INTO logs (user_id, action, datetime) VALUES ({user}, '{action}', '{datetime_data}')
        """
        self._cursor.execute(database_log_sql)
        self._connection.commit()
        await self.close_connection()
        await self.download_logs_table()
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

    #------------ACTIONS WITH TESTS---------------

    async def add_new_test_results(self, test_result):
        await self.set_connection()
        add_new_test_result_sql = f"""
            INSERT INTO tests (
                user_id, 
                test_name, 
                language, 
                is_finished, 
                result, 
                datetime) 
                
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
        await self.download_tests_table()
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

    #---------------DOWNLOAD TABLES----------------

    async def download_logs_table(self):
        file_name = "logs"
        logs = await self.get_all_logs()
        return await DataConvertor().convert_to_exel(values=logs, columns=DB_LOGS_COLUMNS, file_name=file_name)

    async def download_tests_table(self):
        file_name = "tests"
        tests = await self.get_all_tests_results()
        return await DataConvertor().convert_to_exel(values=tests, columns=DB_TESTS_COLUMNS, file_name=file_name)

    async def download_users_table(self):
        file_name = "users"
        users = await self.get_all_users()
        print(users)
        return await DataConvertor().convert_to_exel(users, DB_USERS_COLUMNS, file_name)
