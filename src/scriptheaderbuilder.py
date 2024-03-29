from datetime import datetime


def __build_script_header(name, script_type=""):
    now = datetime.now()
    header = f"""-- Author:            Datamine Software
-- Contact:           support.sa@dataminesoftware.com
-- Creation Datetime: {now.strftime("%d/%m/%Y %H:%M:%S")}
-- Script Type:       {script_type}
-- Script Name:       {name}\n\n\n"""
    return header
