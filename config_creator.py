#! /bin/python
import json


def load_existing(path: str):
    try:
        cfg = json.load(open(path, 'r'))
    except FileNotFoundError as e:
        print("[!!! ERROR] Config file could not be found, please check the path.\n" + path)
        return None
    return cfg


def store_config(path: str):
    try:
        pass
    except FileNotFoundError as e:
        pass


if __name__ == '__main__':
    pass
