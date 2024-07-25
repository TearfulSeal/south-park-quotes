
from flask import Flask, render_template, request, redirect
import requests
import json
from random import choice
app = Flask(__name__)


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
def makeRequest(name):
    url = "https://southparkquotes.onrender.com/v1/quotes"
    if name != "":
        url+=f"/search/{name}"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
def imageName(char):
    name = ""
    for i in char:
        if i.isalpha():
            name += i
    return name.lower() + ".png"
     

@app.route('/', methods=["GET","POST"])
def hello():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        name = request.form.get("name").lower()
        data = makeRequest(name)
     
        try:
            data = choice(data)
            return render_template("quote.html", quote= data["quote"], char= data["character"], img = imageName(data["character"]))
        except:
            
            return redirect("/")
        


@app.route('/random')
def random():
    data = makeRequest("")[0]
    try:
        return render_template("quote.html", quote = data["quote"], char= data["character"], img = imageName(data["character"]))
    except:
       
        return redirect("/")




if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
