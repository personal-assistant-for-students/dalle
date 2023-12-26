from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline


class Item(BaseModel):
    text: str


app = FastAPI()
classifier = pipeline("sentiment-analysis")


@app.post("/")
def predict(item: Item):
    """TODO"""
    return classifier(item.text)
