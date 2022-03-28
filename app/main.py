import logging
from fastapi import FastAPI, UploadFile, File, Body
from app import file_manager
from typing import List

app = FastAPI()


@app.post("/prepare_rates")
async def prepare_rates(
        rate_plan_name: str = Body(..., description="Nombre de la tarifa resultante"),
        files: List[UploadFile] = File(..., description="Lista de archivos (.xlsx) a adjuntar")
):
    # return {"filenames": [file.filename for file in files]}
    file_manager.validate_type(files)
    directory = file_manager.make_directory(rate_plan_name)
    for file in files:
        contents = await file.read()
        file_manager.save_file(directory, file.filename, contents)

    rateplan = file_manager.get_dataframes(directory)
    logging.info('Data lista para la respuesta')

    return {
        "rateplan_name": rate_plan_name,
        "rateplan": rateplan
    }
