# TODO: move step2stl here


# TODO: Comment
def generate_controller_assembly(
    base, base_top, base_bottom, button_steps, buttons, path="generated_files/"
):
    controller_assembly = cq.Assembly().add(base_top).add(base_bottom)
    i = 0
    if buttons is not None:
        for button_values in buttons.values():
            controller_assembly.add(
                button_steps[i][0],
                loc=cq.Location(
                    (
                        -(button_values["x"] - base["width"] / 2),
                        (button_values["y"] - base["length"] / 2),
                        -(button_values["mount"]["height"]),
                    )
                ),
            )
            i += 1
    controller_assembly.save(path + "controller.step")


generate_controller_assembly(
    base=base,
    base_top=base_top,
    base_bottom=base_bottom,
    buttons=buttons,
    button_steps=button_steps,
    path=path,
)


# TODO: Move to generate_stl
def step2stl(filename):
    if filename.lower().endswith(".stl"):
        return 1
    elif filename.lower().endswith(".step"):
        step = cq.importers.importStep(filename)
        filename = filename[:-5]
        cq.exporters.export(step, filename + ".stl")
        return 0
    else:
        step = cq.importers.importStep(filename + ".step")
        cq.exporters.export(step, filename + ".stl")
        return 0
