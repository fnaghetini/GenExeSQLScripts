from datetime import datetime, date
from tkinter import messagebox


class Log:
    def __init__(self, path):
        self.logfile = open(path, mode='w')
        self.execution_date = date.today().strftime("%d/%m/%Y")
        self.start_time = datetime.now()

    def display_date(self):
        execution_date = f'Data: {self.execution_date}\n'
        self.logfile.write(execution_date)
        self.logfile.flush()

    def show_error_message(self, error_message):
        full_error_message = f'ERRO ({datetime.now().strftime("%H:%M:%S")}): {error_message}!\n'
        self.logfile.write(full_error_message)
        self.logfile.flush()
        messagebox.showerror('Erro', full_error_message)
        raise Exception(full_error_message)

    def show_progress_message(self, progress_message, display_time=False):
        if display_time:
            datetime_progress_message = f'{progress_message} ({datetime.now().strftime("%H:%M:%S")}).\n'
            self.logfile.write(datetime_progress_message)
            self.logfile.flush()
        else:
            self.logfile.write(f'{progress_message}\n')
            self.logfile.flush()

    def reset_start_time(self):
        return datetime.now()

    def display_execution_time(self, new_start_time=None, full_exec_time=False):
        if new_start_time is not None:
            execution_time = datetime.now() - new_start_time
            self.logfile.write(f'Tempo de execução: {execution_time}\n')
            self.logfile.flush()
        else:
            execution_time = datetime.now() - self.start_time
            if full_exec_time:
                self.logfile.write(f'\nTEMPO DE EXECUÇÃO TOTAL: {execution_time}\n\n')
            else:
                self.logfile.write(f'Tempo de execução: {execution_time}\n')
            self.logfile.flush()

    def show_completion_message(self, completion_message, write_log=True, show_messagebox=True):
        if write_log:
            full_completion_message = f'\n\nPROCESSO CONCLUÍDO! {completion_message}'
            self.logfile.write(full_completion_message)
            self.logfile.flush()
        if show_messagebox:
            messagebox.showinfo('Processo Concluído', completion_message)

    def close_logfile(self):
        if self.logfile:
            self.logfile.close()
