from bert_score import score
import torch

import pandas as pd

import csv

import glob

#first get the data i want to use

original_texts = pd.read_csv("./output/merged-fkgl-texts.csv")

files = glob("./output/*_prompt_output.csv")

data = pd.DataFrame()

for file in files:
    frame = pd.read_csv(file, header=None)
    data = pd.concat([data, frame])







