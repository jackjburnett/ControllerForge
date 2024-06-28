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


if __name__ == "__main__":
    generate_button_cap(wall_thickness=1.0).save("test_files/cap.step")
