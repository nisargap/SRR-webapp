from flask import Flask, render_template
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route("/")
def main():

    return render_template("index.html")

@app.route("/wifi")
def wifi_page():

    return render_template("wifipage.html")


if __name__ == "__main__":

    app.run(host='0.0.0.0')
