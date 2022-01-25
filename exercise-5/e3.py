def load(path):
    import importlib, os

    # Use the filename as the module name.
    modname = os.path.basename(path).split('.')[0]
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
