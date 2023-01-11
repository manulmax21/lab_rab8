#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys


def add_shop(list_race, name, namber, time):
    """
    Добавить данные магазина.
    """
    list_race.append(
        {
            "name": name,
            "namber": namber,
            "time": time
        }
    )
    return list_race


def display_shop(list_race):
    """
    Отобразить список.
    """
    if list_race:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 6,
            '-' * 20,
            '-' * 30,
            '-' * 20
        )
        print(line)
        print(
            '| {:^6} | {:^20} | {:^30} | {:^20} |'.format(
                "No",
                "пункт назначения",
                "номер",
                "время"
            )
        )
        print(line)
        for idx, listrace in enumerate(list_race, 1):
            print(
                '| {:>6} | {:<20} | {:<30} | {:>20} |'.format(
                    idx,
                    listrace.get('name', ''),
                    listrace.get('namber', ''),
                    listrace.get('time', '')
                )
            )
        print(line)
    else:
        print("Список рейсов пуст.")


def select_product(list_race, race_sear):
    """
    Выбрать.
    """
    search_race = []
    for race_sear_itme in list_race:
        if race_sear == race_sear_itme['name']:
            search_race.append(race_sear_itme)
    return search_race


def save_race(file_name, list_race):
    """
    Сохранить все в JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(list_race, fout, ensure_ascii=False, indent=4)


def load_list_race(file_name):
    """
    Загрузить все из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )
    parser = argparse.ArgumentParser("races")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new race"
    )
    add.add_argument(
        "-nm",
        "--name",
        action="store",
        required=True,
        help="The race's name"
    )
    add.add_argument(
        "-nb",
        "--namber",
        action="store",
        help="The namber"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        type=int,
        required=True,
        help="time"
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all races"
    )
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the product"
    )
    select.add_argument(
        "-SS",
        "--name_sear",
        action="store",
        type=str,
        required=True,
        help="The name race"
    )
    args = parser.parse_args(command_line)
    
    # Получить имя файла.
    data_file = args.data
    if not data_file:
        data_file = os.environ.get("RACES_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)
    
    is_dirty = False
    if os.path.exists(args.filename):
        race = load_list_race(args.filename)
    else:
        race = []
    if args.command == "add":
        race = add_shop(
            race,
            args.name,
            args.namber,
            args.time
        )
        is_dirty = True
    elif args.command == "display":
        display_shop(race)

    elif args.command == "select":
        selected = select_product(race, args.race_sear)
        display_shop(selected)
    if is_dirty:
        save_race(args.filename, race)


if __name__ == '__main__':
    main()