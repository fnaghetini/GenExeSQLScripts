from tkinter import messagebox
from src.constants import INSERT_SCRIPT_ROWS_LIMIT, UPDATE_SCRIPT_ROWS_LIMIT
from src.datainput import __get_path_leaf, __select_directory, __get_input_files_list, __read_csv
from src.auditicolumnsbuilder import __get_autiting_cols
from src.scriptheaderbuilder import __build_script_header
from src.scriptrowbuilder import __get_values_list, __get_values_string
from src.scriptrowbuilder import __get_insert_cols_str, __get_insert_script_row
from src.scriptrowbuilder import __get_update_values_cols_str, __get_update_script_row
from src.database import Database


def insert_scripts(tbx_table, cbx_modify_cols_var):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path, 'csv')
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:
            # Importação da tabela
            table = __read_csv(file)
            if cbx_modify_cols_var == 1:
                __get_autiting_cols(table)
            # Definição do comando SQL
            cols_str = __get_insert_cols_str(table)
            # Criação do 1° script SQL
            n_script = 1
            script_name = f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql"
            script = open(script_name, 'w+')
            header = __build_script_header(script_name.rsplit('/', 1)[1])
            script.write(header)

            # Iteração sobre as linhas da tabela
            for i in range(len(table)):
                if i not in [0, len(table)] and i % INSERT_SCRIPT_ROWS_LIMIT == 0:
                    script.close()
                    n_script += 1
                    script_name = f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql"
                    script = open(script_name, 'w+')
                    header = __build_script_header(script_name.rsplit('/', 1)[1])
                    script.write(header)
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


def update_scripts(tbx_table, cbx_modify_cols_var):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path, 'csv')
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:
            # Importação da tabela
            table = __read_csv(file)
            if cbx_modify_cols_var == 1:
                __get_autiting_cols(table)
            # Definição do comando SQL
            cols_list = list(table.columns)
            # Criação do 1° script SQL
            n_script = 1
            script_name = f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql"
            script = open(script_name, 'w+')
            header = __build_script_header(script_name.rsplit('/', 1)[1])
            script.write(header)

            # Iteração sobre as linhas da tabela
            for i in range(len(table)):
                if i not in [0, len(table)] and i % UPDATE_SCRIPT_ROWS_LIMIT == 0:
                    n_script += 1
                    script.close()
                    script_name = f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql"
                    script = open(script_name, 'w+')
                    header = __build_script_header(script_name.rsplit('/', 1)[1])
                    script.write(header)
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
        print(cbx_modify_cols_var)


def insert_data_into_db(driver_var, tbx_server, tbx_db, tbx_user='', tbx_pwd=''):
    folder_path = __select_directory()
    input_scripts_list = __get_input_files_list(folder_path, 'sql')

    db = Database(driver_var.get(),
                  tbx_server.get("1.0", "end-1c"),
                  tbx_db.get("1.0", "end-1c"),
                  tbx_user.get("1.0", "end-1c"),
                  tbx_pwd.get("1.0", "end-1c")
                  )
    db.open_connection()

    count = 1

    for script_file in input_scripts_list:
        with open(script_file, 'r') as inserts:
            script = inserts.read()
            for statement in script.split(';'):
                with db.cursor() as cursor:
                    cursor.execute(statement)

        print(f"Script {__get_path_leaf(script_file)} executado com sucesso! ({count}/{len(input_scripts_list)})")

        count += 1

    db.close_connection()

    messagebox.showinfo('Processo Concluído',
                        f'{len(input_scripts_list)} script(s) executado(s) com sucesso!')
