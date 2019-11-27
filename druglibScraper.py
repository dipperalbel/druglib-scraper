from bs4 import BeautifulSoup
import json
import requests
import re

errors_names = []

correct_list = []

correct_names = []

def scrape_druglib(url, product, target_path = './'):

    req = requests.get(url)
    
    if req.status_code != 200:
        print("Could not connect to " + url )
        print("Response : " + str(req.status_code))
        errors_names.append(product)
        return None
    
    bs = BeautifulSoup(req.text, 'html.parser')
    
    all_reviews = []
    source = []
    
    try :        
        source = bs.findAll("table", {"cellspacing" : 4, "border" : 0})

    except Exception as e:
        print(e)
        return None
    
    for i in range(len(source)):
        review = {}
        author = source[i].find("h2").getText()
        review["author"] = author
        test = source[i].findAll("td", {"class" :  "review3"})
        rating = len(test[0].findAll("img", {"src" : "/img/red_star.gif"}))
        review["rating"] = rating
        review["Effectiveness"] = test[1].getText()
        review["Side effects"] = test[2].getText()
        review["Condition"] = test[3].getText()
        review["Dosage and duration"] = test[4].getText()
        review["Other conditions"] = test[5].getText()
        review["Other drug taken"] = test[6].getText()
        review["Benefits"] = test[7].getText()
        review["Side effects"] = test[8].getText()
        review["Comments"] = test[9].getText()
        all_reviews.append(review)

    json_object = {"name" : product}
    json_object["numberReviews"] = len(bs.findAll("table", {"cellspacing" : 4, "border" : 0}))
    
    try :
        scores = re.findall("\d+[.,]\d+",str(bs.find("div", {"class":"info_box"}).getText()))
        json_object["overallScore"] = float(scores[0])
        json_object["effectivenessScore"] = float(scores[1])
        json_object["sideEffectScore"] = float(scores[2])
        json_object["reviews"] = all_reviews
        correct_names.append(product)
        return json_object

    except Exception as e:
        errors_names.append(product)
        print(e)
        return None


with open("prodottinomi.txt", "r") as filetxt :
    s = filetxt.readlines()

res = [sub[ : -1] for sub in s]
res = [sub.strip() for sub in res]
res = [sub.replace(" ", "-" ) for sub in res]
temp = set(res)
res = list(temp)

name = res

print(len(name))

for i in name:
    print(i)
    url = "http://www.druglib.com/ratingsreviews/"+i
    ret = scrape_druglib(url,i)
    if (ret is not None ) :
        correct_list.append(ret)
    

if len(errors_names) != 0 :
    print("Items that could not get scrapped: " + str(errors_names))

json_result = {"website" : "druglib.com"}
json_result["namesItemsReviewed"] = correct_names


json_result["aggregateReviews"] = correct_list

with open("druglibresult.json","w") as f:
    obj =  json.dumps(json_result, indent = 4)
    f.write(obj)


