import json

from modules import generate_step, get_model, train_model
from utils import step2stl, zipfiles


def pipeline_test():
    train_model.train_model()
    with open("parameter_store/switches/kailh.json") as f:
        kailh = json.load(f)
    buttons = {
        "UP": {
            "x": 70,
            "y": 30,
            "diameter": 24.0,
            "thickness": 2.0,
            "bevel": False,
            "wall": {
                "thickness": 0.0,
                "height": 0.0,
            },
            "mount": {
                "type": kailh["Red"]["dimensions"]["mount"]["type"],
                "height": kailh["Red"]["dimensions"]["mount"]["height"],
                "diameter": (kailh["Red"]["dimensions"]["mount"]["X_point_width"] / 2)
                            + 1,
                "X_point_width": kailh["Red"]["dimensions"]["mount"]["X_point_width"],
                "X_point_length": kailh["Red"]["dimensions"]["mount"]["X_point_length"],
            },
        },
        "DOWN": {
            "x": 35,
            "y": 15,
            "diameter": 30.0,
            "thickness": 2.0,
            "bevel": True,
            "wall": {
                "thickness": 1.0,
                "height": 3.0,
            },
            "mount": {
                "type": kailh["Red"]["dimensions"]["mount"]["type"],
                "height": kailh["Red"]["dimensions"]["mount"]["height"],
                "diameter": (kailh["Red"]["dimensions"]["mount"]["X_point_width"] / 2)
                            + 1,
                "X_point_width": kailh["Red"]["dimensions"]["mount"]["X_point_width"],
                "X_point_length": kailh["Red"]["dimensions"]["mount"]["X_point_length"],
            },
        },
    }
    base = {
        "height": 25,
        "width": 200,
        "length": 100,
        "thickness": 2.5,
        "rounded_edges": True,
        "screw_radius": 1,
        "corner_radius": 5,
    }

    generate_stl.generate_controller_files(base=base, buttons=buttons)
    step2stl.step2stl("generated_files/controller.step")
    zipfiles.zip_controller_files(base=base, buttons=buttons)

    get_model.get_model()
    return "Pipeline Test Complete"


if __name__ == "__main__":
    print("Please test the pipeline via ControllerForge.py")
