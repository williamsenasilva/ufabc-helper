import pip
import os
from sys import platform

all_packages = open("requirements.txt", "r")
all_packages = all_packages.read().splitlines()


if not os.environ.get('LOCALHOST_MYSQL_DB_URL'):
    for package in all_packages:
        if 'mysqlclient' in package:
            all_packages.remove(package)


windows = []
linux = []
darwin = []


def install(packages):
    for package in packages:
        pip.main(['install', package])


if __name__ == '__main__':
    install(all_packages)

    if platform == 'windows':
        install(windows)
    elif platform.startswith('linux'):
        install(linux)
    elif platform == 'darwin':  # MacOS
        install(darwin)
