from zipfile import ZipFile, ZIP_DEFLATED


def zip_controller_files(base=None, buttons=None, path="generated_files/"):
    files = []
    if base is not None:
        files.append(path + "base_top.step")
        files.append(path + "base_bottom.step")
    if buttons is not None:
        # TODO
        i = 0
        for button in buttons.values():
            files.append(path + "button" + str(i) + ".step")
            i += 1
    if buttons is not None and base is not None:
        files.append(path + "controller.stl")
    # Create a ZipFile object
    with ZipFile(path + "controller_files.zip", "w", ZIP_DEFLATED) as zipf:
        # Add each file to the ZIP file
        for file in files:
            zipf.write(file)


if __name__ == "__main__":
    buttons = {
        "button1": {},
        "button2": {},
    }
    base = {}
    zip_controller_files(base=base, buttons=buttons, path="test_results/")
