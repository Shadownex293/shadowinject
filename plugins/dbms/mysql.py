class MySQLPlugin:
    name = "MySQL"
    
    @staticmethod
    def get_version_query():
        return "SELECT @@version"
        
    @staticmethod
    def get_database_names_query():
        return "SELECT schema_name FROM information_schema.schemata"
        
    @staticmethod
    def get_tables_query(database):
        return f"SELECT table_name FROM information_schema.tables WHERE table_schema='{database}'"
        
    @staticmethod
    def get_columns_query(database, table):
        return f"SELECT column_name FROM information_schema.columns WHERE table_schema='{database}' AND table_name='{table}'"
        
    @staticmethod
    def get_data_query(database, table, columns):
        return f"SELECT {','.join(columns)} FROM {database}.{table}"
        
    @staticmethod
    def file_read(filepath):
        return f"LOAD_FILE('{filepath}')"
        
    @staticmethod
    def file_write(content, remote_path):
        # Need to write using INTO OUTFILE
        return f"SELECT '{content}' INTO OUTFILE '{remote_path}'"