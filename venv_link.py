# symlink a system package or module into the current virtual env

import imp
import os
import sys
import sysconfig
import site


def install_link(name):
    """'Install' a module or package by linking to system version"""
    
    virt_prefix = sys.prefix
    real_prefix = getattr(sys, "real_prefix", None)
    if real_prefix is None or real_prefix == virt_prefix:
        raise Exception("Not in a virtual environment")

    lib_names = 'purelib', 'platlib'
    virt_libs = tuple(map(sysconfig.get_path, lib_names))
    real_libs = tuple(d.replace(virt_prefix, real_prefix) for d in virt_libs)

    # We want to see what the system Python would import...
    saved_path = sys.path[:]
    sys.path[:] = (d for d in saved_path if not d.startswith(virt_libs))
    for d in real_libs:
        site.addsitedir(d)
    try:
        f, real_path, info = imp.find_module(name)
    finally:
        sys.path[:] = saved_path

    if f is not None:
        f.close()

    link_path = real_path
    for virtd, reald in zip(virt_libs, real_libs):
        link_path = link_path.replace(reald, virtd)

    print "{} -> {}".format(link_path, real_path)
    os.symlink(real_path, link_path)
    

    # I spy with my little eye a use case for the import engine PEP...
    # http://mail.python.org/pipermail/import-sig/2011-July/000318.html
    # Although, in reality, pip would likely do all this at a higher level
    # using the distribution metadata store, rather than at the import
    # namespace level the way I am doing it here.


if __name__ == "__main__":
    install_link(sys.argv[1])
