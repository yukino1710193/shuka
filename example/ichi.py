from flask import Flask, Response
import os, requests

app = Flask(__name__)

TARGET = os.environ.get('TARGET', 'ichi')
PORT = os.environ.get('PORT', 8001)
NEXT = os.environ.get('NEXT', "")
NEXT = "127.0.0.1:8002"



@app.route("/")
def index():
    response = Response(f"{TARGET}\n")
    response.headers["app"] = "kusari"
    return response



@app.route("/hometag/<tag>")
def home_tag(tag):
    response = Response(f"{TARGET}\n")
    response.headers["tag"] = tag
    response.headers["app"] = "kusari"
    return response



@app.route("/chain/<tag>")
def chain_tag(tag):
    if NEXT:
        next = NEXT
        data = requests.get(f"http://{next}/chain/{tag}", headers={"app": "kusari", "tag": tag}).content
    else:
        next = f"127.0.0.1:{PORT}"
        data = requests.get(f"http://{next}/hometag/{tag}", headers={"app": "kusari", "tag": tag}).content
    response = Response(data)
    response.headers["tag"] = tag
    response.headers["app"] = "kusari"
    return response

@app.route("/chain")
def chain():
    if NEXT:
        next = NEXT
        data = requests.get(f"http://{next}/chain", headers={"app": "kusari"}).content
    else:
        next = f"127.0.0.1:{PORT}"
        data = requests.get(f"http://{next}/", headers={"app": "kusari"}).content
    response = Response(data)
    response.headers["app"] = "kusari"
    return response



if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port=int(PORT))