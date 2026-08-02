import pandas as pd

import csv

import glob

from bert_score import score
import torch

#first get the data i want to use

original_texts = pd.read_csv("./output/merged-fkgl-texts.csv")

original_texts.columns["texts"]

files = glob("./output/*_prompt_output.csv")

data = pd.DataFrame()

for file in files:
    frame = pd.read_csv(file, header=None)
    data = pd.concat([data, frame])

data.columns = ['model', 'grade', 'output']

#then match the translated text to the original and perform bert score algorithm

data["original_text"] = original_texts["texts"]

P, R, F1 = score(
    data["output"],
    data["original_text"],
    lang="en",
    batch_size=64,
)







