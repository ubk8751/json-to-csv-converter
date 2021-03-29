'''
By:     Samuel Jonsson
        Blekinge Tekniska Högskola
Date:   2021-03-28
Email:  ubk8751@gmail.com
'''

# Import all the goodies
from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import requests
import csv

# Necessary Flask code
app = Flask(__name__)

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
def export_to_csv(dct):
    # The columns that should be in the CSV file
    cols = ["Date", "Time", "Temperature", "Coordinates"]
    try:
        # Create the CSV file named data.csv using the defined columns and the data in the dictionary
        with open("data.csv", 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=cols)
            writer.writeheader()
            for data in dct:
                writer.writerow(dct[data])
        
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

def get_json_from_link(link):
    # Get the last word
    temp = link.split("/")

    e = temp[-1]
    s = temp[2]

    # Check if the link ends with data.json
    if e == "data.json" and s == "opendata-download-metfcst.smhi.se":
        # Get the requests file using requests.
        request = requests.get(link)
        
        # If the adress works, convert the requests file into a json file.
        if request.status_code == 200:
            items = request.json()

            # Return our json file
            return items
    else:
        print("Check your address please!")

def get_json_from_file(path):
    try:
        ext = path.split(".")

        if ext[-1] == "json":
            data = json.load(path)
            return data
        else:
            print("Wrong file type!")
    
    except IOError:
        print("I/O Error!")

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

# Route for getting a json file using a link, sort it and export as Json or CSV
@app.route("/link", methods=["POST","GET"])
def if_link():
    weather_link = ""
    
    if request.method == "POST":
        # Get the link from the app
        weather_link = request.args.get("weather_link", "")
        
        if weather_link:
            items = get_json_from_link(weather_link)

            sorted_items = create_dict(items)

            if request.method == "POST":
                if request.form["option"] == "CSV":
                    export_to_csv(sorted_items)
                    return render_template("link.html", weather_link = weather_link, items = sorted_items)
                elif request.form["option"] == "Json":
                    export_to_json(sorted_items)
                    return render_template("link.html", weather_link = weather_link, items = sorted_items)
                else:
                    return render_template("link.html", weather_link = weather_link, items = sorted_items)
            else:
                    return render_template("link.html", weather_link = weather_link, items = sorted_items)
    
    return render_template("link.html")

# Route for reading a json file, sort it and export as Json or CSV
@app.route("/file", methods=["POST","GET"])
def if_file():
    '''path = ""
    items = get_json_from_file(path)
    sorted_items = create_dict(items)
    file_name = "smhi_data.json"'''
    return render_template("file.html") #, items = sorted_items, file_name = file_name

if __name__ == "__main__":
    app.run(debug=True,port=5000)