import pyodbc as odbc


class Database:
    def __init__(self, log, driver, server, database, user='', pwd=''):
        self.log = log
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.pwd = pwd

        if self.user == '' and self.pwd == '':
            conn_data = (
                            "Driver={" + self.driver + "};"
                            f"Server={self.server};"
                            f"Database={self.database};"
                            "Trusted_Connection=yes;"
                        )
        elif self.user != '' and self.pwd != '':
            conn_data = (
                            "Driver={" + self.driver + "};"
                            f"Server={self.server};"
                            f"Database={self.database};"
                            f"UID={self.user};"
                            f"PWD={self.pwd};"
                        )
        else:
            self.log.show_error_message('Please enter valid database information.')

        self.conn = odbc.connect(conn_data)

    def open_connection(self):
        self.log.show_progress_message(f'\nSuccessful database connection!', display_time=True)
        self.log.show_progress_message(f'Driver:   {self.driver}')
        self.log.show_progress_message(f'Server:   {self.server}')
        self.log.show_progress_message(f'Database: {self.database}')
        self.log.show_progress_message(f'User:     {self.user}')
        self.log.display_date()
        return self

    def cursor(self):
        return self.conn.cursor()

    def close_connection(self):
        self.log.show_progress_message(f'\nDatabase connection closed!\n')
        return self.conn.close()
