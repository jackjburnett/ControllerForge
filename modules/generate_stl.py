import cadquery as cq


# generate_button_cap is a function for generating button caps
# the function produces a default button cap if no values are passed to it
# the default button is 24mm in diameter and 2mm thick with no walls or  bevel
# the default mount is the Cherry MX clone found on Kailh Red switches
def generate_button_cap(
        diameter=24.0,
        thickness=2.0,
        bevel=False,
        wall=None,
        mount_values=None,
):
    # Sets a default mount, if one has not been passed
    if mount_values is None:
        mount_values = {
            "type": "MX",
            "height": 4.05,
            "X_point_width": 4.2,
            "X_point_length": 1.4,
            "diameter": 6.0,
        }
    # Create the top of the button, using the diameter and thickness
    top = cq.Workplane().circle(diameter / 2).extrude(thickness)
    # Add bevel to the button, if it has been requested
    if bevel:
        top = top.edges().fillet(0.99)
    # Create the mount based on the mount type
    if mount_values["type"] == "MX":
        # MX mounts generate the mount's X-Point using the width and length of the X_point
        # the current implementation assumes uniformity of the X_point's arms
        mount_X_point = (
            cq.Workplane()
            .rect(mount_values["X_point_width"], mount_values["X_point_length"])
            .rect(mount_values["X_point_length"], mount_values["X_point_width"])
            .extrude(mount_values["height"])
        )
        # The mount is generated by cutting the X_point out of the mount's radius (diameter/2)
        mount = (
            cq.Workplane()
            .circle(mount_values["diameter"] / 2)
            .extrude(mount_values["height"])
            .cut(mount_X_point)
        )
    else:
        mount = (
            cq.Workplane()
            .circle(mount_values["diameter"] / 2)
            .extrude(mount_values["height"])
        )
    # Combine all parts of the button cap into an assembly
    cap = cq.Assembly().add(top).add(mount, loc=cq.Location((0, 0, thickness)))
    # If no wall is provided, an empty wall is created
    if wall is None:
        wall = {"thickness": 0.0, "height": 0.0}
    # If the walls have a thickness and height above 0, they are generated then added to the assembly
    if wall["thickness"] > 0.0 and wall["height"] > 0.0:
        walls = (
            cq.Workplane()
            .circle(diameter / 2)
            .circle((diameter / 2) - wall["thickness"])
            .extrude(wall["height"])
        )
        cap.add(walls, loc=cq.Location((0, 0, thickness / 2)))
    # Return the assembled button cap
    return cap


# TODO: Implement
# TODO: Comment
def calculate_base_from_buttons(buttons=None):
    if buttons is None:
        base = {
            "height": 5,
            "width": 5,
            "length": 5,
            "thickness": 1,
            "rounded_edges": False,
            "screw_radius": 0,
            "corner_radius": 1,
        }
    else:
        max_x = 0
        max_y = 0
        for button in buttons.values():
            if (button["y"] + (button["diameter"] / 2) + 5) > max_y:
                max_y = button["y"] + (button["diameter"] / 2) + 5
            if (button["x"] + (button["diameter"] / 2) + 5) > max_x:
                max_x = button["x"] + (button["diameter"] / 2) + 5
        base = {
            "height": 25,
            "width": (max_x + 5) / 2,
            "length": max_y + 5,
            "thickness": 2.5,
            "rounded_edges": True,
            "screw_radius": 0,
            "corner_radius": 5,
        }
    return base


# TODO: What if base is larger than printer?
# TODO: Comment
def generate_base(base=None):
    if base is None:
        base = {
            "height": 50,
            "width": 200,
            "length": 100,
            "thickness": 5,
            "rounded_edges": False,
            "screw_radius": 1,
            "corner_radius": 5,
        }
    # TODO: Use dictionary values instead of assigning variable
    width = base["width"]
    height = base["height"]
    length = base["length"]
    thickness = base["thickness"]
    rounded_edges = base["rounded_edges"]
    corner_radius = base["corner_radius"]
    screw_radius = base["screw_radius"]
    # Set corner positions in advance
    positions = [
        (
            -(width / 2 - (thickness + corner_radius)),
            -(length / 2 - (thickness + corner_radius)),
            thickness,
        ),
        (
            -(width / 2 - (thickness + corner_radius)),
            length / 2 - (thickness + corner_radius),
            thickness,
        ),
        (
            width / 2 - (thickness + corner_radius),
            -(length / 2 - (thickness + corner_radius)),
            thickness,
        ),
        (
            width / 2 - (thickness + corner_radius),
            length / 2 - (thickness + corner_radius),
            thickness,
        ),
    ]

    # Create bottom of base
    bottom_base = cq.Workplane().rect(width, length).extrude(height)
    # Add rounded edges to bottom base
    if rounded_edges:
        bottom_base = bottom_base.fillet(1)
    inner_base = (
        cq.Workplane()
        .rect(width - (thickness * 2), length - (thickness * 2))
        .extrude(height - thickness)
    )
    bottom_base = bottom_base.cut(inner_base)
    # Add corners for screw/plugs to bottom base
    corner = cq.Workplane().circle(corner_radius).extrude(height - thickness)
    corners = cq.Workplane()
    for pos in positions:
        corners = corners.union(corner.translate(pos))
    bottom_base = bottom_base.union(corners)
    # Add the screw holes or slots to the bottom base
    corner_holes = cq.Workplane()
    if screw_radius > 0.0:
        corner_hole = (
            cq.Workplane().circle(screw_radius).extrude(height - (thickness * 2))
        )
    else:
        corner_hole = cq.Workplane().circle(corner_radius / 2).extrude(thickness)
    for pos in positions:
        corner_holes = corner_holes.union(corner_hole.translate(pos))
    bottom_base = bottom_base.cut(corner_holes)
    # Create top base
    top_base = (
        cq.Workplane()
        .rect(width - (thickness * 2) - 0.5, length - (thickness * 2) - 0.5)
        .extrude(thickness)
    )
    # Add the screw holes or slots to the top base
    if screw_radius > 0.0:
        top_base = top_base.cut(corner_holes.translate((0, 0, -thickness)))
    else:
        top_base = top_base.union(corner_holes.translate((0, 0, 0)))
    return top_base, bottom_base


# TODO: Comment
# TODO: Add printer
def generate_controller(
        base=None,
        buttons=None,
):
    base_top, base_bottom = generate_base(base)
    button_steps = []
    if buttons is not None:
        for button_name, button_values in buttons.items():
            button_steps.append(
                [
                    generate_button_cap(
                        diameter=button_values["diameter"],
                        thickness=button_values["thickness"],
                        bevel=button_values["bevel"],
                        mount_values=button_values["mount"],
                        wall=button_values["wall"],
                    ),
                    button_name,
                ]
            )
            offset_x = base["width"] / 2
            offset_y = base["length"] / 2
            button_hole = (
                cq.Workplane()
                .circle((button_values["diameter"] / 2) + 1)
                .extrude(base["thickness"])
                .translate(
                    (
                        button_values["x"] - offset_x,
                        button_values["y"] - offset_y,
                        0,
                    )
                )
            )
            base_top = base_top.cut(button_hole)
    return base_top, base_bottom, button_steps


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
                        button_values["x"] - base["width"] / 2,
                        button_values["y"] - base["length"] / 2,
                        -(button_values["mount"]["height"]),
                    )
                ),
            )
            i += 1
    controller_assembly.save(path + "controller.step")


# TODO: Comment
# TODO: Add printer
def generate_controller_files(path="generated_files/", base=None, buttons=None):
    if base is None and buttons is not None:
        base = calculate_base_from_buttons(buttons)
    if base is not None or buttons is not None:
        base_top, base_bottom, button_steps = generate_controller(
            base=base, buttons=buttons
        )
        cq.exporters.export(base_top, path + "base_top.step")
        cq.exporters.export(base_bottom, path + "base_bottom.step")
        for button in button_steps:
            button[0].save(path + button[1] + ".step")
        generate_controller_assembly(
            base=base,
            base_top=base_top,
            base_bottom=base_bottom,
            buttons=buttons,
            button_steps=button_steps,
            path=path,
        )


# TODO: Comment
if __name__ == "__main__":
    buttons = {
        "UP": {
            "x": 20,
            "y": 15,
            "diameter": 24.0,
            "thickness": 2.0,
            "bevel": False,
            "mount": {
                "type": "MX",
                "height": 4.0,
                "diameter": 6.0,
                "X_point_width": 4.2,
                "X_point_length": 1.4,
            },
            "wall": {
                "thickness": 1.0,
                "height": 3.0,
            },
        },
        "DOWN": {
            "x": 70,
            "y": 30,
            "diameter": 24.0,
            "thickness": 2.0,
            "bevel": True,
            "mount": {
                "type": "MX",
                "height": 4.0,
                "diameter": 6.0,
                "X_point_width": 4.2,
                "X_point_length": 1.4,
            },
            "wall": {
                "thickness": 1.0,
                "height": 3.0,
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
    generate_controller_files(path="test_files/", base=base, buttons=buttons)
