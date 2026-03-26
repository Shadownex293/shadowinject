class GenericPlugin:
    name = "Generic"
    
    @staticmethod
    def get_version_query():
        return "SELECT version()"
        
    @staticmethod
    def get_database_names_query():
        return "SELECT name FROM master..sysdatabases"  # MSSQL fallback