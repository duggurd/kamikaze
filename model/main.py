from transformers import AutoModelForSequenceClassification, AutoTokenizer, RobertaForSequenceClassification
from fastapi import FastAPI

from pydantic import BaseModel
from typing import List


class Sentiment(BaseModel):
    text: str

class BatchSentiment(BaseModel):
    text: list[str]


app = FastAPI()


model_name = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

app = FastAPI()


@app.post("/sentiment")
def def_sentiment(sent: Sentiment):
    tokenized_text = tokenizer(sent.text, return_tensors="pt")
    output = model.forward(**tokenized_text)[0].detach().numpy().tolist()

    return {
        "sentiment": output
    }


@app.post("/sentiment/batch")
def def_sentiment(sent: BatchSentiment):
    tokenized_text = tokenizer(sent.text, return_tensors="pt", padding=True)
    output = model.forward(**tokenized_text)[0].detach().numpy().tolist()

    return {
        "sentiment": output
    }