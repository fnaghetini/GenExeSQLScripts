import ntpath
import pandas as pd


def __get_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def __get_insert_cols_str(table):
    cols_list = [f'[{col}],' for col in table.columns]
    cols_str = ''.join(map(str, cols_list))[:-1]
    return cols_str


def __get_date_cols_index(table):
    date_cols = ['analysis_date', 'date_shipped', 'sampling_date', 'date_plan',
                 'date_shipped', 'date_imported', 'date_received']
    date_cols_idxs = [i for i, col in enumerate(list(table.columns)) if col in date_cols][0]
    return date_cols_idxs


def __get_insert_values_str(table, row_idx):
    date_cols_idxs = __get_date_cols_index(table)
    values_list = []

    for col_idx, value in enumerate(table.iloc[row_idx, :]):
        if pd.isna(value):
            values_list.append("NULL,")
        else:
            if col_idx in date_cols_idxs:
                values_list.append(f"CONVERT(DATETIME,'{value}',102),")
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
    row = f"""UPDATE {input_table} SET {cols_values_str}
              WHERE sample_number = '{table.loc[row_idx, 'sample_number']}';\n"""
    return row

