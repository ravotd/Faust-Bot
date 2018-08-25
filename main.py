#!/bin/python

"""
mainfile, initializes everything
"""

# function declarations
from argparse import ArgumentParser

from faustbot.faustbot import FaustBot

if __name__ == "__main__":
    arg_parser = ArgumentParser(description="FautBot - ")
    arg_parser.add_argument('--config', required=True, type=str, help="Path to the configuration file")
    arg_parser.add_argument('--debug', required=False, type=bool, help="Wether debugging log should be enabled or not")
    args = arg_parser.parse_args()
    bot = FaustBot(args.config, args.debug)
    bot.run()
