def get_dependencies():
    path = '/Users/david/lib/dependable/sample2/__init__.py'
    from modulegraph.modulegraph import ModuleGraph
    gr = ModuleGraph()
    node = gr.run_script(path)
    gr.run_script('/Users/david/lib/dependable/sample2/foo.py')

    print(list(gr.getReferences(node)))

    #modules = read_project(path)
    #import pprint
    #pprint.pprint(modules)
    return []


def print_tree(node, depth=0):
    print(' ' * depth + '-' + node.full_path)
    for child in node.imports:
        print_tree(child, depth + 1)


import ast
import os



def read_project(root_path):
    modules = {}
    ignore_files = set([".hg", ".svn", ".git", ".tox", "__pycache__", "env", "venv"]) # python 2.6 comp

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ignore_files]

        files = [fn for fn in files if os.path.splitext(fn)[1] == ".py" and fn not in ignore_files]

        for file_name in files:
            full_path = os.path.join(root, file_name)
            print('Reading {}'.format(full_path))
            with open(full_path, "r") as f:
                file_data = f.read()
                tree = ast.parse(file_data)
                modules[full_path] = [i for i in list_import_names(tree)]
                continue
    return modules


def get_descendants(node):
    nodes = []
    for node in ast.iter_child_nodes(node):
        nodes.append(node)
        nodes.extend(get_descendants(node))
    return nodes


def list_import_names(tree):
    for node in get_descendants(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                yield name.name
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                yield '.' * node.level + (node.module + '.' if node.module else '') + name.name
        else:
            continue