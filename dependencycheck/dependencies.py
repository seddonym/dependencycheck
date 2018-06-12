from pydeps.py2depgraph import py2dep


def get_dependencies():
    deps = py2dep('sample',
                 verbose=0,
                 show_cycles=False,
                 show_raw_deps=False,
                 noise_level=200,
                 max_bacon=200,
                 show_deps=False)
    return []
