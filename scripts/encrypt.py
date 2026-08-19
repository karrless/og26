#!/usr/bin/env python3
import argparse
import getpass
import sys

import bcrypt


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Хэширует пароль с помощью bcrypt"
    )

    parser.add_argument(
        "-p",
        "--password",
        help="Пароль для хэширования. Если не указать, скрипт спросит безопасно.",
    )

    parser.add_argument(
        "-r",
        "--rounds",
        type=int,
        default=12,
        help="Cost factor для bcrypt, по умолчанию 12",
    )

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    password = args.password

    if password is None:
        password = getpass.getpass("Введите пароль: ")

    if not password:
        print("Пароль пустой", file=sys.stderr)
        return 1

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=args.rounds),
    )

    print(hashed.decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())