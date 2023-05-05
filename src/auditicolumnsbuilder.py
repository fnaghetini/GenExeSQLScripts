from datetime import date


def __get_autiting_cols(df):
    df['last_modified_by'] = 'Datamine'
    df['last_modified_date_time'] = date.today().strftime("%d/%m/%Y")
    return df
