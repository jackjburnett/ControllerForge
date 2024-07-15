import cadquery as cq


# Function to generate text for button caps and key caps
def generate_text(text=None):
    # If no text has been passed, an empty Workplane is returned
    if text is None:
        return cq.Workplane()
    # If text is passed, it will generate text for the cap
    else:
        return cq.Workplane().text(
            text["content"],
            text["size"],
            distance=text["depth"],
            font=text["font"],
            halign="center",
            valign="center",
        )


# Function to add text to a plane, taking a plane, the text, and offsets
def add_text(plane=None, text=None, x_offset=0, y_offset=0):
    # If a plane is not passed, None is returned
    if plane is not None:
        # If there is a plane, text is added to it
        if text is not None:
            # Text is generated using generate_text, then translated using the offsets
            text_workplane = generate_text(text).translate((x_offset, y_offset))
            # If the text is more than 0 depth, it is cut out of the plane
            if text["depth"] > 0:
                plane = plane.cut(text_workplane)
            # If the text has a negative depth, it is added to the plane
            elif text["depth"] < 0:
                plane = plane.add(text_workplane)
            # A depth of 0 results in the text not being put on the plane
    return plane


# Function used to generate the mounts for key caps and button caps
def generate_mount(mount_values=None):
    # If no mount values are passed, mount_values is instantiated to prevent errors
    if mount_values is None:
        mount_values = {"type": "", "diameter": 0}
    # Create the mount based on the mount type
    if mount_values["type"].upper() == "MX":
        # MX mounts generate the mount's X-Point using the width and length of the X_point
        # the current implementation assumes uniformity of the X_point's arms
        mount_x_point = (
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
            .cut(mount_x_point)
        )
    elif mount_values["type"].upper() == "STEM":
        # Stem creates a solid mount for the key
        mount = (
            cq.Workplane()
            .circle(mount_values["diameter"] / 2)
            .extrude(mount_values["height"])
        )
    else:
        # raise ValueError("Mount most have a specified type")
        # If there is no mount, an empty Workplane is returned
        mount = cq.Workplane()
    return mount


# TODO: Generate key caps using json file
# TODO: REWORK TO BE BUILT CORRECTLY
def generate_key_cap(
        units=None, dimensions=None, bevel=False, mount_values=None, text=None
):
    # Parameters derived from the dictionaries values
    top_difference = units["base"] - units["top"]
    top_width = units["top"] * dimensions["width"]
    top_length = units["top"] * dimensions["length"]
    base_width = units["base"] * dimensions["width"]
    base_length = units["base"] * dimensions["length"]
    # Create the top part of the keycap
    top_part = (
        cq.Workplane("XY").rect(top_width, top_length).extrude(dimensions["thickness"])
    )
    # Create the base profile and loft to the top profile
    keycap_body = (
        cq.Workplane("XY")
        .rect(top_width, top_length)
        .workplane(offset=dimensions["height"])
        .rect(base_width, base_length)
        .loft(combine=True)
    )
    # Create the inner hollow part
    inner_keycap = (
        cq.Workplane("XY")
        .rect(
            (top_width - (dimensions["thickness"] * 2)) * dimensions["width"],
            (top_length - (dimensions["thickness"] * 2)) * dimensions["length"],
        )
        .workplane(offset=dimensions["height"])
        .rect(
            (units["base"] - (dimensions["thickness"] * 2)) * dimensions["width"],
            (units["base"] - (dimensions["thickness"] * 2)) * dimensions["length"],
        )
        .loft(combine=True)
    )
    # Cut out the inner keycap to create the hollow
    keycap = keycap_body.cut(inner_keycap)
    # Add rounded corners if requested
    if bevel:
        keycap = keycap.edges().fillet(0.5)
    # Combine the sides and the keycap top
    keycap = top_part.union(keycap)
    # Add text to the keycap
    keycap = add_text(
        plane=keycap,
        text=text,
        x_offset=text.get("x", 0),
        y_offset=text.get("y", 0),
    )
    # Generate the mount
    mount = generate_mount(mount_values)
    # Create the cap assembly
    cap = (
        cq.Assembly()
        .add(keycap)
        .add(mount, loc=cq.Location((0, 0, dimensions["thickness"])))
    )
    # Return the cap
    return cap


# generate_button_cap is a function for generating button caps
# the function produces a default button cap if no values are passed to it
# the default button is 24mm in diameter and 2mm thick with no walls or  bevel
# the default mount is the Cherry MX clone found on Kailh Red switches
# TODO: Add convex and concave buttons
# TODO: Add comments
# TODO: REWORK TO BE BUILT CORRECTLY
def generate_button_cap(
        diameter=24.0, thickness=2.0, bevel=False, wall=None, mount_values=None, text=None
):
    # Create the top of the button, using the diameter and thickness
    top = cq.Workplane().circle(diameter / 2).extrude(thickness)
    # Add bevel to the button, if it has been requested
    if bevel:
        top = top.edges().fillet(0.99)
    # text is added to the top of the button, if text is none this will just return the top
    top = add_text(
        plane=top, text=text, x_offset=-(text.get("x", 0)), y_offset=text.get("y", 0)
    )
    mount = generate_mount(mount_values)
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


# Function that generates a USB_C receptacle port cutout using a height, width, corner radius, and wall thickness
def generate_usb_c(height=4, width=11, corner_radius=1, wall_thickness=2):
    return (
        cq.Workplane()
        .rect(width, height)
        .extrude(wall_thickness)
        .edges("|Z")
        .fillet(corner_radius)
    )


# TODO: Implement
# TODO: Comment
def add_usb_c(usb_c=None, x_offset=0, y_offset=0):
    pass


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
            "width": max_x + 5,
            "length": max_y + 5,
            "thickness": 2.5,
            "rounded_edges": True,
            "screw_radius": 0,
            "corner_radius": 5,
        }
    return base


# TODO: Convert to generate_simple_base
# TODO: What if base is larger than printer?
# TODO: Comment
# TODO: Add 'modular' option to base
# TODO: Generate ModularBase ipynb
# TODO: Create GenerateModularBase
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
        keys=None,
):
    base_top, base_bottom = generate_base(base)
    button_steps = []
    if buttons is not None:
        for button_name, button_values in buttons.items():
            button_steps.append(
                [
                    generate_button_cap(
                        diameter=button_values.get("diameter", 24.0),
                        thickness=button_values.get("thickness", 2.0),
                        bevel=button_values.get("bevel", False),
                        mount_values=button_values.get("mount", None),
                        wall=button_values.get("wall", None),
                        text=button_values.get("text", None),
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
                        -(button_values["x"] - offset_x),
                        (button_values["y"] - offset_y),
                        0,
                    )
                )
            )
            base_top = base_top.cut(button_hole)
        if keys is not None:
            pass
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
                        -(button_values["x"] - base["width"] / 2),
                        (button_values["y"] - base["length"] / 2),
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
            "text": {"content": "↑", "size": 12, "depth": 1, "font": "Arial"},
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
            "text": {
                "content": "down",
                "size": 12,
                "depth": -1,
                "font": "Arial",
                "x": 0,
                "y": 0,
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
    keys = {
        "A": {
            "x": 70,
            "y": 30,
            "bevel": True,
            "mount": {
                "type": "MX",
                "height": 4.0,
                "diameter": 6.0,
                "X_point_width": 4.2,
                "X_point_length": 1.4,
            },
            "units": {"top": 15, "base": 20},
            "dimensions": {"width": 1, "length": 1, "height": 15, "thickness": 2},
            "text": {
                "content": "A",
                "size": 12,
                "depth": -1,
                "font": "Arial",
                "x": 1,
                "y": 1,
            },
        },
        "B": {
            "x": 40,
            "y": 20,
            "bevel": False,
            "mount": {
                "type": "MX",
                "height": 4.0,
                "diameter": 6.0,
                "X_point_width": 4.2,
                "X_point_length": 1.4,
            },
            "units": {"top": 20, "base": 25},
            "dimensions": {"width": 1, "length": 1, "height": 15, "thickness": 2},
            "text": {
                "content": "B",
                "size": 12,
                "depth": 1,
                "font": "Arial",
                "x": -1,
                "y": -1,
            },
        },
    }
    generate_controller_files(path="test_files/", base=base, buttons=buttons)
    path = "test_files/"
    generate_key_cap(
        units=keys["A"]["units"],
        dimensions=keys["A"]["dimensions"],
        bevel=keys["A"]["bevel"],
        mount_values=keys["A"]["mount"],
        text=keys["A"]["text"],
    ).save(path + "A.step")
    generate_key_cap(
        units=keys["B"]["units"],
        dimensions=keys["B"]["dimensions"],
        bevel=keys["B"]["bevel"],
        mount_values=keys["B"]["mount"],
        text=keys["B"]["text"],
    ).save(path + "B.step")
