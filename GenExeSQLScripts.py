from tkinter import *
from idlelib.tooltip import Hovertip
from src.constants import DATE_CONVENTIONS
from src.buttons import insert_scripts, update_scripts, insert_data_into_db


######################################################################################
# ------------------------------------ Interface ----------------------------------- #
######################################################################################

# Criação da janela principal
root = Tk()

# Título
root.title("Datamine GDMS")
# Dimensões da tabela
root.geometry("500x480")
# Configuração de background
root.configure(background='white')

# Criação dos widgets - Geração de Scripts SQL
txt_title1 = Label(root, text="Geração de Scripts SQL", bg='white', fg='black', font="lucida 12 bold")
txt_table = Label(root, text="Nome da Tabela:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_table = Text(root, height=1, width=30, bg='light yellow')

txt_date_convention = Label(root, text="Convenção de Data:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
date_convention_var = StringVar(root)
date_convention_var.set("dd/mm/yyyy")
pkl_date_convention = OptionMenu(root, date_convention_var, *list(DATE_CONVENTIONS.keys()))
pkl_date_convention.config(height=1, width=34, bg='light yellow', highlightcolor='white', highlightbackground='white')

cbx_modify_cols_var = IntVar()
cbx_modify_cols = Checkbutton(root, text="Gerar colunas de modificação", bg='white', fg='black',
                              variable=cbx_modify_cols_var)

btn_insert_scripts = Button(root, text="Gerar INSERT Script(s)", width=20, justify=CENTER, cursor='hand2',
                            command=lambda: insert_scripts(tbx_table, date_convention_var, cbx_modify_cols_var.get()))
btn_update_scripts = Button(root, text="Gerar UPDATE Script(s)", width=20, justify=CENTER, cursor='hand2',
                            command=lambda: update_scripts(tbx_table, cbx_modify_cols_var.get()))

# Criação dos widgets - Execução de Scripts SQL
txt_title2 = Label(root, text="Execução de Scripts SQL", bg='white', fg='black', font="lucida 12 bold")
txt_driver = Label(root, text="Driver:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
driver_var = StringVar(root)
driver_var.set("SQL Server")
pkl_driver = OptionMenu(root, driver_var, "SQL Server", "ODBC Driver 17 for SQL Server")
pkl_driver.config(height=1, width=34, bg='light yellow', highlightcolor='white', highlightbackground='white')
txt_server = Label(root, text="Servidor:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_server = Text(root, height=1, width=30, bg='light yellow')
txt_db = Label(root, text="Banco de Dados:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_db = Text(root, height=1, width=30, bg='light yellow')
txt_user = Label(root, text="Usuário:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_user = Text(root, height=1, width=30, bg='white')
txt_pwd = Label(root, text="Senha:", width=30, bg='white', fg='black', justify=LEFT, anchor='w', padx=10)
tbx_pwd = Text(root, height=1, width=30, bg='white')

btn_insert_data = Button(root, text="Executar Script(s)", width=20, justify=CENTER, cursor='hand2',
                         command=lambda: insert_data_into_db(driver_var, tbx_server, tbx_db, tbx_user, tbx_pwd))
txt_version = Label(root, text="v0.0.9", bg='white', fg='black', justify=RIGHT, anchor='e')

# Posição dos widgets - Geração de Scripts SQL
txt_title1.grid(row=0, column=0, columnspan=2, pady=10)
txt_table.grid(row=1, column=0, pady=5, sticky=W)
tbx_table.grid(row=1, column=1)

txt_date_convention.grid(row=2, column=0, pady=5, sticky=W)
pkl_date_convention.grid(row=2, column=1)

cbx_modify_cols.grid(row=3, column=0, columnspan=2, pady=10)

btn_insert_scripts.grid(row=4, column=0, pady=10)
btn_update_scripts.grid(row=4, column=1, pady=10)

# Posição dos widgets - Execução de Scripts SQL
txt_title2.grid(row=5, column=0, columnspan=2, pady=10)
txt_driver.grid(row=6, column=0, pady=5, sticky=W)
pkl_driver.grid(row=6, column=1)
txt_server.grid(row=7, column=0, pady=5, sticky=W)
tbx_server.grid(row=7, column=1)
txt_db.grid(row=8, column=0, pady=5, sticky=W)
tbx_db.grid(row=8, column=1)
txt_user.grid(row=9, column=0, pady=5, sticky=W)
tbx_user.grid(row=9, column=1)
txt_pwd.grid(row=10, column=0, pady=5, sticky=W)
tbx_pwd.grid(row=10, column=1)
btn_insert_data.grid(row=11, column=0, columnspan=2, pady=10)
txt_version.grid(row=12, column=1, sticky=E)

# Tooltips
tip_table = Hovertip(tbx_table, "Nome da tabela do banco que \nreceberá os dados.")
tip_server = Hovertip(tbx_server, "Insira o nome do servidor.")
tip_db = Hovertip(tbx_db, "Insira o nome do banco de dados.")
tip_user = Hovertip(tbx_user, "Insira o usuário (Database Authentication).")
tip_pwd = Hovertip(tbx_pwd, "Insira a senha (Database Authentication).")

# Execução do app
root.mainloop()
