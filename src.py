import ntpath


def __get_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def __get_cols_str(table):
    cols_list = [f'[{col}],' for col in table.columns]
    cols_str = ''.join(map(str, cols_list))[:-1]
    return cols_str


def __get_date_cols_index(table):
    date_cols = ['analysis_date', 'date_shipped', 'sampling_date', 'date_plan',
                 'date_shipped', 'date_imported', 'date_received']
    date_cols_idxs = [i for i, col in enumerate(list(table.columns)) if col in date_cols][0]
    return date_cols_idxs

