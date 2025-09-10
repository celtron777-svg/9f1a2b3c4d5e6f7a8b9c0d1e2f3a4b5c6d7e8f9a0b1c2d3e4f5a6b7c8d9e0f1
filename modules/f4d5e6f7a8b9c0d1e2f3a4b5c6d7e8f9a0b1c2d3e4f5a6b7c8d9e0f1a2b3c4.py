import os, glob, importlib.util
module_dir = '/vgu/modules/'
for path in sorted(glob.glob(os.path.join(module_dir, '*.py'))):
    if '__autoload__.py' in path: continue
    spec = importlib.util.spec_from_file_location('', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)