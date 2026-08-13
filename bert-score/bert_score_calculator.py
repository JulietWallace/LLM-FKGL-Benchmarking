import pandas as pd

import csv

import glob

from bert_score import score
import torch

#first get the data i want to use

original_texts = pd.read_csv('texts_concat.csv', header=None)

original_texts.columns = ['grade', 'text_num', 'text']

outputs = pd.read_csv('prompt_files_concat.csv')

outputs.columns = ['model', 'grade', 'text_num', 'target_grade', 'prompt_index', 'output']

#then match the translated text to the original and perform bert score algorithm

outputs = outputs.merge(
    original_texts[['grade', 'text_num', 'text']],
    on=['grade', 'text_num'],
    how='left'
)
outputs.to_csv("out.csv", index=False)


P, R, F1 = score(
    outputs['output'].astype(str).tolist(),
    outputs['text'].astype(str).tolist(),
    lang="en",
    batch_size=64,
)

outputs["bert_precision"] = P
outputs["bert_recall"] = R
outputs["bert_f1"] = F1

out = outputs.to_csv("bert_scores_output.csv")




