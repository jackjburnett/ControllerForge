import json

import modules.generate_stl as generate_stl
import modules.get_model as get_model
import modules.train_model as train_model

train_model.train_model()
with open("parameter_store/switches/kailh.json") as f:
    kailh = json.load(f)
generate_stl.generate_button_cap(
    mount_height=kailh["Red"]["dimensions"]["mount"]["height"],
    mount_cross_width=kailh["Red"]["dimensions"]["mount"]["cross_width"],
    mount_cross_length=kailh["Red"]["dimensions"]["mount"]["cross_length"],
    mount_radius=(kailh["Red"]["dimensions"]["mount"]["cross_width"] / 2) + 1,
    wall_thickness=1.0,
).save("generated_files/cap.step")
get_model
