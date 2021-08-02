import sqlite3, py.util, os

class trafficRecoDB:

    def __init__(self, dbpath, conf_path=""):
        self.conn = sqlite3.connect(dbpath)
        self.cursor = self.conn.cursor()
        self.conf_path = conf_path
        if len(conf_path) > 0:
            self.req = py.util.loadReq(conf_path)
        self.setupTables()

    # Close the connection to the database
    def __del__(self):
        self.conn.close()
    
    # Set up the tables
    def setupTables(self):
        lang_gen_voices = """
            CREATE TABLE IF NOT EXISTS lang_gen_voices (
                lang_name TEXT PRIMARY KEY NOT NULL 
            );
        """
        classes = """
            CREATE TABLE IF NOT EXISTS classes (
                class_name TEXT PRIMARY KEY NOT NULL
            );
        """
        gender = """
            CREATE TABLE IF NOT EXISTS genders (
                gender_name TEXT PRIMARY KEY NOT NULL
            );
        """
        voice_files = """
            CREATE TABLE IF NOT EXISTS voice_files (
                voice_file_name TEXT PRIMARY KEY NOT NULL,
                file_path TEXT NOT NULL,
                file_num INT NOT NULL,
                lang_name TEXT NOT NULL,
                gender_name TEXT NOT NULL,
                class_name TEXT NOT NULL,
                FOREIGN KEY (lang_name) REFERENCES lang_gen_voices (lang_name),
                FOREIGN KEY (gender_name) REFERENCES gender(gender_name),
                FOREIGN KEY (class_name) REFERENCES classes(class_name)
            );
        """
        queries = [lang_gen_voices, classes, gender, voice_files]
        for query in queries:
            self.execQuery(query)

    # Insert row in a table, ignore if it exists
    def insert(self, table, **kwargs):
        self.execQuery(f"""
            INSERT OR IGNORE INTO {table} ({", ".join(list(kwargs.keys()))})
            VALUES ({", ".join(["'"+val+"'" if isinstance(val, str) else str(val) for val in list(kwargs.values())])});
        """)

    # Check the file paths if some does not exist in the directory
    def checkIntegrity(self, table, *args):
        self.execQuery(f"SELECT ({','.join(args)}) FROM {table};")
        file_paths = self.cursor.fetchall()
        for file_path in file_paths:
            if not os.path.exists(file_path[0]):
                self.removeItem(table, file_path=file_path[0])

    # Delete row in a table
    def removeItem(self, table, **kwargs):
        where = ",".join([key + "=" + ("\""+kwargs[key]+"\"" if isinstance(kwargs[key], str) else kwargs[key])  for key in kwargs])
        query = f"DELETE FROM {table} WHERE ({where});"
        self.execQuery(query)

    # Get all values from table
    def getAll(self, table):
        self.execQuery(f" SELECT * FROM {table};")
        return self.cursor.fetchall()

    # Delete all from table
    def clear(self, table):
        self.execQuery(f"DELETE FROM {table};")

    # Execute a query
    def execQuery(self, query):
        self.cursor.execute(query)
        self.conn.commit()