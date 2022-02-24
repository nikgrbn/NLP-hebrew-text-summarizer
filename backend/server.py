from flask import Flask

app = Flask(__name__)

@app.route("/")
def example():
    return {"hello" : "good luck"}

if __name__ == "__main__":
    app.run(debug=True)
