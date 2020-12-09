from datetime import date
import calendar
from typing import List


def get_day_from_date(date_input: date) -> str:
    day, month, year = [int(i) for i in date_input.strftime("%d/%m/%Y").split('/')]
    new_date = date(year=year, month=month, day=day)
    return new_date.strftime("%A") 

def get_month_from_date(date_input: date) -> str:
    day, month, year = [int(i) for i in date_input.strftime("%d/%m/%Y").split('/')]
    new_date = date(year=year, month=month, day=day)
    return calendar.month_name[new_date.month]

def log(log_title: str, log_content: str) -> None:
    print(f'[{log_title.upper()}]: {log_content}')

def remove_all(string: str, substrings: List[str]) -> str:
    for substring in substrings:
        string = string.replace(substring, '')
    return string

def sort_dict_by_value(dictionary: dict) -> dict:
    sorted_dict = {}
    sorted_values = list(dictionary.values())
    sorted_values.sort(reverse=True)
    dictionary_keys = list(dictionary.keys())

    for i in range(0, len(sorted_values)):
        for key in dictionary_keys:
            if dictionary.get(key) == sorted_values[i]:
                sorted_dict[key] = sorted_values[i]
    return sorted_dict


    
    





