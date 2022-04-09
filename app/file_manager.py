import glob
import json
import logging
import os
from datetime import date

import pandas as pd
from fastapi import HTTPException

logging.basicConfig(filename='carga_tarifa.log', level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')


def validate_type(files: list):
    """"Check if file type is excel. Raise an exception if not"""
    errors = []
    if files:
        for file in files:
            if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                errors.append(f"El archivo {file.filename} tiene un tipo de documento inválido")
    else:
        errors.append(f"Almenos un archivo es requerido")

    if len(errors) > 0:
        raise HTTPException(400, detail={"Error de validación en archivos": errors})

    return True


def make_directory(directory_name: str) -> str:
    """"Creates a directory to store the files"""
    directory = os.path.join('rateplans', f"{directory_name}_{date.today()}")
    os.makedirs(directory, 493, exist_ok=True)
    return directory


def save_file(directory: str, filename: str, content):
    file_path = f"{directory}/{filename}"
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail={"Error creating file": filename})


def get_dataframes(rateplan_pahts: str):
    excel_files = glob.glob(os.path.join(rateplan_pahts, "*.xlsx"))
    dataframes = []

    for excel in excel_files:
        df = pd.read_excel(excel)
        dataframes.append(df)
        logging.info(f'Creado dataframe para: {excel}')

    df_concat = pd.concat(dataframes, ignore_index=True)
    logging.info(f'Dataframes concatenados')
    df_concat.drop_duplicates(inplace=True, subset=['Codigo'], keep='last')
    logging.info(f'Duplicados eliminados')

    return df_concat
