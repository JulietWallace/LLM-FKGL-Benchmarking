import pandas as pd
import csv

grades = [0, 2, 4, 6, 8, 10, 12]

for grade in grades:
    file = pd.read_csv("../fkgl-texts/{grade}.csv".format(grade = grade))
    print(file.to_string())
    top_3 = file.head(4) #get first 4 texts
    print(top_3.to_string())
    texts = top_3.iloc[:, :2]
    texts.to_csv("../fkgl-texts/short/{grade}.csv".format(grade = grade))#skip first one
    print(texts.to_string())
    