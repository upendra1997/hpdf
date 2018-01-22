from src import app
from flask import Flask, render_template, request, session, redirect, url_for, flash, g, send_file, json
import requests


# app = Flask(__name__)
# app.config.from_object("config")


@app.route('/')
def main():
    return "Hello World - Upendra Upadhyay"

@app.route('/authors',methods=["GET","POST"])
def index():
    user_url = "https://jsonplaceholder.typicode.com/users"
    post_url = "https://jsonplaceholder.typicode.com/posts"
    users = requests.get(user_url).json()
    posts = requests.get(post_url).json()
    print(users)
    print(posts)
    res = {}
    for u in users:
        res[u["id"]] = {"name": u["name"]}
    for p in posts:
        if p["userId"] in res.keys():
            if("count" in res[p["userId"]].keys()):
                res[p["userId"]]["count"]+=1
            else:
                res[p["userId"]]["count"] = 1
    text = ""
    for a in res.values():
        text+="Author Name: "+a["name"]+"; Number of posts: "+str(a["count"])+";<br>"
    print(text)
    return text


@app.route('/setcookie')
def setCookie():
    session["name"] = "Upendra"
    session["age"] = 21
    return "Cookies set!!"


@app.route('/getcookie')
def getCookie():
    if "name" not in session.keys() or "age" not in session.keys():
        return "No Cookie set please set cookies by clicking <a href='/setcookie'>here</a>"
    return "Name: "+session["name"]+"<br> Age: "+str(session["age"])


@app.route('/robots.txt')
def deny():
    return ''':( <br>YOU SHOULDN'T BE HERE<br>''', 401


@app.route('/html')
def html():
    return render_template('index.html')


@app.route('/image')
def image():
    image_url = 'images/image.png'
    return send_file(image_url)


@app.route('/input',methods=["GET","POST"])
def input():
    if(request.method=="GET"):
        return render_template('index.html')
    print("INPUT: ",request.form["t"])
    return request.form["t"]

@app.route('/signup',methods=["GET","POST"])
def signup():
    if(request.method=='GET'):
        return render_template('signup.html')
    else:
        if request.form['password1']==request.form['password2']:
            # This is the url to which the query is made
            url = "https://auth.diagnostician94.hasura-app.io/v1/admin/create-user"

            # This is the json payload for the query
            requestPayload = {
                "provider": "username",
                "data": {
                    "username": request.form["username"],
                    "password": request.form["password1"]
                },
                "roles": [
                    "user"
                ],
                "is_active": True
            }
            print("username", request.form["username"],"password", request.form["password1"])
            # Setting headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer e665801b3a45b92a9d7581e334459dae6b1e72d20a21a28f"
            }

            # Make the query and store response in resp
            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

            # resp.content contains the json response.
            print(resp.content)
            j = json.loads(resp.content)
            if "message" in j.keys():
                flash(j["message"])
            else:
                flash("User successfully created.")
        else:
            flash("password did not match")
    return render_template('signup.html')

# from src import app
# @app.route('/create/<table_name>/')