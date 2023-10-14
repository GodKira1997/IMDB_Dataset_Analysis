"""
file: setup.py
description: TThis program installs all the packages required for the main
program
language: python3
author: Anurag Kallurwar, ak6491@rit.edu
"""


import pip


def install_and_import_packages(package: str):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        return __import__(package)


configparser = install_and_import_packages('configparser')
psycopg2 = install_and_import_packages('psycopg2')
extras = install_and_import_packages('psycopg2.extras')
numpy = install_and_import_packages('numpy')
pandas = install_and_import_packages('pandas')
pymongo = install_and_import_packages('pymongo')
