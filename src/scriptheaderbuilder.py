from datetime import date

today = date.today()


def __get_current_date():
    return today.strftime("%d/%m/%Y")


def __build_script_header(name):
    header = f"""/****** Autor:           Datamine Software                                     ******/
/****** Contato:         support.sa@dataminesoftware.com                       ******/
/****** Data de Criação: {__get_current_date()}                                            ******/
/****** Script:          {name}            ******/\n\n\n"""

    return header

