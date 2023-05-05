from src.constants import TABLE_KEY_RELATIONSHIP
import pandas as pd


def __get_date_cols_index(table):
    date_cols_idxs = [i for i, col in enumerate(list(table.columns)) if 'date' in col.lower()]
    return date_cols_idxs


def __get_values_list(table, row_idx):
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
    return values_list


def __get_values_string(values_list):
    return ''.join(map(str, values_list))[:-1]


# Scripts de INSERT
def __get_insert_cols_str(table):
    cols_list = [f'[{col}],' for col in table.columns]
    cols_str = ''.join(map(str, cols_list))[:-1]
    return cols_str


def __get_insert_script_row(input_table, cols_str, values_str):
    row = f"INSERT INTO {input_table} ({cols_str}) values ({values_str});\n"
    return row


# Scripts de UPDATE
def __get_update_values_cols_str(table, row_idx, cols_list):
    values_list = __get_values_list(table, row_idx)
    cols_values_list = [f"{col} = {value}" for col, value in zip(cols_list, values_list)]
    cols_values_str = ''.join(map(str, cols_values_list))[:-1]
    return cols_values_str


def __get_update_script_row(input_table, cols_values_str, table, row_idx):
    key = TABLE_KEY_RELATIONSHIP[input_table]
    # Chave primária
    if len(key) == 1:
        row = f"""UPDATE {input_table} SET {cols_values_str}\nWHERE {key[0]} = '{table.loc[row_idx, key[0]]}';\n"""
    # Chave composta
    else:
        row = f"""UPDATE {input_table} SET {cols_values_str}\nWHERE {key[0]} = '{table.loc[row_idx, key[0]]}' AND {key[1]} = '{table.loc[row_idx, key[1]]}';\n"""
    return row
