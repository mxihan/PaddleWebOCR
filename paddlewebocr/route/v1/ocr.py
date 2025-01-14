import json
import time
import orjson
import logging
from typing import Any
from fastapi import APIRouter, File, UploadFile, Form, status
from fastapi.responses import ORJSONResponse, JSONResponse
from paddlewebocr.pkg.util import *
from paddlewebocr.pkg.ocr import text_ocr
from paddlewebocr.pkg.postprocessing import *


class MyORJSONResponse(ORJSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY)


router = APIRouter()


@router.post('/ocr')
async def ocr(img_upload: UploadFile = File(None),
              img_b64: str = Form(None),
              compress_size: int = Form(None),
              ocr_model: str = Form(None),
              ocr_post_process: str = Form(None)):
    start_time = time.time()

    if img_upload is not None:
        img = convert_bytes_to_image(img_upload.file.read())
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})

    img = rotate_image(img)
    img = img.convert("RGB")
    img = compress_image(img, compress_size)

    texts = text_ocr(img, ocr_model)
    img_drawed = draw_box_on_image(img.copy(), texts)
    img_drawed_b64 = convert_image_to_b64(img_drawed)

    result_json = "{}"
    result = list(map(lambda x: x[1][0], texts))
    if ocr_post_process == 'id_card_front':
        postprocessing = IdCardFront(result)
        result_json = postprocessing.run()
    elif ocr_post_process == 'id_card_back':
        postprocessing = IdCardBack(result)
        result_json = postprocessing.run()
    elif ocr_post_process == 'business_license':
        postprocessing = BusinessLicense(result)
        result_json = postprocessing.run()
    result = json.loads(result_json)

    data = {'code': 0, 'msg': '成功',
            'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                     'raw_out': list(map(lambda x: [x[0], x[1][0], x[1][1]], texts)),
                     'speed_time': round(time.time() - start_time, 2),
                     'result': result}}
    return MyORJSONResponse(content=data)
