import os
import shutil
import subprocess
from typing import Optional

import click


@click.option("--token")
@click.command()
def pypy(token: Optional[str]):
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
        for path in "build", "dist", os.path.join("src", "uncertainties.egg-info"):
            if os.path.exists(path):
                shutil.rmtree(path)


if __name__ == "__main__":
    pypy()  # pylint: disable=no-value-for-parameter
