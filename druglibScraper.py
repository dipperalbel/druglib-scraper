from bs4 import BeautifulSoup
import json
import requests
import re

errors_names = []

correct_list = []

def scrape_druglib(url, product, target_path = './'):

    req = requests.get(url)
    
    if req.status_code != 200:
        print("Could not connect to " + url )
        print("Response : " + str(req.status_code))
        errors_names.append(product)
        name.remove(product)
        return
    
    bs = BeautifulSoup(req.text, 'html.parser')
    
    all_reviews = []
    source = bs.findAll("table", {"cellspacing" : 4, "border" : 0})
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
    scores = re.findall("\d+[.,]\d+",str(bs.find("div", {"class":"info_box"}).getText()))
    json_object["Overall score"] = float(scores[0])
    json_object["Effectiveness score"] = float(scores[1])
    json_object["Side effect score"] = float(scores[2])
    json_object["reviews"] = all_reviews
    return json_object

name = ["accutane"]

set_name =  set(name)
name =  set_name
name = list(name)

for i in range(len(name)):
    refined_name = name[i].lower()
    refined_name = refined_name.strip()
    refined_name.replace(" ", "-")
    url = "http://www.druglib.com/ratingsreviews/"+refined_name
    correct_list.append(scrape_druglib(url,name[i]))

if len(errors_names) != 0 :
    print("Items that could not get scrapped: " + str(errors_names))

json_result = {"namesItemsReviewed" : name}
json_result["aggregateReviews"] = correct_list

with open("result.json","w") as f:
    obj =  json.dumps(json_result, indent = 4)
    f.write(obj)


