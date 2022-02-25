from flask import Flask
import flask

app = Flask(__name__)

@app.route("/summary", methods=['GET'])
def example():
    response = flask.jsonify({"hello" : "good luck"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)
