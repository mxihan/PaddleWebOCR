import os
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np


OCR = {
    "ch_PP-OCRv4_xx": PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_PP-OCRv4_det_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_slim_infer",
                                         rec_model_dir="./inference/ch_PP-OCRv4_rec_infer",
                                         det_max_side_len="1920",
                                         use_angle_cls=True,
                                         max_text_length=100,
                                         drop_score=0.3,
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_PP-OCRv4_xx_server": PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_PP-OCRv4_det_server_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_slim_infer",
                                         rec_model_dir="./inference/ch_PP-OCRv4_rec_server_infer",
                                         det_max_side_len="1920",
                                         use_angle_cls=True,
                                         max_text_length=100,
                                         drop_score=0.3,
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_PP-OCRv3_xx_slim": PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_PP-OCRv3_det_slim_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_slim_infer",
                                         rec_model_dir="./inference/ch_PP-OCRv3_rec_slim_infer",
                                         det_max_side_len="1920",
                                         use_angle_cls=True,
                                         max_text_length=100,
                                         drop_score=0.3,
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_PP-OCRv3_xx": PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_PP-OCRv3_det_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_infer",
                                         rec_model_dir="./inference/ch_PP-OCRv3_rec_infer",
                                         det_max_side_len="1920",
                                         use_angle_cls=True,
                                         max_text_length=100,
                                         drop_score=0.3,
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_PP_OCRv2_xx_slim":  PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_PP-OCRv2_det_slim_quant_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_slim_infer",
                                         rec_model_dir="./inference/ch_PP-OCRv2_rec_slim_quant_infer",
                                         det_max_side_len="1920",
                                         use_angle_cls=True,
                                         max_text_length=100,
                                         drop_score=0.3,
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_PP_OCRv2_xx":  PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_PP-OCRv2_det_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_infer",
                                         rec_model_dir="./inference/ch_PP-OCRv2_rec_infer",
                                         det_max_side_len="1920",
                                         use_angle_cls=True,
                                         max_text_length=100,
                                         drop_score=0.3,
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False)
}


def text_ocr(img: Image, ocr_model: str) -> list:
    ocr = OCR.get(ocr_model, OCR["ch_PP-OCRv3_xx_slim"])
    result = ocr.ocr(np.array(img), cls=False)
    return result[0]
