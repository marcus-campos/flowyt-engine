from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = {
    "packages": ["os", "sys"], 
    "excludes": [], 
    "includes": ["_sysconfigdata__darwin_darwin", "pkg_resources.py2_warn"],
    "build_exe": "build/orchestryzi"   
}

base = 'Console'

executables = [
    Executable('app.py', base=base)
]

setup(name='Orchestryzi',
      version = 'v0.1.2',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
