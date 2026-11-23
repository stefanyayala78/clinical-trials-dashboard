import sqlite3
import hashlib
#I don´t have to create a function in app since this are the programming logics not a windowN

class DatabaseManager: #Template for the Data Base
    def __init__(self, db_name="clinical_trails.db"):
        self.db_name=db_name
        self.create_users_table() #Needs to be there since the beginning


    def create_table(self, table_name, columns):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        columns_sql = []

        for column_name, data_type in columns:
            columns_sql.append(
                f"{column_name} {data_type}"
            )

        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            {', '.join(columns_sql)}
        )
        """

        cursor.execute(query)


        conn.commit()
        conn.close()


    def create_users_table(self):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def register_user(self, username, password):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        #password.encode() turns text into bytes
        #hashlib.sha256() creates a unique digital fingerpriint
        #encripted password

        try:
            cursor.execute("""
            INSERT INTO users(username, password)
            VALUES (?, ?) 
            """, (username, password_hash))

            #Values (?,?) for position

            conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False
        #It is an exception that SQLite raises when you violate a database constraint.
        #Example sample user name

        finally:
            conn.close()

    def login_user(self, username, password): #To verify if there is a user wiith that username
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest() #Transforms the password entered

        cursor.execute("""
            SELECT id,username
            FROM users
            WHERE username = ? AND password=? 
            """, (username, password_hash))

        user=cursor.fetchone() #Fetchone: first result found
        conn.close()

        return user


    def get_columns(self, table_name):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        conn.close()

        return columns

    def insert_row(self,table_name,values):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        placeholders= ",".join(
            ["?"]*len(values)
        )

        #Instruction in SQLITE
        query= f""" 
        INSERT INTO {table_name}
        VALUES(
            NULL,{placeholders})""" #Null because of the ID in autoincrement

        cursor.execute(
            query,
            values
        )

        row_id=cursor.lastrowid

        conn.commit()
        conn.close()

        return row_id

    def delete_row(self,table_name,row_id): #row_id helps SQLite to know which row to delete
        conn = sqlite3.connect( f"database/{self.db_name}")

        cursor = conn.cursor()

        query = f"""
            DELETE FROM {table_name}
            WHERE id = ?
            """

        cursor.execute(
            query,
            (row_id,)
        )

        conn.commit()
        conn.close()

    def edit_row(self,table_name,row_id,columns,values):
        conn = sqlite3.connect( f"database/{self.db_name}")
        cursor = conn.cursor()

        set_clause = ", ".join(
            [f"{col} = ?" for col in columns]
        )

        query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE id = ?
            """

        cursor.execute(
            query,
            (*values, row_id)
        )

        conn.commit()
        conn.close()

    def get_all_studies(self):
        self.conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            AND name != 'users'
        """)

        return cursor.fetchall()

    def study_number(self):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            AND name != 'users'
        """)
        ## SQLite master is a table created by SQLite that stores the database structure information.
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def active_studies(self):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                AND name != 'users'
            """)

        tables = cursor.fetchall() #Gets all the tables

        studies_with_data = 0

        for table in tables:
            table_name = table[0] #Extracts from the Tuple the name of the study ("study1,")
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}") #How many rows
            rows= cursor.fetchone()[0] #Extrcts rows tuple from (3,)

            if rows >0:
                studies_with_data += 1

        conn.close()
        return studies_with_data

    def average_subjects(self):
        conn = sqlite3.connect(f"database/{self.db_name}")
        cursor = conn.cursor()

        cursor.execute("""SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        AND name != 'users'
        """)

        tables = cursor.fetchall()

        total_subjects=0
        total_studies=len(tables)

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}") #Count rows
            rows = cursor.fetchone()[0] #Subjects

            total_subjects += rows

        conn.close()

        if total_studies == 0:
            return 0

        return round(total_subjects/total_studies, 2) #Round for two decimals


