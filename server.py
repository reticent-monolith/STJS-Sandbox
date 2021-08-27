from flask import Flask, request, render_template, make_response, jsonify, redirect, url_for
import jwt as pjwt
import os
import datetime
import time  
import json
from dotenv import load_dotenv
import pprint
import pickle

app = Flask(__name__)
load_dotenv()
SITE_REF = os.environ["SITE_REF"]
JWT_USER = os.environ["JWT_USER"]
SECRET = os.environ["SECRET"]
DOMAIN = os.environ["DOMAIN"]
VERSION = os.environ["VERSION"]

def get_refs(file):
    if os.path.exists(file):
        with open(file, 'rb') as refs:
            return pickle.load(refs)
    else:
        return []

def store_refs(refs, file):
    with open(file, 'wb') as file_obj:
        pickle.dump(refs, file_obj)

min_payload = {
    "accounttypedescription": "ECOM",
    "currencyiso3a": "GBP",
    "sitereference": SITE_REF,
    "requesttypedescriptions": ["THREEDQUERY"]
}

@app.route("/")
def index():
    return redirect(url_for("basic"))

# BASIC SETUP
@app.route("/basic")
def basic():
    transaction_refs = get_refs("./refs.pickle")
    jwt = {
        "payload": {**min_payload, **{
            "baseamount": 1050,
            "requesttypedescriptions": ["THREEDQUERY", "AUTH"]
        }},
        "iss": JWT_USER,
        "iat": time.mktime(datetime.datetime.now().timetuple())
    }
    has_saved_creds = "0"
    pan = ""
    type = ""
    print(f"In basic: {transaction_refs}")
    if len(transaction_refs) > 0:
        jwt["payload"]["credentialsonfile"] = 2
        jwt["payload"]["parenttransactionreference"] = transaction_refs[len(transaction_refs)-1]["transactionreference"]
        has_saved_creds = "1"
        pan = transaction_refs[len(transaction_refs)-1]["maskedpan"]
        type = transaction_refs[len(transaction_refs)-1]["paymenttypedescription"]

    my_jwt = pjwt.encode(jwt, SECRET, algorithm="HS256")
    return render_template("basic.jinja", jwt=my_jwt, decoded_jwt=jwt, domain=DOMAIN, version=VERSION, creds=has_saved_creds, pan=pan, type=type)

# SUBSCRIPTION
@app.route("/subscription")
def subscription():
    jwt = {
        "payload": {**min_payload, **{
            "requesttypedescriptions": ["THREEDQUERY", "AUTH", "SUBSCRIPTION"],
            "baseamount": 1050,
            "authmethod": "FINAL",
            "credentialsonfile": 1,
            "subscriptionfinalnumber": "0", 
            "subscriptionfrequency": "1", 
            "subscriptiontype": "RECURRING", 
            "subscriptionunit": "MONTH",
            "subscriptionnumber": 1
        }},
        "iss": JWT_USER,
        "iat": time.mktime(datetime.datetime.now().timetuple()),
    }
    my_jwt = pjwt.encode(jwt, SECRET, algorithm="HS256")
    return render_template("subscription.jinja", jwt=my_jwt, decoded_jwt=jwt, domain=DOMAIN, version=VERSION)

# TOKENISE
@app.route("/tokenise")
def tokenise():
    jwt = {
        "payload": {**min_payload, **{
            "baseamount": 1050,
            "requesttypedescriptions": ["ACCOUNTCHECK"],
            "credentialsonfile": 1
        }},
        "iss": JWT_USER,
        "iat": time.mktime(datetime.datetime.now().timetuple()),
    }
    my_jwt = pjwt.encode(jwt, SECRET, algorithm="HS256")
    return render_template("tokenise.jinja", jwt=my_jwt, decoded_jwt=jwt, domain=DOMAIN, version=VERSION)

@app.route("/end?from=<page>", methods=["POST"])
def end(page):
    return render_template("end.jinja", page=page, data=dict(request.form))

@app.route("/submit", methods=["POST"])
def submit():
    post_data = request.get_json()
    try:
        obj_jwt = pjwt.decode(post_data['jwt'], SECRET, algorithms=["HS256"], audience=JWT_USER)
        print(obj_jwt)
        return make_response(jsonify({"jwt": obj_jwt}), 200)
    except KeyError as ke:
        print(f"Key {ke} not found in response JWT!")
    except Exception as e:
        print(f"Something awful happened: {e}")
    finally: 
        return make_response({"response": "obj received"}, 200)

@app.route("/success", methods=["POST"])
def success():
    print(request.get_json())
    return make_response({"response": "obj received"}, 200)

@app.route("/error", methods=["POST"])
def error():
    print(request.get_json())
    return make_response({"response": "obj received"}, 200)
    
@app.route("/save_transactionreference", methods=["POST"])
def save():
    req = request.get_json()
    transaction_refs = get_refs("./refs.pickle")
    transaction_refs.append({
        "transactionreference": req["transactionreference"],
        "maskedpan": req["maskedpan"],
        "paymenttypedescription": req["paymenttypedescription"]
    })
    store_refs(transaction_refs, "./refs.pickle")
    return make_response("Saved", 200)

@app.route("/updatejwt", methods=["POST"])
def update_jwt():
    req = request.get_json()
    jwt = pjwt.decode(req["jwt"], SECRET, algorithms=["HS256"])
    amount = req["new_amount"]
    jwt["payload"]["baseamount"] = float(amount)*100
    return make_response(jsonify({"jwt": pjwt.encode(jwt, SECRET, algorithm="HS256")}), 200)

# DRIVER CODE
if __name__=="__main__":
    app.run(host="localhost", port=3000, load_dotenv=True)