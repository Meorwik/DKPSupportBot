class ConnectionConfig:
    @classmethod
    def get_postgres_connection_config(cls):
        # db_name = "railway"
        # db_user = "postgres"
        # db_password = "WmG1sJGgxmdWQpkNhgxD"
        # db_host = "containers-us-west-10.railway.app"
        # db_port = "5735"
        #
        # postgres_connection_config = {
        #     "dbname": db_name,
        #     "password": db_password,
        #     "user": db_user,
        #     "port": db_port,
        #     "host": db_host
        # }
        #
        # return postgres_connection_config

        return cls.get_test_db_connection_config()

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
        db_password = "8yNOalMo1l7JKdAGAV5m"
        db_host = "containers-us-west-72.railway.app"
        db_port = "8017"

        postgres_connection_config = {
            "dbname": db_name,
            "password": db_password,
            "user": db_user,
            "port": db_port,
            "host": db_host
        }

        return postgres_connection_config