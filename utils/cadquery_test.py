import difflib
import sys

import cadquery as cq

height = 60.0
width = 80.0
thickness = 10.0
diameter = 22.0
padding = 12.0

# make the base
result = (
    cq.Workplane("XY")
    .box(height, width, thickness)
    .faces(">Z")
    .workplane()
    .hole(diameter)
    .faces(">Z")
    .workplane()
    .rect(height - padding, width - padding, forConstruction=True)
    .vertices()
    .cboreHole(2.4, 4.4, 2.1)
    .edges("|Z")
    .fillet(2.0)
)

# Export
cq.exporters.export(result, "cadquery_test_results/result.stl")
cq.exporters.export(result.section(), "cadquery_test_results/result.dxf")
cq.exporters.export(result, "cadquery_test_results/result.step")

# Check diff
# As long as only the FILE_NAME line is output, cadquery is working fine
with open("cadquery_test_results/expected_result.step", "r") as expected_result:
    with open("cadquery_test_results/result.step", "r") as result:
        diff = difflib.unified_diff(
            expected_result.readlines(),
            result.readlines(),
            fromfile="expected_result",
            tofile="result",
        )
        for line in diff:
            for prefix in ("-", "+"):
                if line.startswith(prefix):
                    sys.stdout.write(line)
