import pandas as pd
import csv
import time
import glob

grades = [0, 2, 4, 6, 8, 10, 12]

file = open("texts_concat.csv", "a")
writer = csv.writer(file)


for grade in grades:
    lines = pd.read_csv("fkgl-texts/{grade}.csv".format(grade = grade)) #open the csv with the texts for that level
    top_3 = lines.head(3) #get first 3 texts
    texts = top_3.iloc[:, 0].to_list() #transform to list
    texts_fkgl = top_3.iloc[:, 1].to_list() #transform to list
    for index, text in enumerate(texts):
        writer.writerow([grade, index, text])


data_files = glob.glob("output/timed/*_out.csv")


df = pd.concat((pd.read_csv(f, header = None) for f in data_files), ignore_index=True)

df.to_csv("data_files_concat.csv", index=False)

prompt_output_files = glob.glob("output/timed/*_prompt_output.csv")

df_prompts = pd.concat((pd.read_csv(f, header = None) for f in prompt_output_files), ignore_index=True)

df_prompts.to_csv("prompt_files_concat.csv", index=False)

