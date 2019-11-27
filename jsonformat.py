import json

obj = {}

s = []

with open("prodottiformatted.json", "r") as f:
    with open("prodottinomi.txt", "w") as filetxt :
        obj = json.load(f)
        for k in obj.keys() :
            filetxt.write(obj[k]["name"])
            filetxt.write("\n")

    
with open("prodottinomi.txt", "r") as filetxt :
    s = filetxt.readlines()

res = [sub[ : -1] for sub in s]
res = [sub.strip() for sub in res]
res = [sub.replace(" ", "-" ) for sub in res]
temp = set(res)
res = list(temp)
print(res)
