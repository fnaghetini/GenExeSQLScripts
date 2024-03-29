from src.constants import TABLE_KEY_RELATIONSHIP
import pandas as pd


def __get_date_cols_index(table):
    date_cols_idxs = [i for i, col in enumerate(list(table.columns))
                      if 'date' in col.lower() and col.lower() not in ['last_modified_date_time', 'date_imported']]
    return date_cols_idxs


def __get_last_modified_date_time_index(table):
    last_modified_date_time_idx = [i for i, col in enumerate(list(table.columns))
                                   if col.lower() == 'last_modified_date_time']
    return last_modified_date_time_idx


def __get_date_imported_index(table):
    date_imported_idx = [i for i, col in enumerate(list(table.columns)) if col.lower() == 'date_imported']
    return date_imported_idx


def __get_values_list(table, row_idx, date_convention):
    date_cols_idxs = __get_date_cols_index(table)
    last_modified_date_time_idx = __get_last_modified_date_time_index(table)
    date_imported_idx = __get_date_imported_index(table)
    values_list = []

    for col_idx, value in enumerate(table.iloc[row_idx, :]):
        if pd.isna(value):
            values_list.append("NULL,")
        else:
            if col_idx in date_cols_idxs:
                values_list.append(f"CONVERT(DATETIME,'{value}',{date_convention}),")
            elif col_idx in last_modified_date_time_idx:
                values_list.append(f"CONVERT(DATETIME,GETDATE(),{date_convention}),")
            elif col_idx in date_imported_idx:
                values_list.append(f"CONVERT(DATETIME,'{value}',120),")
            else:
                values_list.append(f"'{value}',")
    return values_list


def __get_values_string(values_list):
    return ''.join(map(str, values_list))[:-1]


# INSERT scripts
def __get_insert_cols_str(table):
    cols_list = [f'[{col}],' for col in table.columns]
    cols_str = ''.join(map(str, cols_list))[:-1]
    return cols_str


def __get_insert_script_row(input_table, cols_str, values_str):
    row = f"INSERT INTO {input_table} ({cols_str}) values ({values_str});\n"
    return row


# UPDATE scripts
def __get_update_values_cols_str(table, row_idx, cols_list, date_convention):
    values_list = __get_values_list(table, row_idx, date_convention)
    cols_values_list = [f"{col} = {value}" for col, value in zip(cols_list, values_list)]
    cols_values_str = ''.join(map(str, cols_values_list))[:-1]
    return cols_values_str


def __get_update_script_row(input_table, cols_values_str, df, row_idx):
    key = TABLE_KEY_RELATIONSHIP[input_table]
    # PK
    if len(key) == 1:
        row = f"""UPDATE {input_table} SET {cols_values_str}\nWHERE {key[0]} = '{df.loc[row_idx, key[0]]}';\n"""
    # CK
    elif len(key) == 2:
        row = f"""UPDATE {input_table} SET {cols_values_str}\nWHERE {key[0]} = '{df.loc[row_idx, key[0]]}' AND {key[1]} = '{df.loc[row_idx, key[1]]}';\n"""
    elif len(key) == 3:
        row = f"""UPDATE {input_table} SET {cols_values_str}\nWHERE {key[0]} = '{df.loc[row_idx, key[0]]}' AND {key[1]} = '{df.loc[row_idx, key[1]]}' AND {key[2]} = '{df.loc[row_idx, key[2]]}';\n"""
    return row


def __get_delete_script_row(input_table, df, row_idx):
    key = TABLE_KEY_RELATIONSHIP[input_table]
    # PK
    if len(key) == 1:
        row = f"""DELETE FROM {input_table} WHERE {key[0]} = '{df.loc[row_idx, key[0]]}';\n"""
    # CK
    elif len(key) == 2:
        row = f"""DELETE FROM {input_table} WHERE {key[0]} = '{df.loc[row_idx, key[0]]}' AND {key[1]} = '{df.loc[row_idx, key[1]]}';\n"""
    elif len(key) == 3:
        row = f"""DELETE FROM {input_table} WHERE {key[0]} = '{df.loc[row_idx, key[0]]}' AND {key[1]} = '{df.loc[row_idx, key[1]]}' AND {key[2]} = '{df.loc[row_idx, key[2]]}';\n"""
    return row
