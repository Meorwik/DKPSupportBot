from pandas import DataFrame
from psycopg2 import connect

DB_USERS_COLUMNS = ["id", "user_id", "username", "first_name", "last_name"]


class DataConvertor:
    async def convert_to_exel(self, values, columns, file_name):
        file_path = f"data/info_files/{file_name}.xlsx"
        try:
            data_frame = DataFrame(values, columns=columns)
            data_frame.to_excel(file_path)
            return file_path
        except PermissionError:
            return file_path


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
        self._cursor = self._connection.cursor()
        return self._connection

    async def close_connection(self):
        self._connection.close()


class PostgresDataBaseManager(DataBaseManager):

    async def add_user(self, user):
        await self.set_connection()
        sql_add_user = \
            f"""
                INSERT INTO users(user_id, username, first_name, last_name) 
                VALUES('{user.id}', '{user.username}', '{user.first_name}', '{user.last_name}')
            """
        self._cursor.execute(sql_add_user)
        self._connection.commit()
        await self.close_connection()
        return True

    async def get_user(self, user):
        await self.set_connection()
        sql_get_user = f"SELECT * FROM users WHERE user_id = '{user.id}'"
        self._cursor.execute(sql_get_user)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    async def get_all_users(self):
        await self.set_connection()
        sql_get_user = f"SELECT * FROM users"
        self._cursor.execute(sql_get_user)
        result = self._cursor.fetchall()
        await self.close_connection()
        return result

    async def check_user(self, user):
        user_data = await self.get_user(user)
        if not user_data:
            await self.add_user(user=user)

        return True

    async def create_table_copy(self, original_table, new_table_name):
        await self.set_connection()
        copy_table_sql = f"CREATE TABLE {new_table_name} AS TABLE {original_table}"
        self._cursor.execute(copy_table_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def create_users_table(self):
        await self.set_connection()
        create_users_table_sql = """
            CREATE TABLE users (
            "id" serial PRIMARY KEY,
            "user_id" VARCHAR (50) UNIQUE NOT NULL,
            "username" VARCHAR (50),
            "first_name" VARCHAR (50),
            "last_name" VARCHAR (50));
        """

        self._cursor.execute(create_users_table_sql)
        self._connection.commit()
        await self.close_connection()
        return True

    async def transfer_data(self, table_from, table_to):
        await self.set_connection()
        transfer_data_sql = f"INSERT INTO {table_to} (SELECT * FROM {table_from})"
        self._cursor.execute(transfer_data_sql)
        self._connection.commit()
        await self.close_connection()
        return True
