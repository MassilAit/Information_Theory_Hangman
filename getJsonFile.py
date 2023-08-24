import pandas as pd
import json


def write_json_file(filename: str, separator ='\t')-> None :

    df =pd.read_csv(filename,sep=separator, header=None)
    dic={}
    for i in df[0]:
        n=len(str(i))
        if(n not in dic):
            dic[n]=[]
        dic[n].append(str(i))

    with open("data/words.json", "w") as outfile:
        json.dump(dic, outfile)


write_json_file('data/30k.txt')