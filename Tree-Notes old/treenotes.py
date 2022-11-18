#!/bin/python3
import commands
import utils

current = utils.Note(name="Root")
links = {}
commands.current = current
commands.links = links


def main():
    from sys import argv
    # TODO support for multiple commands
    if len(argv) > 1:
        cmd = argv[1:]
        func = cmd[0]
        args = cmd[1:]
        print(f"Executing ", *cmd, "...")

        execute(func, args)

    print("Wellcome To Tree-Notes, For help, type \"help\"")
    while True:
        cmd = input(">>>: ").split()
        if cmd:
            func = cmd[0]
            args = cmd[1:]
            execute(func, args)
        else:
            continue


def execute(func, args):
    for f in commands.functions:
        if f.__name__ == func:
            f(*args)
            break
    else:
        print("invalid command")


main()
