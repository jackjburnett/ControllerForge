import argparse

from flask import Flask, send_file, request, jsonify

from modules import train_model, predict_parameters, generate_stl
from parameter_store import default_values
from utils import pipeline_test, step2stl, zipfiles

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
    return send_file(
        "parameter_store/ai_models/trained_model.onnx",
        download_name="trained_model.onnx",
        mimetype="application/onnx",
    )


# TODO: Implement this
@app.route("/predict_parameters", methods=["GET"])
def predict_parameters_call():
    predict_parameters.predict_parameters()


# TODO: Implement this
@app.route("/generate_stl", methods=["POST"])
def generate_stl_call():
    if request.is_json:
        try:
            # Parse the JSON data from the request
            json_data = request.get_json()
            if "buttons" in json_data:
                buttons = json_data["buttons"]
            else:
                buttons = None
            if "base" in json_data:
                base = json_data["base"]
            else:
                base = None

            generate_stl.generate_controller_files(base=base, buttons=buttons)
            if base is not None and buttons is not None:
                step2stl.step2stl("generated_files/controller.step")
            zipfiles.zip_controller_files(base=base, buttons=buttons)
            return send_file(
                "generated_files/controller_files.zip",
                download_name="controller_files.zip",
                mimetype="application/zip",
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Request does not contain JSON data"}), 400


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
