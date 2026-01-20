def get_next_version(csda_version: str, tag: str) -> str:
    """Calculate the next version based on the given tag."""
    csda_version_parts = csda_version.split(".")
    assert tag.startswith("v")
    tag_parts = tag[1:].split(".")
    if (
        csda_version_parts[0] == tag_parts[0]
        and csda_version_parts[1] == tag_parts[1]
        and csda_version_parts[2] == tag_parts[2]
    ):
        return ".".join(tag_parts[0:3] + [str(int(tag_parts[3]) + 1)])
    else:
        return ".".join(csda_version_parts + ["0"])
