class ConnectionConfig:
    @classmethod
    def get_postgres_connection_config(cls):
        db_name = "railway"
        db_user = "postgres"
        db_password = "f5T28hV4Umu90iVUxyYc"
        db_host = "containers-us-west-132.railway.app"
        db_port = "6150"

        postgres_connection_config = {
            "dbname": db_name,
            "password": db_password,
            "user": db_user,
            "port": db_port,
            "host": db_host
        }

        return postgres_connection_config

    @classmethod
    def get_localhost_connection_config(cls):
        db_name = "postgres"
        db_user = "postgres"
        db_password = "463549"
        db_host = "localhost"
        db_port = "5432"

        postgres_connection_config = {
            "dbname": db_name,
            "password": db_password,
            "user": db_user,
            "port": db_port,
            "host": db_host
        }

        return postgres_connection_config

    @classmethod
    def get_test_db_connection_config(cls):
        db_name = "railway"
        db_user = "postgres"
        db_password = "gd2sFXTHjZb0IOMosa72"
        db_host = "containers-us-west-17.railway.app"
        db_port = "8025"

        postgres_connection_config = {
            "dbname": db_name,
            "password": db_password,
            "user": db_user,
            "port": db_port,
            "host": db_host
        }

        return postgres_connection_config