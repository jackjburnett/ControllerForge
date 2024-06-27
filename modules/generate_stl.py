import cadquery as cq


def generate_button_cap(
    button_width=24.0,
    top_thickness=2.0,
    wall_thickness=0.0,
    wall_height=3.0,
    bevel=False,
    stem_height=4.0,
    stem_radius=3.0,
    inner_stem_width=4.2,
    inner_stem_length=1.4,
):
    # Create the top
    top = cq.Workplane().circle(button_width / 2).extrude(top_thickness)
    # Add bevel
    if bevel:
        top = top.edges().fillet(0.99)
    # Create the stem
    inner_stem = (
        cq.Workplane()
        .rect(inner_stem_width, inner_stem_length)
        .rect(inner_stem_length, inner_stem_width)
        .extrude(stem_height)
    )
    stem = cq.Workplane().circle(stem_radius).extrude(stem_height).cut(inner_stem)
    # Create walls
    if wall_thickness > 0:
        walls = (
            cq.Workplane()
            .circle(button_width / 2)
            .circle((button_width / 2) - wall_thickness)
            .extrude(wall_height)
        )
    # Combine all parts
    cap = cq.Assembly().add(top).add(stem, loc=cq.Location((0, 0, top_thickness)))
    if wall_thickness > 0:
        cap.add(walls, loc=cq.Location((0, 0, top_thickness / 2)))
    return cap


generate_button_cap(wall_thickness=1.0).save("cap.step")
