import requests
import random
import time

url = "http://z.cskaoyan.com/admin/employment/list/{}"
fields = ['id', 'name', 'languageType', 'salary', 'salaryDetail', 'cityId', 'city', 'className', 'academy', 'major', 'graduationTime', 'isDelete', 'createTime', 'updateTime', 'language', 'type']
employment_json = []

# scrape data
id = 1  # start id to be scraped
missed = 0
while True:
    r = requests.get(url.format(id))
    if  r.status_code == 200:
        if r.json()["data"]:
            print("Successfully Parsed. ID = {}\n".format(id))
            employment_json.append(r.json())
        else:
            print("Miss data. ID = {}\n".format(id))
            missed += 1
    else:
        print("Came to the end.\n")
        print("{} items were missed.\n".format(missed))
        break
    id += 1
    time.sleep(random.random() * 2)

# import json
# # save data to employment.json
# with open("employment.json",'w') as f:
#     json.dump(employment_json, f)

# # load data from employment.json
# with open("employment.json") as f:
#     employment_json = json.load(f)

delimiter = "^" # should not be comma due to the content include ","
with open("employment.csv", "w", encoding="utf-8") as f:
    head = delimiter.join(fields) + "\n"
    f.write(head)
    for item in employment_json:
        for field in fields:
            value = str(item["data"][field]).replace("\n", "")
            f.write(value + delimiter)
        f.write("\n")
