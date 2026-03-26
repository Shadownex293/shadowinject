class SQLitePlugin:
    name = "SQLite"

    @staticmethod
    def get_version_query():
        return "SELECT sqlite_version()"

    @staticmethod
    def get_database_names_query():
        return "SELECT name FROM sqlite_master WHERE type='database'"

    @staticmethod
    def get_tables_query(database):
        # SQLite doesn't have multiple databases in same connection normally
        return "SELECT name FROM sqlite_master WHERE type='table'"

    @staticmethod
    def get_columns_query(database, table):
        return f"PRAGMA table_info({table})"

    @staticmethod
    def get_data_query(database, table, columns):
        return f"SELECT {','.join(columns)} FROM {table}"