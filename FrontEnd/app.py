from flask import Flask, render_template,jsonify, request
from pymongo import MongoClient
from subprocess import Popen, call
import time
app = Flask(__name__)
app.config['DEBUG'] = True

    
@app.route("/")
def index():

    # System call here to wifite
    # and then kill process
    
    return render_template("index.html")

@app.route("/wifi")
def wifi_page():
    
    availableAPs = ""
    
    with open('/home/pi/Documents/repo/SRR-webapp/BackEnd/availableAPs.txt', 'r') as r:
        
        availableAPs = r.read()
        availableAPs = set(availableAPs.splitlines())
        print(availableAPs)
        if " " in availableAPs:
            availableAPs.remove(" ")
        if "\n" in availableAPs:
            availableAPs.remove("\n")
        if "\x00" in availableAPs:
            availableAPs.remove("\x00")
    return render_template("wifipage.html", availableAPs = availableAPs)

@app.route("/getStatus")
def get_attackStatus():
    client = MongoClient()
    wifiteDB = client["wifiteDB"]
    ourCollection = wifiteDB["ourCollection"]
    currentAttackDict = ourCollection.find({"infoType":"currentAttackName"})[0]
    currentAttackName = currentAttackDict["currentAttackName"]
    return jsonify(currentAttackName=currentAttackName)


@app.route("/getPackets")
def get_packets():
    client = MongoClient()
    wifiteDB = client["wifiteDB"]
    ourCollection = wifiteDB["ourCollection"]
    currentPacketDict = ourCollection.find({"infoType":"packetsCollected"})[0]
    currentIVs = currentPacketDict["ivs"]
    lastIVs = currentPacketDict["last_ivs"]
    rate = float(currentIVs - lastIVs)/5
    return jsonify(ivs=currentIVs,last_ivs=lastIVs,rate=rate)

@app.route("/startAttack/<ssid>")
def startAttack(ssid):

    global current_process
    
    newWifite = "/home/pi/Documents/repo/SRR-webapp/BackEnd/newWifite"

    process = Popen(["sudo", newWifite, "-e", ssid])

    return render_template("startedattack.html", ssid = ssid)


def shutdown_server():

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("not running")
    func()

@app.route("/stopAttack")
def stopAttack():

    shutdown_server()
    return "stopped server"

if __name__ == "__main__":

    app.run(host="0.0.0.0")
