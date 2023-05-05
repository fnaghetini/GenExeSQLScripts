from datetime import date


def __build_script_header(name):
    today = date.today()
    header = f"""/****** Autor:           Datamine Software                                     ******/
/****** Contato:         support.sa@dataminesoftware.com                       ******/
/****** Data de Criação: {today.strftime("%d/%m/%Y")}                                            ******/
/****** Script:          {name}            ******/\n\n\n"""

    return header

