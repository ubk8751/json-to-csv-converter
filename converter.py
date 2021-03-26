import json
import requests

def main():
    # Get the requests file using requests.
    request = requests.get("https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/13.199167/lat/55.708333/data.json")
    
    # If the adress works, convert the requests file into a json file.
    if request.status_code == 200:
        items = request.json()
        print(items['timeSeries'][0]['parameters'][10])
        

def convert():
    pass

def create_dict(items):
    lst = {}
    for item in items['timeSeries']:
        for item2 in item["parameters"]:
            if item2["unit"] == "Cel":
                lst[item["validTime"]] = item2
    print(lst)

if __name__ == "__main__":
    main()