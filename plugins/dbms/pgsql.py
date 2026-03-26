class PostgreSQLPlugin:
    name = "PostgreSQL"
    
    @staticmethod
    def get_version_query():
        return "SELECT version()"
        
    @staticmethod
    def get_database_names_query():
        return "SELECT datname FROM pg_database"
        
    @staticmethod
    def get_tables_query(database):
        return f"SELECT tablename FROM pg_tables WHERE schemaname='public'"
        
    @staticmethod
    def get_columns_query(database, table):
        return f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}'"
        
    @staticmethod
    def get_data_query(database, table, columns):
        return f"SELECT {','.join(columns)} FROM {table}"