import pyodbc as odbc
from tkinter import messagebox


class Database:
    def __init__(self, driver, server, database, user='', pwd=''):
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
            messagebox.showerror('Erro', 'Verifique se as informações estão corretamente preenchidas.')
            raise Exception('Erro ao conectar com o banco.')
        self.conn = odbc.connect(conn_data)

    def open_connection(self):
        print(f"Conexão bem sucedida com o banco {self.database}!")
        return self

    def cursor(self):
        return self.conn.cursor()

    def close_connection(self):
        print(f"Conexão com o banco {self.database} encerrada!")
        return self.conn.close()
