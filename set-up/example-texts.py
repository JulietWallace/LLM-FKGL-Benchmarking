import pandas as pd
import csv

examples = open("examples.csv", "a")
writer = csv.writer(examples)

for grade in range(0, 13):
    lines = pd.read_csv("../fkgl-texts/{grade}.csv".format(grade = grade)) #open the csv with the texts for that level
    example = lines.iloc[5, 0]
    writer.writerow([example])