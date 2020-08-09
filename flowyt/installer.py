import sys
import os
from pathlib import Path


from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = {
    "packages": ["os", "sys"],
    "excludes": [],
    "includes": [],
    "build_exe": "build/flowyt",
}

if sys.platform == "darwin":  # macOS
    buildOptions["includes"] += ["_sysconfigdata__darwin_darwin", "pkg_resources.py2_warn"]

base = "Console"

executables = [
    Executable("cli.py", base=base, targetName="app"),
    Executable("wsgi.py", base=base, targetName="wsgi"),
    Executable("cli.py", base=base, targetName="cli")
]

###############
# CLI
###############

version = input("Enter build version: ")
print("")
print("")
print("===================================")
print("Generating the version {0}".format(version))
print("===================================")

setup(
    name="Flowyt",
    version=version,
    description="",
    options=dict(build_exe=buildOptions),
    executables=executables,
)
