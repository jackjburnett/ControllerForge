import onnxruntime as rt


def predict_parameters(path="parameter_store/ai_models/", onnx_name="trained_model"):
    sess = rt.InferenceSession(
        path + onnx_name + ".onnx", providers=["CPUExecutionProvider"]
    )
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred_onx = sess.run([label_name], {input_name: [[6.9, 3.1, 4.9, 1.5]]})[0]
    return pred_onx


if __name__ == "__main__":
    print(predict_parameters(path="test_files/"))
