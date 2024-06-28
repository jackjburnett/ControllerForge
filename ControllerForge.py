import modules.generate_stl as generate_stl
import modules.train_model as train_model

train_model.train_model()
generate_stl.generate_button_cap(wall_thickness=1.0).save("generated_files/cap.step")
