import csv

with open(".\\indsol_web\\authapp\data\\region.csv", "r", newline="") as file:
    spamreader = csv.reader(file, delimiter=" ", quotechar=",")
    for row in spamreader:
        print(", ".join(row))
