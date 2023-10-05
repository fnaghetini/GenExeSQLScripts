from tkinter import messagebox
from src.constants import GENERATE_SCRIPTS_LOG_PATH, EXECUTE_SCRIPTS_LOG_PATH
from src.constants import DATE_CONVENTIONS, TABLE_KEY_RELATIONSHIP
from src.constants import INSERT_SCRIPT_ROWS_LIMIT, UPDATE_SCRIPT_ROWS_LIMIT, DELETE_SCRIPT_ROWS_LIMIT
from src.datainput import __get_path_leaf, __select_directory, __get_input_files_list
from src.datainput import __read_csv, __clean_table_column_names
from src.log import Log
from src.auditicolumnsbuilder import __get_auditing_cols
from src.scriptheaderbuilder import __build_script_header
from src.scriptrowbuilder import __get_values_list, __get_values_string
from src.scriptrowbuilder import __get_insert_cols_str, __get_insert_script_row
from src.scriptrowbuilder import __get_update_values_cols_str, __get_update_script_row
from src.scriptrowbuilder import __get_delete_script_row
from src.database import Database


def generate_insert_scripts(tbx_table, date_convention_var, cbx_modify_cols_var):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path, 'csv')
    input_table = str(tbx_table.get("1.0", "end-1c")).lower()
    date_convention = DATE_CONVENTIONS[date_convention_var.get()]

    log = Log(GENERATE_SCRIPTS_LOG_PATH)
    log.show_progress_message('GENERATING INSERT SCRIPTS...\n')
    log.display_date()

    if folder_path == '':
        log.show_error_message('Please choose a valid folder!')
        return
    elif len(input_files_list) == 0:
        log.show_error_message(f'There is no CSV file in {folder_path}')
        return
    else:
        for file in input_files_list:
            table = __read_csv(file)
            table.columns = __clean_table_column_names(table)

            if cbx_modify_cols_var == 1:
                __get_auditing_cols(table, date_convention[1])

            cols_str = __get_insert_cols_str(table)

            n_script = 1
            script_name = f"{file[:-4]}_INSERT_pt{str(n_script).zfill(3)}.sql"
            script = open(script_name, 'w+')
            header = __build_script_header(script_name.rsplit('/', 1)[1], script_type='INSERT')
            script.write(header)

            for i in range(len(table)):
                if i not in [0, len(table)] and i % INSERT_SCRIPT_ROWS_LIMIT == 0:
                    script.close()
                    log.show_progress_message(f"\nScript {script_name.rsplit('/', 1)[1]} generated successfully.",
                                              display_time=True)
                    n_script += 1
                    script_name = f"{file[:-4]}_INSERT_pt{str(n_script).zfill(3)}.sql"
                    script = open(script_name, 'w+')
                    header = __build_script_header(script_name.rsplit('/', 1)[1], script_type='INSERT')
                    script.write(header)
                    values_list = __get_values_list(table, i, date_convention[0])
                    values_str = __get_values_string(values_list)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
                elif i == len(table):
                    values_list = __get_values_list(table, i, date_convention[0])
                    values_str = __get_values_string(values_list)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)
                    script.close()
                    log.show_progress_message(f"\nScript {script_name.rsplit('/', 1)[1]} generated successfully.",
                                              display_time=True)
                else:
                    values_list = __get_values_list(table, i, date_convention[0])
                    values_str = __get_values_string(values_list)
                    row = __get_insert_script_row(input_table, cols_str, values_str)
                    script.write(row)

        log.display_execution_time(full_exec_time=True)
        log.show_completion_message(f'INSERT script(s) successfully generated in the folder {folder_path}.')
        log.close_logfile()


def generate_update_scripts(tbx_table, date_convention_var, cbx_modify_cols_var):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path, 'csv')
    input_table = str(tbx_table.get("1.0", "end-1c")).lower()
    date_convention = DATE_CONVENTIONS[date_convention_var.get()]

    log = Log(GENERATE_SCRIPTS_LOG_PATH)
    log.show_progress_message('GENERATING UPDATE SCRIPTS...\n')
    log.display_date()

    if folder_path == '':
        log.show_error_message('Please choose a valid folder!')
    elif len(input_files_list) == 0:
        log.show_error_message(f'There is no CSV file in {folder_path}')
    elif input_table not in list(TABLE_KEY_RELATIONSHIP.keys()):
        log.show_error_message(f"There is no PK for {input_table}. Please contact admin to add the PK.")
        return
    else:
        for file in input_files_list:
            table = __read_csv(file)
            table.columns = __clean_table_column_names(table)

            if cbx_modify_cols_var == 1:
                __get_auditing_cols(table, date_convention[1])

            cols_list = list(table.columns)

            n_script = 1
            script_name = f"{file[:-4]}_UPDATE_pt{str(n_script).zfill(3)}.sql"
            script = open(script_name, 'w+')
            header = __build_script_header(script_name.rsplit('/', 1)[1], script_type='UPDATE')
            script.write(header)

            for i in range(len(table)):
                if i not in [0, len(table)] and i % UPDATE_SCRIPT_ROWS_LIMIT == 0:
                    n_script += 1
                    script.close()
                    log.show_progress_message(f"\nScript {script_name.rsplit('/', 1)[1]} generated successfully.",
                                              display_time=True)
                    script_name = f"{file[:-4]}_UPDATE_pt{str(n_script).zfill(3)}.sql"
                    script = open(script_name, 'w+')
                    header = __build_script_header(script_name.rsplit('/', 1)[1], script_type='UPDATE')
                    script.write(header)
                    cols_values_str = __get_update_values_cols_str(table, i, cols_list, date_convention[0])
                    row = __get_update_script_row(input_table, cols_values_str, table, i)
                    script.write(row)
                elif i == len(table):
                    cols_values_str = __get_update_values_cols_str(table, i, cols_list, date_convention[0])
                    row = __get_update_script_row(input_table, cols_values_str, table, i)
                    script.write(row)
                    script.close()
                    log.show_progress_message(f"\nScript {script_name.rsplit('/', 1)[1]} generated successfully.",
                                              display_time=True)
                else:
                    cols_values_str = __get_update_values_cols_str(table, i, cols_list, date_convention[0])
                    row = __get_update_script_row(input_table, cols_values_str, table, i)
                    script.write(row)
        log.display_execution_time(full_exec_time=True)
        log.show_completion_message(f'UPDATE script(s) successfully generated in the folder {folder_path}.')
        log.close_logfile()


def generate_delete_scripts(tbx_table):
    folder_path = __select_directory()
    input_files_list = __get_input_files_list(folder_path, 'csv')
    input_table = str(tbx_table.get("1.0", "end-1c")).lower()

    log = Log(GENERATE_SCRIPTS_LOG_PATH)
    log.show_progress_message('GENERATING INSERT SCRIPTS...\n')
    log.display_date()

    if folder_path == '':
        log.show_error_message('Please choose a valid folder!')
    elif len(input_files_list) == 0:
        log.show_error_message(f'There is no CSV file in {folder_path}')
    elif input_table not in list(TABLE_KEY_RELATIONSHIP.keys()):
        log.show_error_message(f"There is no PK for {input_table}. Please contact admin to add the PK.")
        return
    else:
        for file in input_files_list:
            table = __read_csv(file)
            table.columns = __clean_table_column_names(table)

            n_script = 1
            script_name = f"{file[:-4]}_DELETE_pt{str(n_script).zfill(3)}.sql"
            script = open(script_name, 'w+')
            header = __build_script_header(script_name.rsplit('/', 1)[1], script_type='DELETE')
            script.write(header)

            for i in range(len(table)):
                if i not in [0, len(table)] and i % DELETE_SCRIPT_ROWS_LIMIT == 0:
                    n_script += 1
                    script.close()
                    log.show_progress_message(f"\nScript {script_name.rsplit('/', 1)[1]} generated successfully.",
                                              display_time=True)
                    script_name = f"{file[:-4]}_DELETE_pt{str(n_script).zfill(3)}.sql"
                    script = open(script_name, 'w+')
                    header = __build_script_header(script_name.rsplit('/', 1)[1], script_type='DELETE')
                    script.write(header)
                    row = __get_delete_script_row(input_table, table, i)
                    script.write(row)
                elif i == len(table):
                    row = __get_delete_script_row(input_table, table, i)
                    script.write(row)
                    script.close()
                    log.show_progress_message(f"\nScript {script_name.rsplit('/', 1)[1]} generated successfully.",
                                              display_time=True)
                else:
                    row = __get_delete_script_row(input_table, table, i)
                    script.write(row)
        log.display_execution_time(full_exec_time=True)
        log.show_completion_message(f'DELETE script(s) successfully generated in the folder {folder_path}.')
        log.close_logfile()


def insert_data_into_db(driver_var, tbx_server, tbx_db, tbx_user='', tbx_pwd=''):
    folder_path = __select_directory()
    input_scripts_list = __get_input_files_list(folder_path, 'sql')

    log = Log(EXECUTE_SCRIPTS_LOG_PATH)
    log.show_progress_message('EXECUTING SQL SCRIPTS...\n')
    log.display_date()

    db = Database(log,
                  driver_var.get(),
                  tbx_server.get("1.0", "end-1c"),
                  tbx_db.get("1.0", "end-1c"),
                  tbx_user.get("1.0", "end-1c"),
                  tbx_pwd.get("1.0", "end-1c")
                  )
    db.open_connection()

    count = 1

    for script_file in input_scripts_list:
        reseted_start_time = log.reset_start_time()
        with open(script_file, 'r') as inserts:
            script = inserts.read()
            for statement in script.split(';'):
                with db.cursor() as cursor:
                    cursor.execute(statement)

        log.show_progress_message(f'\nScript {__get_path_leaf(script_file)} executed successfully! ({count}/{len(input_scripts_list)})')
        log.display_execution_time(new_start_time=reseted_start_time)

        count += 1

    db.close_connection()

    log.display_execution_time(full_exec_time=True)
    log.show_completion_message(f'{len(input_scripts_list)} script(s) executed successfully!')
    log.close_logfile()
