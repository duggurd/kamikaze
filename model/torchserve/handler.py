from ts.torch_handler.base_handler import BaseHandler

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json

MODEL_NAME = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
MODEL_FOLDER = "distilroberta_raw"
class RobertaForSequenceClassificationHandler(BaseHandler):

    def __init__(self):
        self.initialized = False

    def initialize(self, context):
        self._context = context

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

        self.initialized = True

    def preprocess(self, data):
        raw_request_text = []

        for request in data:
            raw_request_text.extend(request.get("body").get("data"))


        model_input = self.tokenizer(raw_request_text, return_tensors="pt", padding=True)
        return model_input
    
    def inference(self, model_input):
        model_output = self.model.forward(**model_input)
        return model_output

    def postprocess(self, model_output):
        postprocessed = model_output[0].detach().numpy().tolist()

        return postprocessed