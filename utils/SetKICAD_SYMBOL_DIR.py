import os


def SetKSD(KCDPath=r"C:\Program Files\KiCad\8.0\share\kicad\symbols"):
    # Set the KICAD_SYMBOL_DIR environment variable
    os.environ["KICAD_SYMBOL_DIR"] = KCDPath

    # Now you can use os.environ['KICAD_SYMBOL_DIR'] in your script to access the set value
    return "KICAD_SYMBOL_DIR set to:", os.environ["KICAD_SYMBOL_DIR"]


if __name__ == "__main__":
    print(SetKSD())
