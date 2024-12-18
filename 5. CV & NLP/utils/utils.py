from utils.ocr import *
from flask import jsonify
from utils.summarize import *
from langchain import HuggingFaceHub
from dotenv import load_dotenv
import os

load_dotenv('.env')

# initialize Hub LLM
llm_t5 = HuggingFaceHub(
    repo_id='google/flan-t5-large',
    model_kwargs={'temperature':0,"max_length": 64,"max_new_tokens":128}
)

llm_xl_sum = HuggingFaceHub(
    repo_id='csebuetnlp/mT5_multilingual_XLSum',
    model_kwargs={'temperature':0.5,"max_length": 64,"max_new_tokens":512}
)

os.environ['CURL_CA_BUNDLE'] = ''



def get_text_from_ocr(image_bytes, ocr_engine):
    if ocr_engine == 'paddleocr':
        return(paddle_ocr(image_bytes))
    elif ocr_engine == 'tesseract':
        return(tesseract_ocr(image_bytes))
    else:
        return jsonify({"error": "Invalid OCR engine selected"}), 400
    

def get_abstractive_summary(paragraph,abstractive_summarization_model):

    if abstractive_summarization_model == 't5':
        return(abstractive_summarize(paragraph, llm_t5))
        
    elif abstractive_summarization_model == 'xl_sum':
        return(abstractive_summarize(paragraph, llm_xl_sum))
    else:
        return jsonify({"error": "Invalid OCR engine selected"}), 400
    