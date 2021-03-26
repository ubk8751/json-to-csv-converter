import json
import requests
import csv

def main():
    # Get the requests file using requests.
    request = requests.get("https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/13.199167/lat/55.708333/data.json")
    
    # If the adress works, convert the requests file into a json file.
    if request.status_code == 200:
        items = request.json()
        
        # Sort the dict and only take the information we need
        sorted_items = create_dict(items)

        # Export dict as json file
        export_to_json(sorted_items)

        # Export dict as csv file
        export_to_csv(sorted_items)



def export_to_csv(dct):
    cols = ["Date", "Time", "Temperature", "Coordinates"]
    try:
        with open("data.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cols)
            writer.writeheader()
            for data in dct:
                writer.writerow(dct[data])
        print("CSV created")
    except IOError:
        print("I/O error")

def export_to_json(items):
    try:
        with open("data.json", "w") as outfile: 
            json.dump(items, outfile)
        print("Json created")
    except IOError:
        print("I/O error")

def create_dict(items):
    lst = {}
    for series in items['timeSeries']:
        for item in series["parameters"]:
            if item["unit"] == "Cel":
                time = series["validTime"].split("T")
                hour = time[1].split(":")
                h = hour[0] + ":" + hour[1]
                d = time[0]
                val = item["values"][0]
                lst[series["validTime"]] = {"Date": d, "Time": h, "Temperature": val, "Coordinates": {"x": items["geometry"]["coordinates"][0][0], "y": items["geometry"]["coordinates"][0][1]}}
    return lst

if __name__ == "__main__":
    main()