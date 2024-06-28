import numpy as np

# Convert into ONNX format.
from skl2onnx import to_onnx
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def train_model(path="parameter_store/ai_models/"):
    iris = load_iris()
    X, y = iris.data, iris.target
    X = X.astype(np.float32)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    clr = RandomForestClassifier()
    clr.fit(X_train, y_train)

    onx = to_onnx(clr, X[:1])
    with open(path + "trained_model.onnx", "wb") as f:
        f.write(onx.SerializeToString())


if __name__ == "__main__":
    train_model(path="test_files/")
