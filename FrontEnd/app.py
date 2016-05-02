from flask import Flask, render_template
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route("/")
def main():

    # System call here to wifite
    # and then kill process
    
    return render_template("index.html")

@app.route("/wifi")
def wifi_page():
    
    
    with r as open('/home/pi/Documents/repo/SRR-webapp/BackEnd/availableAPs.txt', 'r'):
        
        print(r)
        
        
    return render_template("wifipage.html", availableAPs = availableAPs)


if __name__ == "__main__":

    app.run(host='0.0.0.0')
