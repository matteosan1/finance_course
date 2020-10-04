import json, csv

with open("testing_techana_frames.json", "r") as f:
    labels = json.load(f)

#print (labels)
with open("testing_techana_frames.csv", mode='w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for l in labels:
        writer.writerow(l)
