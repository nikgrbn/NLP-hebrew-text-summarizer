from flask import Flask, request
from flask_cors import CORS
import flask

from src.model import model_connectors
from src.svd import *
from src.tf_idf import *
from src.abstractor import *
from src.main import *


def thread_load_model():
    global model
    model = load_model()
    print("\nModel loaded successfully.")

def countdown(stop):
    t = 0
    dc = 0
    while True:
        mins, secs = divmod(t, 60)
        timer = 'Loading model{:<4}- {:02d}:{:02d}'.format('.'*(dc % 4), mins, secs)
        print("\r" + timer, end="", flush=True)
        time.sleep(1)
        t += 1
        dc += 1

        if stop():
            break

app = Flask(__name__)
CORS(app)

model: gensim.models.fasttext.FastText


th_load = threading.Thread(target=thread_load_model)
stop_timer = False
th_timer = threading.Thread(target=countdown, args=(lambda: stop_timer,))
th_load.start()
th_timer.start()

th_load.join()
stop_timer = True
th_timer.join()

@app.route("/summary", methods=['POST'])
def summary():
    global model



    text = request.data
    text = text.decode()[1:-1]
    text = text.replace('\\n', '')
    text = text.replace('\\t', '')
    text = text.replace('\\', '')
    print(text)
    summary = main(text, model)
    print(summary)
    

    response = flask.jsonify({"payload" : summary})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




if __name__ == "__main__":
    app.run(debug=True)