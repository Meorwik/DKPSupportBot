class ConnectionConfig:
    def get_postgres_connection_config(self):
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


