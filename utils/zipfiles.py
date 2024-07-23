from zipfile import ZipFile, ZIP_DEFLATED


def zip_controller_files(buttons=None, keys=None, path="generated_files/"):
    files = [path + "base_top.step", path + "base_bottom.step"]
    if buttons is not None:
        for button in buttons.keys():
            files.append(path + button + ".step")
    if keys is not None:
        for key in keys.keys():
            files.append(path + key + ".step")

    # Create a ZipFile object
    with ZipFile(path + "controller_files.zip", "w", ZIP_DEFLATED) as zipf:
        # Add each file to the ZIP file
        for file in files:
            zipf.write(file)


if __name__ == "__main__":
    buttons = {
        "Up": {},
        "Down": {},
    }
    base = {}
    zip_controller_files(base=base, buttons=buttons, path="test_results/")
