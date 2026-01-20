import os
import sys


def get_next_version(csda_version: str, tag: str) -> str:
    """Calculate the next version based on the given tag."""
    csda_version_parts = csda_version.split(".")
    if tag.startswith("v"):
        tag_parts = tag[1:].split(".")
        if "-" in tag_parts[2]:
            tag_parts = tag_parts[0:2] + tag_parts[2].split("-")
    else:
        tag_parts = None
    if (
        tag_parts
        and csda_version_parts[0] == tag_parts[0]
        and csda_version_parts[1] == tag_parts[1]
        and csda_version_parts[2] == tag_parts[2]
    ):
        return ".".join(tag_parts[0:3]) + "-" + str(int(tag_parts[3]) + 1)
    else:
        return ".".join(csda_version_parts) + "-0"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception(
            f"Invalid number of arguments, expected 2, got {len(sys.argv) - 1}"
        )
    csda_version = sys.argv[1]
    tag = sys.argv[2]
    version = get_next_version(csda_version, tag)
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"version={version}\n")
    else:
        print(version)
