import importlib.util
import os
from pathlib import Path

import js2py

from engine.settings import WORKSPACES_PATH


class FunctionLoader(object):
    base_model = {
        "config": {},
        "flows": {},
        "functions": {},
        "routes": []
    }

    def load_string(self, modules, language):
        functions = {}
        for module in modules:
            context = None
            if language == "python":
                context = self._load_py(module["data"])
            elif language == "javascript":
                context = self._load_py(module["data"])

            functions[module["name"]] = context
            
        return functions

    def load_local(self, workspace):
        workspace_path = "{0}/{1}".format(WORKSPACES_PATH, workspace)
        
        functions_path = "{0}/functions".format(workspace_path)
        functions = {}

        for module in os.listdir(functions_path):
            module_path = Path(module)

            if module_path.name == "__init__.py" or not module_path.suffix == ".py":
                continue

            spec = importlib.util.spec_from_file_location(
                "module.name", functions_path + "/{0}".format(module)
            )
            module_loaded = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_loaded)
            functions[module_path.stem] = module_loaded

        return functions

    def _load_py(self, text):
        context = {}
        exec(text, context)
        return context

    def _load_js(self, text):
        context = js2py.EvalJs(enable_require=False)
        context.execute(text)
        return context
