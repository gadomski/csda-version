from __future__ import annotations

import os
from typing import Literal

import click
from pydantic import BaseModel, Field


class CsdaVersion(BaseModel):
    year: int = Field(gt=2000, lt=2100)
    pi: Literal[1, 2, 3, 4]
    sprint: int

    @classmethod
    def parse(cls, s: str) -> CsdaVersion:
        parts = s.split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid CSDA version: {s}")
        return CsdaVersion.model_validate(
            {"year": int("20" + parts[0]), "pi": int(parts[1]), "sprint": parts[2]}
        )

    def to_str(self) -> str:
        return f"{str(self.year)[2:]}.{self.pi}.{self.sprint}"


class Tag(CsdaVersion):
    release: int

    @classmethod
    def parse(cls, s: str) -> Tag:
        if not s.startswith("v"):
            raise ValueError(f"Invalid tag: {s}")
        parts = s.split(".")
        if len(parts) == 3 and "-" in parts[2]:
            parts = parts[0:2] + parts[2].split("-")
        if len(parts) != 4:
            raise ValueError(f"Invalid tag: {s}")
        return Tag.model_validate(
            {
                "year": int("20" + parts[0][1:]),
                "pi": int(parts[1]),
                "sprint": parts[2],
                "release": parts[3],
            }
        )

    def to_str(self) -> str:
        csda_version_str = super().to_str()
        return csda_version_str + "-" + str(self.release)


def get_next_version(csda_version_str: str, tag_str: str) -> str:
    """Calculate the next version based on the given tag."""
    csda_version = CsdaVersion.parse(csda_version_str)
    if tag_str:
        tag = Tag.parse(tag_str)
    else:
        tag = None
    if (
        tag
        and csda_version.year == tag.year
        and csda_version.pi == tag.pi
        and csda_version.sprint == tag.sprint
    ):
        tag.release += 1
        return tag.to_str()
    else:
        return Tag(
            year=csda_version.year,
            pi=csda_version.pi,
            sprint=csda_version.sprint,
            release=0,
        ).to_str()


def get_next_csda_version(date: str, csda_version_str: str) -> str:
    """Returns the next CSDA version."""
    date_parts = date.split("-")

    year = int(date_parts[0])
    month = int(date_parts[1])
    if month <= 3:
        pi = 2
    elif month <= 6:
        pi = 3
    elif month <= 9:
        pi = 4
    else:
        pi = 1
    if pi == 1:
        year += 1

    csda_version = CsdaVersion.parse(csda_version_str)
    if year != csda_version.year:
        csda_version.year = year
        csda_version.pi = 1
        csda_version.sprint = 0
    elif pi != csda_version.pi:
        csda_version.pi = pi
        csda_version.sprint = 0
    else:
        csda_version.sprint += 1
    return csda_version.to_str()


@click.group()
def cli() -> None:
    """Calculate CSDA versions."""
    pass


@cli.command("next-version")
@click.argument("csda_version")
@click.argument("tag")
@click.option(
    "--github-output",
    is_flag=True,
    help="Write output to GITHUB_OUTPUT environment variable",
)
def next_version_cmd(csda_version: str, tag: str, github_output: bool) -> None:
    """Calculate the next version based on CSDA_VERSION and TAG."""
    version = get_next_version(csda_version, tag)
    if github_output:
        github_output_path = os.environ.get("GITHUB_OUTPUT")
        if github_output_path:
            with open(github_output_path, "a") as f:
                f.write(f"version={version}\n")
        else:
            raise click.ClickException("GITHUB_OUTPUT environment variable not set")
    else:
        click.echo(version)


@cli.command("next-csda-version")
@click.argument("date")
@click.argument("csda_version")
def next_csda_version_cmd(date: str, csda_version: str) -> None:
    """Calculate the next CSDA version based on DATE and CSDA_VERSION."""
    version = get_next_csda_version(date, csda_version)
    click.echo(version)


if __name__ == "__main__":
    cli()
