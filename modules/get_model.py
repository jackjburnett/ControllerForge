import onnx


# TODO: ONNX extension validation
def get_model(path="parameter_store/ai_models/", onnx_name="trained_model"):
    model = onnx.load(path + onnx_name + ".onnx")
    return model


if __name__ == "__main__":
    get_model(path="test_files/")
