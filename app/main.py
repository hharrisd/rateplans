import logging
from fastapi import FastAPI, UploadFile, File, Body
from app import file_manager

app = FastAPI()


@app.post("/prepare_rates")
async def prepare_rates(
        rate_plan_name: str = Body(..., description="Nombre de la tarifa resultante"),
        files: list[UploadFile] = File(..., description="Lista de archivos (.xlsx) a adjuntar")
):
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
