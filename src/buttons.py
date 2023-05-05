from tkinter import messagebox
import pyodbc as odbc
from src.constants import INSERT_SCRIPT_ROWS_LIMIT, UPDATE_SCRIPT_ROWS_LIMIT
from src.datainput import __get_path_leaf, __select_directory, __get_input_files_list, __read_csv
from src.scriptrowbuilder import __get_values_list, __get_values_string
from src.scriptrowbuilder import __get_insert_cols_str, __get_insert_script_row
from src.scriptrowbuilder import __get_update_values_cols_str, __get_update_script_row


def insert_scripts(tbx_table):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path)
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:
            # Importação da tabela
            table = __read_csv(file)
            # Definição do comando SQL
            cols_str = __get_insert_cols_str(table)
            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql", 'w+')

            # Iteração sobre as linhas da tabela
            for i in range(len(table)):
                if i not in [0, len(table)] and i % INSERT_SCRIPT_ROWS_LIMIT == 0:
                    script.close()
                    n_script += 1
                    script = open(f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql", 'w+')
                    values_list = __get_values_list(table, i)
                    values_str = __get_values_string(values_list)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
                elif i == len(table):
                    values_list = __get_values_list(table, i)
                    values_str = __get_values_string(values_list)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
                    script.close()
                else:
                    values_list = __get_values_list(table, i)
                    values_str = __get_values_string(values_list)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
        messagebox.showinfo('Processo Concluído', f'INSERT script(s) gerado(s) com sucesso na pasta {folder_path}.')


def update_scripts(tbx_table):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path)
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:
            # Importação da tabela
            table = __read_csv(file)
            # Definição do comando SQL
            cols_list = list(table.columns)
            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql", 'w+')

            # Iteração sobre as linhas da tabela
            for i in range(len(table)):
                if i not in [0, len(table)] and i % UPDATE_SCRIPT_ROWS_LIMIT == 0:
                    n_script += 1
                    script.close()
                    script = open(f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql", 'w+')
                    cols_values_str = __get_update_values_cols_str(table, i, cols_list)
                    row = __get_update_script_row(input_table, cols_values_str, table, i)
                    script.write(row)
                elif i == len(table):
                    cols_values_str = __get_update_values_cols_str(table, i, cols_list)
                    row = __get_update_script_row(input_table, cols_values_str, table, i)
                    script.write(row)
                    script.close()
                else:
                    cols_values_str = __get_update_values_cols_str(table, i, cols_list)
                    row = __get_update_script_row(input_table, cols_values_str, table, i)
                    script.write(row)
        messagebox.showinfo('Processo Concluído', f'UPDATE script(s) gerado(s) com sucesso na pasta {folder_path}.')


def insert_data_into_db(driver_var, tbx_server, tbx_db, tbx_user='', tbx_pwd=''):
    folder_path = __select_directory()
    input_scripts_list = __get_input_files_list(folder_path)

    driver = driver_var.get()
    server = tbx_server.get("1.0", "end-1c")
    database = tbx_db.get("1.0", "end-1c")
    user = tbx_user.get("1.0", "end-1c")
    pwd = tbx_pwd.get("1.0", "end-1c")

    if folder_path == '' or server == '' or database == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_scripts_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        if user == '' and pwd == '':
            conn_data = (
                    "Driver={" + driver + "};"
                                          f"Server={server};"
                                          f"Database={database};"
                                          "Trusted_Connection=yes;"
            )
        else:
            conn_data = (
                    "Driver={" + driver + "};"
                                          f"Server={server};"
                                          f"Database={database};"
                                          f"UID={user};"
                                          f"PWD={pwd};"
            )

        conn = odbc.connect(conn_data)

        messagebox.showinfo('ODBC', f'Conexão com o banco {database} realizada com sucesso!')

        count = 1

        for script_file in input_scripts_list:
            with open(script_file, 'r') as inserts:
                script = inserts.read()
                for statement in script.split(';'):
                    with conn.cursor() as cursor:
                        cursor.execute(statement)

            print(f"Script {__get_path_leaf(script_file)} executado com sucesso! ({count}/{len(input_scripts_list)})")

            count += 1

        conn.close()

        messagebox.showinfo('Processo Concluído',
                            f'{len(input_scripts_list)} script(s) executado(s) com sucesso no banco {database}!')
