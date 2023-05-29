import ntpath
from tkinter import filedialog
from glob import glob
import pandas as pd


def __get_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def __select_directory():
    folderpath = filedialog.askdirectory(initialdir='/', title='Selecione uma Pasta')
    return folderpath


def __get_input_files_list(folder_path, extension):
    return [f.replace('\\', '/') for f in glob(f"{folder_path}/*.{extension}")]


def __read_csv(file):
    return pd.read_csv(file, sep=',', header=0, dtype=str, encoding='utf-8', low_memory=False)


def __clean_table_column_names(table):
    return table.columns.str.strip().str.lower()
