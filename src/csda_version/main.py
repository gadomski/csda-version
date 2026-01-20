import os
import sys

from . import get_next_version

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
