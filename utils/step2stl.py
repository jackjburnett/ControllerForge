import cadquery as cq


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


if __name__ == "__main__":
    step2stl("test_results/step_test")
