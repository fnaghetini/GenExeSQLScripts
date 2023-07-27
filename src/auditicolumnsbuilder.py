from datetime import date


def __get_autiting_cols(df, date_convention):
    df['last_modified_by'] = 'Datamine'
    df['last_modified_date_time'] = date.today().strftime(date_convention)
    return df
