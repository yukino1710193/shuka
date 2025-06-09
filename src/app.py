from flask import Flask, Response, jsonify, request, g
import os, requests, time, datetime, logging

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger("shuka")

app = Flask(__name__)

TARGET = os.environ.get('TARGET', 'Konnichiwa')
PORT = os.environ.get('PORT', 80)
NEXT = os.environ.get('NEXT', "")
PODNAME = os.environ.get('PODNAME', "")
NODENAME = os.environ.get('NODENAME', "")


@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def add_processing_time(response):
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        logger.info(f"{request.method} {request.path} took {duration:.9f} seconds from {request.remote_addr}")
        response.headers["Shuka-Processing-Time"] = f"{duration:.9f}s"
    return response

@app.route("/")
def index():
    if PODNAME or NODENAME:
        response = Response(f"{TARGET} from {PODNAME} in {NODENAME}\n")
    else:
        response = Response(f"{TARGET}\n")
    response.headers["app"] = "shuka-yukino"
    return response



@app.route("/nodename")
def getNodeName():
    if NODENAME:
        response = Response(f"{NODENAME}\n")
    else:
        response = Response(f"{TARGET}\n")
    response.headers["app"] = "shuka"
    return response



@app.route("/sleep/<sleepTime>")
def sleep(sleepTime):
    print(f"Shuka starts sleep in {int(sleepTime)/1000} seconds")
    startTime = datetime.datetime.now()
    time.sleep(int(sleepTime)/1000)
    endTime = datetime.datetime.now()
    print(f"Shuka ends sleep after {int(sleepTime)/1000} seconds")
    return f"Shuka wa {(endTime - startTime).total_seconds()} byougo ni mezameta"



@app.route("/probe")
def probe():
    if request.headers.get("healthcheck") is None:
        return jsonify({"message": "ready"}), 200
    if request.headers.get("healthcheck") == "success":
        return jsonify({"message": "success"}), 200
    if request.headers.get("healthcheck") == "failed":
        return jsonify({"message": "failed"}), 500
    # if status == "ready":
    #     return jsonify({"message": "ready"}), 200
    # if status == "failed":
    #     return jsonify({"message": "failed"}), 500



@app.route("/hometag/<tag>")
def home_tag(tag):
    response = Response(f"{TARGET}\n")
    response.headers["tag"] = tag
    response.headers["app"] = "shuka"
    return response



@app.route("/chain/<tag>")
def chain_tag(tag):
    if NEXT:
        next = NEXT
        data = requests.get(f"http://{next}/chain/{tag}", headers={"app": "shuka", "tag": tag}).content
    else:
        next = f"127.0.0.1:{PORT}"
        data = requests.get(f"http://{next}/hometag/{tag}", headers={"app": "shuka", "tag": tag}).content
    response = Response(data)
    response.headers["tag"] = tag
    response.headers["app"] = "shuka"
    return response

@app.route("/chain")
def chain():
    if NEXT:
        next = NEXT
        data = requests.get(f"http://{next}/chain", headers={"app": "shuka"}).content
    else:
        next = f"127.0.0.1:{PORT}"
        data = requests.get(f"http://{next}/", headers={"app": "shuka"}).content
    response = Response(data)
    response.headers["app"] = "shuka"
    return response



if __name__ == "__main__":
    print(PORT)
    app.run(debug=True,host='127.0.0.1',port=int(PORT))
    