from tkinter import *
from glob import glob
import pandas as pd
from tkinter import messagebox
from idlelib.tooltip import Hovertip

######################################################################################
# ------------------------------------- Função ------------------------------------- #
######################################################################################


def btn_execute():

    folder_path = tbx_dir.get("1.0", "end-1c")
    input_files_list = [f.replace('\\', '/') for f in glob(f"{folder_path}/*.csv")]
    insert_table = tbx_table.get("1.0", "end-1c")

    if folder_path == '':
        messagebox.showerror('Erro', "Por favor, preencha todos os campos!")
    elif len(input_files_list) == 0:
        messagebox.showerror('Erro', f"Não há arquivos .csv na pasta {folder_path}.")
    else:
        for file in input_files_list:

            # Tabela como DataFrame
            table = pd.read_csv(file, sep=',', header=0)

            # Colunas
            cols_list = [f'[{col}],' for col in table.columns]
            cols_str = ''.join(map(str, cols_list))[:-1]

            # Criação do 1° script SQL
            n_script = 1
            script = open(f"{file[:-4]}_pt0{str(n_script)}.sql", 'w+')

            # Loop
            for i in range(len(table)):

                if i != 0 and i != len(table) and i % 20000 == 0:
                    n_script += 1
                    script.close()

                    script = open(f"{file[:-4]}_pt0{str(n_script)}.sql", 'w+')

                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    values_str = ''.join(map(str, values_list))[:-1]
                    row = f"INSERT INTO {insert_table} ({cols_str}) values ({values_str});\n"
                    script.write(row)

                elif i == len(table):
                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    values_str = ''.join(map(str, values_list))[:-1]

                    row = f"INSERT INTO {insert_table} ({cols_str}) values ({values_str});\n"
                    script.write(row)

                    script.close()

                else:
                    values_list = [f"'{value}'," if not pd.isna(value) else "NULL," for value in table.iloc[i, :]]
                    values_str = ''.join(map(str, values_list))[:-1]

                    row = f"INSERT INTO {insert_table} ({cols_str}) values ({values_str});\n"
                    script.write(row)

    messagebox.showinfo('Processo Concluído', f'Script(s) gerado(s) com sucesso na pasta {folder_path}.')


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
root.geometry("380x180")
# Configuração de background
root.configure(background='white')

# Widgets
txt_title = Label(root, text="Geração de INSERT Scripts", bg='white', fg='black', font="lucida 12 bold")
txt_dir = Label(root, text="Diretório:", bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_dir = Text(root, height=1, width=30, bg='light yellow')
txt_table = Label(root, text="Nome da Tabela:", bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_table = Text(root, height=1, width=30, bg='light yellow')
btn_exec = Button(root, text="Executar", width=15, command=lambda: btn_execute())
txt_version = Label(root, text="v0.0.1", bg='white', fg='black', justify=RIGHT, anchor='e')

# Associando widgets à janela principal
txt_title.grid(row=0, column=0, columnspan=2, pady=10)
txt_dir.grid(row=1, column=0, pady=5, sticky=W)
tbx_dir.grid(row=1, column=1)
txt_table.grid(row=3, column=0, pady=5, sticky=W)
tbx_table.grid(row=3, column=1)
btn_exec.grid(row=4, column=0, columnspan=2, pady=10)
txt_version.grid(row=5, column=1, sticky=E)

# Tooltips
tip_dir = Hovertip(tbx_dir, "Caminho para a pasta que contém\n os CSVs de entrada.")
tip_table = Hovertip(tbx_table, "Nome da tabela do banco que \nreceberá os dados.")

# Execução do app
root.mainloop()
