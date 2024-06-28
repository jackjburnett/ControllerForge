import argparse

from flask import Flask, send_file

import modules.train_model as train_model
import parameter_store.default_values as default_values
import utils.pipeline_test as pipeline_test

app = Flask(__name__)


@app.route("/")
def index():
    return "Connected to ControllerForge."


@app.route("/train_model", methods=["GET"])
def train_model_call():
    train_model.train_model()
    return "Model Trained"


@app.route("/get_model", methods=["GET"])
def get_model_call():
    return send_file("parameter_store/ai_models/trained_model.onnx")


# TODO: Implement this
@app.route("/predict_parameters", methods=["POST"])
def predict_parameters_call():
    pass


# TODO: Implement this
@app.route("/generate_stl", methods=["POST"])
def generate_stl_call():
    pass


# TODO: Implement this
@app.route("/generate_pcb", methods=["POST"])
def generate_pcb_call():
    pass


# TODO: Implement this
@app.route("/check_conflict", methods=["POST"])
def check_conflict_call():
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Check for flask app arguments.")
    parser.add_argument(
        "--test", "--t", action="store_true", help="Run the pipeline test."
    )
    parser.add_argument(
        "--debug", "--d", action="store_true", help="Run the app with debug mode."
    )
    parser.add_argument(
        "--port", "--p", action="store", help="Set a port number for the flask app."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Checks if a port was passed, if not defaults it to port 5000
    if args.port is not None:
        args.port = int(args.port)
    else:
        args.port = default_values.PORT
    # If --t or --test is given as an argument, run the pipeline test
    if args.test:
        print(pipeline_test.pipeline_test())
    # Default entry is the flask app
    else:
        app.run(debug=args.debug, port=args.port)
