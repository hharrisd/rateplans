import json
import logging
from fastapi import FastAPI, UploadFile, File, Body
from starlette.responses import FileResponse

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

    df = file_manager.get_dataframes(directory)

    rateplan_json = df.to_json(orient="records")

    return {
        "rateplan_name": rate_plan_name,
        "rateplan": json.loads(rateplan_json)
    }


@app.post("/prepare_rates/download")
async def prepare_rates_download(
        rate_plan_name: str = Body(..., description="Nombre de la tarifa resultante"),
        files: List[UploadFile] = File(..., description="Lista de archivos (.xlsx) a adjuntar")
):
    file_manager.validate_type(files)
    directory = file_manager.make_directory(rate_plan_name)
    for file in files:
        contents = await file.read()
        file_manager.save_file(directory, file.filename, contents)

    df = file_manager.get_dataframes(directory)

    df.to_excel(f"{directory}/{rate_plan_name}.xlsx", index=False, header=True)

    return FileResponse(f"{directory}/{rate_plan_name}.xlsx", media_type='application/octet-stream',
                        filename=f"{rate_plan_name}.xlsx")
