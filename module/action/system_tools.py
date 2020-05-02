try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain
import pkg_resources
from packaging.version import parse

required_packages = {"pygame": "0.0.0",
                     "numpy": "0.0.0",
                     "sympy": "0.0.0"}


def install(package):
    pipmain(['install', package])


def get_installed_packages() -> dict:
    return {str(p).split()[0]: str(p).split()[1] for p in pkg_resources.working_set}


def install_required_packages():
    global required_packages
    installed_packages = get_installed_packages()
    for package in required_packages.keys():
        if not(package in installed_packages) or \
                parse(required_packages[package]) > parse(installed_packages[package]):
            install(package)
