import json
import requests
import csv

file_exist = False

def main():
        
        if file_exist:
            items = if_file()
        else:
            items = if_requests()
        
        # Sort the dict and only take the information we need
        sorted_items = create_dict(items)

        # Export dict as json file
        export_to_json(sorted_items)

        # Export dict as csv file
        export_to_csv(sorted_items)

        print("Done")

def if_requests(path="https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/13.199167/lat/55.708333/data.json"):
    # Get the requests file using requests.
    request = requests.get(path)
    
    # If the adress works, convert the requests file into a json file.
    if request.status_code == 200:
        items = request.json()

        # Return our json file
        return items

# Get the Json file to read
def if_file(path="smhi_data.json"):
    # Define the path to the file
    path = "smhi_data.json"
    
    # Get the file
    try:
        f = open(path)
        dct = json.load(f)
        f.close()
    
        # Return the Json file
        return dct
    
    except:
        print("There was an error in loading the file!")

# Get the relevant items and data and return as a dictionary
def create_dict(items):
    lst = {}
    # Look through all items
    for series in items['timeSeries']:
        for item in series["parameters"]:
            # If the item is a temperature item, create a new dictionary sorted under date the date, 
            # with Date, time, temperature and coordinates as keys
            if item["unit"] == "Cel":
                time = series["validTime"].split("T")
                hour = time[1].split(":")
                h = hour[0] + ":" + hour[1]
                d = time[0]
                val = item["values"][0]
                lst[series["validTime"]] = {"Date": d, "Time": h, "Temperature": val, "Coordinates": {"x": items["geometry"]["coordinates"][0][0], "y": items["geometry"]["coordinates"][0][1]}}
    
    # Return the new dictionary
    return lst

# Create and export the CSV file
def export_to_csv(items):
    # The columns that should be in the CSV file
    cols = ["Date", "Time", "Temperature", "Coordinates"]
    try:
        # Create the CSV file named data.csv using the defined columns and the data in the dictionary
        with open("data.csv", 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=cols)
            writer.writeheader()
            for data in items:
                writer.writerow(items[data])
        
        # Confirm creation
        print("CSV created")
    
    # If there is an error in the creation of the file
    except IOError:
        print("I/O error")

# Create and export the Json file
def export_to_json(items):
    try:
    # Dump the dictionary as a Json file named data.json
        with open("data.json", "w") as outfile: 
            json.dump(items, outfile)
        print("Json created")
    
    # If there is an error in the creation of the file
    except IOError:
        print("I/O error")

if __name__ == "__main__":
    main()