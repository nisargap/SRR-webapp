from flask import Flask, render_template
from pymongo import MongoClient
import subprocess

app = Flask(__name__)
app.config['DEBUG'] = True
@app.route("/")
def main():

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


@app.route("/getPackets")
def get_packets():
    client = MongoClient()
    wifiteDB = client["wifiteDB"]
    ourCollection = wifiteDB["ourCollection"]
    currentPacketDict = ourCollection.find({"infoType":"packetsCollected"})[0]
    currentIVs = currentPacketDict["ivs"]
    lastIVs = currentPacketDict["last_ivs"]
    print currentIVs
    print lastIVs

                            

if __name__ == "__main__":

    app.run(host='0.0.0.0')
