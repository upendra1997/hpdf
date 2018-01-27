from src import app
from flask import render_template, request, session, flash, send_file, json
import requests
from urllib import parse
# import os

# app = Flask(__name__)
# app.config.from_object("config")
# CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
url = "https://data.diagnostician94.hasura-app.io/v1/query"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer e665801b3a45b92a9d7581e334459dae6b1e72d20a21a28f"
}


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
            url = "https://auth.diagnostician94.hasura-app.io/v1/admin/create-user"
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

            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
            j = json.loads(resp.content)
            if "message" in j.keys():
                flash(j["message"])
            else:
                flash("User successfully created.")
        else:
            flash("password did not match")
    return render_template('signup.html')


@app.route('/chatbot',methods=["POST"])
def chatbot():
    DATA = request.get_data()
    obj = parse.parse_qs(parse.unquote(DATA.decode()))
    text = obj["text"][0]
    user_name = obj["user_name"][0]
    array = text.split(' ')
    if text.lower() == "num users":
        requestPayload = {
            "type": "count",
            "args": {
                "table": {
                    "name": "users",
                    "schema": "hauth_catalog"
                }
            }
        }
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        return "Number of users registered on Hasura Auth is "+str(resp.json()['count'])

    elif len(array) == 3:
        num = 0
        try:
            num = int(array[2])
        except ValueError:
            return "Please enter a number for number_of_rows."
        requestPayload = {
            "type": "select",
            "args": {
                "table": array[0],
                "columns": [
                    "*"
                ],
                "order_by": [
                    {
                        "column": array[1],
                        "order": "asc"
                    }
                ]
            }
        }
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if "error" in resp.json():
            return "Error: "+resp.json()["error"]
        else:
            cont = resp.json()[:num]
            return str(cont)
    return "Not a valid Command."



# 'token=maQnmrdrkTvbzv3Mh89IVXBl&team_id=T859NJ23D&team_domain=hdggxin&channel_id=G8XRCGJET&channel_name=privategroup&user_id=U85G1DGH3&user_name=hdggxin&command=/chatbot&text=hello&response_url=https://hooks.slack.com/commands/T859NJ23D/302774465728/ZHp4sgq2xkPGapvwFaPVwP8y&trigger_id=303325218739.277328614115.519471ee910f043d65d7c82d2a985583'
# token=gIkuvaNzQIHg97ATvDxqgjtO
# team_id=T0001
# team_domain=example
# channel_id=C2147483705
# channel_name=test
# user_id=U2147483697
# user_name=Steve
# command=/weather
# text=94070
# response_url=https://hooks.slack.com/commands/1234/5678
# from src import app
# @app.route('/create/<table_name>/')