from importlib import import_module
from flask import Flask, redirect, render_template, request
from SIA_helper import find_stop_near, map_maker,open_guy

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def mbta_close():
    if request.method== "POST":
        if request.form["button1"]=="1":
            global location
            location=request.form["location"]
            try:
                stop,wheelchair, lat, long= find_stop_near(location)
                map_url = map_maker(lat,long,600,450,14)
            except TypeError:
                stop,wheelchair, map_url = "too far", "just walk",''
            return render_template("mbta-result.html", stop=stop, wheelchair=wheelchair,map_url=map_url)
        
    return render_template("mbta-form.html")


# @app.route("/", methods=["POST", "GET"])
# def index():
#     if request.method == "POST":
#         result = request.form["location"]
#         return redirect("mbta_result.html",stop=stop, wheelchair=wheelchair,map_url=map_url)
#     return render_template("mbta-form.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.form["button2"]=="2":
            location2=request.form["location2"]
            print(location)
            try:
                ourlist=open_guy(location,location2)
                stop2,wheelchair2, lat2, long2= find_stop_near(location2)
                map_url2 = map_maker(lat2,long2,600,450,14)
            except TypeError:
                stop2,wheelchair2, map_url2 = "too far", "just walk",''
            return render_template("mbta-result2.html", stop2=stop2, wheelchair2=wheelchair2,map_url2=map_url2,ourlist=ourlist)



if __name__ == "__main__":
    app.run(debug=True)