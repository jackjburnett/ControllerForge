import cadquery as cq


def generate_button_cap(
    button_width=24.0,
    top_thickness=2.0,
    wall_thickness=0.0,
    wall_height=3.0,
    bevel=False,
    mount_height=4.0,
    mount_radius=3.0,
    mount_cross_width=4.2,
    mount_cross_length=1.4,
):
    # Create the top
    top = cq.Workplane().circle(button_width / 2).extrude(top_thickness)
    # Add bevel
    if bevel:
        top = top.edges().fillet(0.99)
    # Create the mount
    # TODO: Implement further mount types and check current mount type
    mount_cross = (
        cq.Workplane()
        .rect(mount_cross_width, mount_cross_length)
        .rect(mount_cross_length, mount_cross_width)
        .extrude(mount_height)
    )
    mount = cq.Workplane().circle(mount_radius).extrude(mount_height).cut(mount_cross)
    # Create walls
    if wall_thickness > 0:
        walls = (
            cq.Workplane()
            .circle(button_width / 2)
            .circle((button_width / 2) - wall_thickness)
            .extrude(wall_height)
        )
    # Combine all parts
    cap = cq.Assembly().add(top).add(mount, loc=cq.Location((0, 0, top_thickness)))
    if wall_thickness > 0:
        cap.add(walls, loc=cq.Location((0, 0, top_thickness / 2)))
    return cap


def generate_base(
    base_height=50,
    base_width=200,
    base_length=100,
    wall_thickness=5,
    rounded_edges=True,
    screws=False,
    screw_radius=1,
    corner_radius=5,
):
    # Set corner positions in advance
    positions = [
        (
            -(base_width / 2 - (wall_thickness * 2)),
            -(base_length / 2 - (wall_thickness * 2)),
            wall_thickness,
        ),
        (
            -(base_width / 2 - (wall_thickness * 2)),
            base_length / 2 - (wall_thickness * 2),
            wall_thickness,
        ),
        (
            base_width / 2 - (wall_thickness * 2),
            -(base_length / 2 - (wall_thickness * 2)),
            wall_thickness,
        ),
        (
            base_width / 2 - (wall_thickness * 2),
            base_length / 2 - (wall_thickness * 2),
            wall_thickness,
        ),
    ]

    # Create bottom of base
    bottom_base = cq.Workplane().rect(base_width, base_length).extrude(base_height)
    inner_base = (
        cq.Workplane()
        .rect(base_width - (wall_thickness * 2), base_length - (wall_thickness * 2))
        .extrude(base_height - (wall_thickness * 2))
    )
    bottom_base = bottom_base.cut(inner_base)
    # Add rounded edges to bottom base
    if rounded_edges:
        bottom_base = bottom_base.fillet(2)
    # Add corners for screw/plugs to bottom base
    corner = cq.Workplane().circle(corner_radius).extrude(base_height - wall_thickness)
    corners = cq.Workplane()
    for pos in positions:
        corners = corners.union(corner.translate(pos))
    bottom_base = bottom_base.union(corners)
    # Add the screw holes or slots to the bottom base
    corner_holes = cq.Workplane()
    if screws:
        corner_hole = (
            cq.Workplane()
            .circle(screw_radius)
            .extrude(base_height - (wall_thickness * 2))
        )
    else:
        corner_hole = cq.Workplane().circle(corner_radius / 2).extrude(wall_thickness)
    for pos in positions:
        corner_holes = corner_holes.union(corner_hole.translate(pos))
    bottom_base = bottom_base.cut(corner_holes)
    # Create top base
    top_base = (
        cq.Workplane()
        .rect(base_width - (wall_thickness * 2), base_length - (wall_thickness * 2))
        .extrude(wall_thickness)
    )
    # Add rounded edges to the top base
    if rounded_edges:
        top_base = top_base.fillet(2)
    # Add the screw holes or slots to the top base
    if screws:
        top_base = top_base.cut(corner_holes.translate((0, 0, -wall_thickness)))
    else:
        top_base = top_base.union(corner_holes.translate((0, 0, 0)))
    return top_base, bottom_base


def generate_controller(
    base_height=50,
    base_width=200,
    base_length=100,
    base_wall_thickness=5,
    rounded_edges=True,
    screws=False,
    screw_radius=1,
    corner_radius=5,
    buttons=None,
):
    base_top, base_bottom = generate_base(
        base_height,
        base_width,
        base_length,
        base_wall_thickness,
        rounded_edges,
        screws,
        screw_radius,
        corner_radius,
    )
    button_steps = []
    if buttons is not None:
        for button_values in buttons.values():
            button_steps.append(
                generate_button_cap(
                    button_values["button_width"],
                    button_values["top_thickness"],
                    button_values["wall_thickness"],
                    button_values["wall_height"],
                    button_values["bevel"],
                    button_values["mount_height"],
                    button_values["mount_radius"],
                    button_values["mount_cross_width"],
                    button_values["mount_cross_length"],
                )
            )
            button_hole = (
                cq.Workplane()
                .circle(button_values["button_width"] / 2)
                .extrude(base_wall_thickness)
                .translate((button_values["button_x"], button_values["button_y"], 0))
            )
            base_top = base_top.cut(button_hole)
    return base_top, base_bottom, button_steps


if __name__ == "__main__":
    # Uncomment below four lines to test individual functionalities
    # generate_button_cap(wall_thickness=1.0).save("test_files/cap.step")
    # Create an assembly of the full base
    # base_top, base_bottom = generate_base()
    # base = (cq.Assembly().add(base_top).add(base_bottom)).save("test_files/base.step")

    buttons = {
        "button1": {
            "button_x": -10,
            "button_y": -5,
            "button_width": 24.0,
            "top_thickness": 2.0,
            "wall_thickness": 0.0,
            "wall_height": 3.0,
            "bevel": False,
            "mount_height": 4.0,
            "mount_radius": 3.0,
            "mount_cross_width": 4.2,
            "mount_cross_length": 1.4,
        },
        "button2": {
            "button_x": -50,
            "button_y": 10,
            "button_width": 24.0,
            "top_thickness": 2.0,
            "wall_thickness": 0.0,
            "wall_height": 3.0,
            "bevel": False,
            "mount_height": 4.0,
            "mount_radius": 3.0,
            "mount_cross_width": 4.2,
            "mount_cross_length": 1.4,
        },
    }
    base_top, base_bottom, button_steps = generate_controller(buttons=buttons)
    cq.exporters.export(base_top, "test_files/base_top.step")
