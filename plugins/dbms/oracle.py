class OraclePlugin:
    name = "Oracle"

    @staticmethod
    def get_version_query():
        return "SELECT banner FROM v$version WHERE rownum=1"

    @staticmethod
    def get_database_names_query():
        return "SELECT owner FROM all_tables"

    @staticmethod
    def get_tables_query(database):
        return f"SELECT table_name FROM all_tables WHERE owner='{database}'"

    @staticmethod
    def get_columns_query(database, table):
        return f"SELECT column_name FROM all_tab_columns WHERE owner='{database}' AND table_name='{table}'"

    @staticmethod
    def get_data_query(database, table, columns):
        return f"SELECT {','.join(columns)} FROM {database}.{table}"

    @staticmethod
    def file_read(filepath):
        # Oracle requires UTL_FILE; simplified
        return f"SELECT UTL_FILE.FOPEN('{filepath}') FROM dual"