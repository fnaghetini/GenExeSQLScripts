from tkinter import *
from glob import glob
import pandas as pd
from tkinter import messagebox
from idlelib.tooltip import Hovertip

######################################################################################
# ------------------------------------- Função ------------------------------------- #
######################################################################################


def insert_scripts():

    folder_path = tbx_dir1.get("1.0", "end-1c")
    input_files_list = [f.replace('\\', '/') for f in glob(f"{folder_path}/*.csv")]
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:

            # Tabela como DataFrame
            table = pd.read_csv(file, sep=',', header=0, dtype=str)

            # Colunas
            cols_list = [f'[{col}],' for col in table.columns]
            cols_str = ''.join(map(str, cols_list))[:-1]

            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql", 'w+')

            # Loop
            for i in range(len(table)):

                if i != 0 and i != len(table) and i % 20000 == 0:
                    n_script += 1
                    script.close()

                    script = open(f"{file[:-4]}_INSERT_pt0{str(n_script)}.sql", 'w+')

                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    values_str = ''.join(map(str, values_list))[:-1]
                    row = f"INSERT INTO {input_table} ({cols_str}) values ({values_str});\n"
                    script.write(row)

                elif i == len(table):
                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    values_str = ''.join(map(str, values_list))[:-1]

                    row = f"INSERT INTO {input_table} ({cols_str}) values ({values_str});\n"
                    script.write(row)

                    script.close()

                else:
                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    values_str = ''.join(map(str, values_list))[:-1]

                    row = f"INSERT INTO {input_table} ({cols_str}) values ({values_str});\n"
                    script.write(row)

    messagebox.showinfo('Processo Concluído', f'INSERT script(s) gerado(s) com sucesso na pasta {folder_path}.')


def update_scripts():

    folder_path = tbx_dir1.get("1.0", "end-1c")
    input_files_list = [f.replace('\\', '/') for f in glob(f"{folder_path}/*.csv")]
    input_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:

            # Tabela como DataFrame
            table = pd.read_csv(file, sep=',', header=0, dtype=str)

            # Colunas
            cols_list = list(table.columns)

            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql", 'w+')

            # Loop
            for i in range(len(table)):

                if i != 0 and i != len(table) and i % 20000 == 0:
                    n_script += 1
                    script.close()

                    script = open(f"{file[:-4]}_UPDATE_pt0{str(n_script)}.sql", 'w+')

                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    cols_values_list = [f"{col} = {value}" for col, value in zip(cols_list, values_list)]
                    cols_values_str = ''.join(map(str, cols_values_list))[:-1]

                    row = f"UPDATE {input_table} SET {cols_values_str} WHERE sample_number = '{table.loc[i,'sample_number']}';\n"
                    script.write(row)

                elif i == len(table):
                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    cols_values_list = [f"{col} = {value}" for col, value in zip(cols_list, values_list)]
                    cols_values_str = ''.join(map(str, cols_values_list))[:-1]

                    row = f"UPDATE {input_table} SET {cols_values_str} WHERE sample_number = '{table.loc[i,'sample_number']}';\n"
                    script.write(row)

                    script.close()

                else:
                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    cols_values_list = [f"{col} = {value}" for col, value in zip(cols_list, values_list)]
                    cols_values_str = ''.join(map(str, cols_values_list))[:-1]

                    row = f"UPDATE {input_table} SET {cols_values_str} WHERE sample_number = '{table.loc[i, 'sample_number']}';\n"
                    script.write(row)

    messagebox.showinfo('Processo Concluído', f'UPDATE script(s) gerado(s) com sucesso na pasta {folder_path}.')


def insert_data():
    pass


######################################################################################
# ------------------------------------ Interface ----------------------------------- #
######################################################################################

# Criação da janela principal
root = Tk()

# Ícone
root.wm_iconbitmap('datamine.ico')
# Título
root.title("Datamine GDMS")
# Dimensões da tabela
root.geometry("500x430")
# Configuração de background
root.configure(background='white')

# Widgets
txt_title1 = Label(root, text="Geração de Scripts SQL", bg='white', fg='black', font="lucida 12 bold")
txt_dir1 = Label(root, text="Diretório:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_dir1 = Text(root, height=1, width=30, bg='light yellow')
txt_table = Label(root, text="Nome da Tabela:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_table = Text(root, height=1, width=30, bg='light yellow')
btn_insert_scripts = Button(root, text="Gerar INSERT Scripts", width=20, justify=RIGHT, command=lambda: insert_scripts())
btn_update_scripts = Button(root, text="Gerar UPDATE Scripts", width=20, justify=CENTER, command=lambda: update_scripts())

txt_title2 = Label(root, text="Inserção dos Dados no Banco", bg='white', fg='black', font="lucida 12 bold")
txt_dir2 = Label(root, text="Diretório:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_dir2 = Text(root, height=1, width=30, bg='light yellow')
txt_server = Label(root, text="Servidor:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_server = Text(root, height=1, width=30, bg='light yellow')
txt_db = Label(root, text="Banco de Dados:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_db = Text(root, height=1, width=30, bg='light yellow')
txt_user = Label(root, text="Usuário:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_user = Text(root, height=1, width=30, bg='light yellow')
txt_pwd = Label(root, text="Senha:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_pwd = Text(root, height=1, width=30, bg='light yellow')
btn_insert_data = Button(root, text="Inserir Dados", width=20, command=lambda: insert_data())
txt_version = Label(root, text="v0.0.3", bg='white', fg='black', justify=RIGHT, anchor='e')

# Associando widgets à janela principal
txt_title1.grid(row=0, column=0, columnspan=2, pady=10)
txt_dir1.grid(row=1, column=0, pady=5, sticky=W)
tbx_dir1.grid(row=1, column=1)
txt_table.grid(row=2, column=0, pady=5, sticky=W)
tbx_table.grid(row=2, column=1)
btn_insert_scripts.grid(row=3, column=0, pady=10)
btn_update_scripts.grid(row=3, column=1, pady=10)

txt_title2.grid(row=4, column=0, columnspan=2, pady=10)
txt_dir2.grid(row=5, column=0, pady=5, sticky=W)
tbx_dir2.grid(row=5, column=1)
txt_server.grid(row=6, column=0, pady=5, sticky=W)
tbx_server.grid(row=6, column=1)
txt_db.grid(row=7, column=0, pady=5, sticky=W)
tbx_db.grid(row=7, column=1)
txt_user.grid(row=8, column=0, pady=5, sticky=W)
tbx_user.grid(row=8, column=1)
txt_pwd.grid(row=9, column=0, pady=5, sticky=W)
tbx_pwd.grid(row=9, column=1)
btn_insert_data.grid(row=10, column=0, columnspan=2, pady=10)
txt_version.grid(row=11, column=1, sticky=E)

# Tooltips
tip_dir1 = Hovertip(tbx_dir1, "Caminho para a pasta que contém\n os CSVs de entrada.")
tip_table = Hovertip(tbx_table, "Nome da tabela do banco que \nreceberá os dados.")
tip_dir2 = Hovertip(tbx_dir2, "Caminho para a pasta que contém\n os scripts SQL de entrada.")
tip_server = Hovertip(tbx_server, "Insira o nome do servidor.")
tip_db = Hovertip(tbx_db, "Insira o nome do banco de dados.")
tip_user = Hovertip(tbx_user, "Insira o nome do usuário\n para efetuar o logon.")
tip_pwd = Hovertip(tbx_pwd, "Insira a senha para efetuar o logon.")


# Execução do app
root.mainloop()
