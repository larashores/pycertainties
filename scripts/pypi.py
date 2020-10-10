import os
import shutil
import subprocess
from typing import Optional

import click


@click.option(
    "--token", help="Optionally authenticate with a PyPi API token. Otherwise prompt for username/password on stdin"
)
@click.command()
def pypy(token: Optional[str]):
    """
    Command used to build and upload the project to PyPi in a single step.

    Either run `python scripts/pypy.py` and type in your username/password in stdin, or run `python scripts/pypy.py
    --token pypi-token`, substituting in a valid PyPi API token for your account.
    """
    upload_command = "twine upload dist/*"
    if token is not None:
        upload_command += f" --username __token__ --password {token}"

    try:
        for command in (
            "python setup.py sdist",
            "python setup.py bdist_wheel --python-tag py38",
            "twine check dist/*",
            upload_command,
        ):
            print(command)
            subprocess.run(command.split(" "), check=True)
            print()
    finally:
        # Cleanup
        for path in "build", "dist", os.path.join("src", "pycertainties.egg-info"):
            if os.path.exists(path):
                shutil.rmtree(path)


if __name__ == "__main__":
    pypy()  # pylint: disable=no-value-for-parameter
