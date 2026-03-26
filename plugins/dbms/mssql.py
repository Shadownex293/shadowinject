class MSSQLPlugin:
    name = "MSSQL"

    @staticmethod
    def get_version_query():
        return "SELECT @@version"

    @staticmethod
    def get_database_names_query():
        return "SELECT name FROM master..sysdatabases"

    @staticmethod
    def get_tables_query(database):
        return f"SELECT table_name FROM {database}.information_schema.tables"

    @staticmethod
    def get_columns_query(database, table):
        return f"SELECT column_name FROM {database}.information_schema.columns WHERE table_name='{table}'"

    @staticmethod
    def get_data_query(database, table, columns):
        return f"SELECT {','.join(columns)} FROM {database}.{table}"

    @staticmethod
    def file_read(filepath):
        return f"SELECT * FROM OPENROWSET(BULK '{filepath}', SINGLE_BLOB) AS f"

    @staticmethod
    def file_write(content, remote_path):
        # Using xp_cmdshell or OLE automation; simplified
        return f"exec xp_cmdshell 'echo {content} > {remote_path}'"