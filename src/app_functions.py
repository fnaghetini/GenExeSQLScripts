import ntpath
import pandas as pd
from glob import glob
from tkinter import messagebox
from tkinter import filedialog
import pyodbc as odbc
from constants import TABLE_KEY_RELATIONSHIP


def __get_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def __select_directory():
    folderpath = filedialog.askdirectory(initialdir='/', title='Selecione uma Pasta')
    return folderpath


def __get_insert_cols_str(table):
    cols_list = [f'[{col}],' for col in table.columns]
    cols_str = ''.join(map(str, cols_list))[:-1]
    return cols_str


def __get_date_cols_index(table):
    date_cols_idxs = [i for i, col in enumerate(list(table.columns)) if 'date' in col.lower()]
    return date_cols_idxs


def __get_insert_values_str(table, row_idx):
    date_cols_idxs = __get_date_cols_index(table)
    values_list = []

    for col_idx, value in enumerate(table.iloc[row_idx, :]):
        if pd.isna(value):
            values_list.append("NULL,")
        else:
            if col_idx in date_cols_idxs:
                values_list.append(f"CONVERT(DATETIME,'{value}',103),")
            else:
                values_list.append(f"'{value}',")
    values_str = ''.join(map(str, values_list))[:-1]
    return values_str


def __get_insert_script_row(input_table, cols_str, values_str):
    row = f"INSERT INTO {input_table} ({cols_str}) values ({values_str});\n"
    return row


def __get_update_values_cols_str(table, row_idx, cols_list):
    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[row_idx, :]]
    cols_values_list = [f"{col} = {value}" for col, value in zip(cols_list, values_list)]
    cols_values_str = ''.join(map(str, cols_values_list))[:-1]
    return cols_values_str


def __get_update_script_row(input_table, cols_values_str, table, row_idx):
    key = TABLE_KEY_RELATIONSHIP[input_table]
    # Chave primária
    if len(key) == 1:
        row = f"""UPDATE {input_table} SET {cols_values_str}\n
        WHERE {key[0]} = '{table.loc[row_idx, key[0]]}';\n"""
    # Chave composta
    else:
        row = f"""UPDATE {input_table} SET {cols_values_str}\n
        WHERE {key[0]} = '{table.loc[row_idx, {key[0]}]}' AND
        {key[1]} = '{table.loc[row_idx, {key[1]}]}';\n"""
    return row


def insert_scripts(tbx_table):
    folder_path = __select_directory()
    input_files_list = [f.replace('\\', '/') for f in glob(f"{folder_path}/*.csv")]
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:
            # Importação da tabela
            table = pd.read_csv(file, sep=',', header=0, dtype=str)
            # Definição do comando SQL
            cols_str = __get_insert_cols_str(table)
            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql", 'w+')

            # Iteração sobre as linhas da tabela
            for i in range(len(table)):
                if i not in [0, len(table)] and i % 20000 == 0:
                    script.close()
                    n_script += 1
                    script = open(f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql", 'w+')
                    values_str = __get_insert_values_str(table, i)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
                elif i == len(table):
                    values_str = __get_insert_values_str(table, i)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
                    script.close()
                else:
                    values_str = __get_insert_values_str(table, i)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
        messagebox.showinfo('Processo Concluído', f'INSERT script(s) gerado(s) com sucesso na pasta {folder_path}.')


def update_scripts(tbx_table):
    folder_path = __select_directory()
    input_files_list = [f.replace('\\', '/') for f in glob(f"{folder_path}/*.csv")]
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:
            # Importação da tabela
            table = pd.read_csv(file, sep=',', header=0, dtype=str)
            # Definição do comando SQL
            cols_list = list(table.columns)
            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql", 'w+')

            # Iteração sobre as linhas da tabela
            for i in range(len(table)):
                if i not in [0, len(table)] and i % 10000 == 0:
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
    input_scripts_list = [f.replace('\\', '/') for f in glob(f"{folder_path}/*.sql")]

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
