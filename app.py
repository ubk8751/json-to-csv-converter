from flask import Flask, jsonify, render_template, request, redirect, url_for
from converter import if_file, if_requests, create_dict, export_to_csv, export_to_json

#Obligatory Flask code
app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    options = ["file","link"]
    if request.method == "POST":
        if request.form["route"] == "file":
            return redirect(url_for("file_route"))
        
        elif request.form["route"] == "link":
            return redirect(url_for("link_route"))
        else:
            return render_template("index.html", options=options)
    else:
        return render_template("index.html", options=options)

@app.route("/file", methods = ["POST", "GET"])
def file_route(): 
    return render_template("file.html")

@app.route("/link", methods = ["POST", "GET"])
def link_route():
    sorted_items = {}
    status = ""
    weather_url = request.args.get("weather_url", "")

    if weather_url:
        items = if_requests(weather_url)
        sorted_items = create_dict(items)
        if request.form["choise"] == "csv":
            export_to_csv(sorted_items)
            status = "CSV created!"
        elif request.form["choise"] == "json":
            export_to_json(sorted_items)
            status = "Json Created!"
        else:
            status = "Please choose a file option!"
        

    return render_template("link.html", weather_url = weather_url, status = status)

if __name__ == "__main__":
    app.run(debug=True,port=50)