import asyncio
import datetime
import logging
import re
import time
from functools import wraps
from types import GenericAlias
from typing import List, Optional, Type, Union

from fastapi import Query
from pydantic import TypeAdapter, BaseModel


def parse_list(query: Query, class_type: Type):
    def inner_parse(elements: List[str] = query) -> Optional[List[class_type]]:
        def remove_prefix(text: str, prefix: str):
            return text[text.startswith(prefix) and len(prefix):]

        def remove_postfix(text: str, postfix: str):
            if text.endswith(postfix):
                text = text[: -len(postfix)]
            return text

        if query.default != Ellipsis and not elements:
            return query.default

        if len(elements) > 1:
            elements_list = elements
        else:
            flat_elements = elements[0]
            if flat_elements.startswith("["):
                flat_elements = remove_prefix(flat_elements, "[")

            if flat_elements.endswith("]"):
                flat_elements = remove_postfix(flat_elements, "]")

            if query.default != Ellipsis and not flat_elements:
                return query.default

            elements_list = flat_elements.split(",")
            elements_list = [remove_prefix(n.strip(), '"') for n in elements_list]
            elements_list = [remove_postfix(n.strip(), '"') for n in elements_list]

        errors = {}
        results = []
        for idx, el in enumerate(elements_list):
            try:
                results.append(class_type(el))
            except ValueError as e:
                errors[idx] = repr(e)
        if errors:
            raise Exception(f"Could not parse elements: {errors}")
        else:
            return results

    return inner_parse


def replace_special_character(string: str) -> Union[str, None]:
    if string is not None:
        return string.replace("&", "&amp;").replace("<", "").replace(">", "")
    else:
        return string


def clean_xml_criterion(data, max_len=None):
    if data is None:
        return ""
    elif isinstance(data, str):
        data = data.replace("&", "&amp;").replace("<", "").replace(">", "")
        return data if max_len is None else data[:max_len]
    else:
        return data


def is_valid_json(json_data):
    try:
        import json

        json.loads(json_data)
    except ValueError:
        return False
    return True


def parse_int(string: str):
    if string:
        return int(string.strip())
    else:
        return None


def get_duration(function):
    """
    Use this annotation if you want to know how long does the function take
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.debug(f'START {function.__name__} - {locals()}')
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        logging.debug(f'END {function.__name__} - {((end - start) * 1000):.2f} ms')
        return result

    return wrapper


def transform_string(string: str):
    caracteres_speciaux = ["é", "è", "ê", "à", "â", "ô", "ù", "û", "ç", "ñ"]
    remplacements = ["e", "e", "e", "a", "a", "o", "u", "u", "c", "n"]
    for i in range(len(caracteres_speciaux)):
        string = string.replace(caracteres_speciaux[i], remplacements[i])
        string = string.replace(caracteres_speciaux[i].upper(), remplacements[i].upper())
    return string.replace(" ", "+")


def get_request_timestamp():
    return datetime.datetime.now(tz=datetime.timezone.utc).isoformat(sep='T', timespec='milliseconds').replace('+00:00', 'Z')


def gen_all_context_ids(address_correction_request_list, additional_packages: List[dict]) -> str:
    lst_elem = []
    for acr in address_correction_request_list:
        if acr.parcel_id and acr.unique_id:
            additional_packages.append({'tracking_id': acr.parcel_id, 'unique_id': acr.unique_id})

    for package in list({v['tracking_id']: v for v in additional_packages}.values()):
        lst_elem.append(f'<ns0:contextId>' f'{package["tracking_id"]},{package["unique_id"]}' f'</ns0:contextId>')

    return """
  """.join(
        lst_elem
    )


def get_datetime_isoformat(my_datetime, timespec='milliseconds', withZ=True):
    """

    :param my_datetime:
    :param timespec:
    :return:
    """
    my_isofrm = my_datetime.isoformat(sep='T', timespec=timespec)

    if my_datetime.tzinfo.utcoffset(my_datetime) == datetime.timedelta(0) and withZ:
        my_isofrm = my_isofrm.replace('+00:00', 'Z')

    return my_isofrm


def check_keys_existing(data: dict) -> bool:
    if 'lat' in data or 'lng' in data:
        return True
    else:
        return False


def get_start_row(data):
    start_row = 2

    if 'lat' in data:
        start_row += len(data['lat'])

    return start_row


def get_address_line_cleaned(data, index):
    address_line = (
        f"{data['Company'][index]}+"
        f"{data['Line 1'][index]}+"
        f"{data['Line 2'][index]}+"
        f"{data['City'][index]}+"
        f"{data['Postal Code'][index]}+"
        f"{data['Country'][index]}"
    )

    return re.sub("#|/|&", " ", address_line.replace('?', ' '))


def get_item_from_list_if_exist(list_to_look, index, dict_value):
    try:
        return list_to_look[index][dict_value]
    except IndexError:
        return ""


def calculate_distance(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float):
    from math import sin, cos, sqrt, atan2, radians
    # Approximate radius of earth in km
    R = 6373.0
    try:
        lat1 = radians(latitude_1)
        lon1 = radians(longitude_1)
        lat2 = radians(latitude_2)
        lon2 = radians(longitude_2)
    except TypeError as e:
        return -1
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    # In km
    return distance


def xpath_get(mydict, path, default=None):
    elem = mydict
    try:
        for x in path.strip('/').split('/'):
            if isinstance(elem, (tuple, list)):
                index = int(x)
                if index < len(elem):
                    elem = elem[index]
                else:
                    elem = default
            else:
                elem = elem.get(x, default)
    except Exception:
        logging.debug('unable to find key in %s ' % path)

    return elem


def get_xpath_with_dicts_format(mydict, path, default=None):
    data = xpath_get(mydict, path, default)
    result = {}
    for val in data:
        result[val['Name']] = val['Value']

    return result


def mock_return_value(return_value, return_type, condition: bool = False):
    """
    A decorator that wraps a function and mocks its return value.

    Parameters:
    - return_value: The value that the mocked function should return.

    Returns:
    - Decorator function.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not condition:
                return await func(*args, **kwargs)
            if issubclass(type(return_type), GenericAlias):
                return return_value
            if issubclass(return_type, BaseModel):
                return TypeAdapter(return_type).validate_python(return_value)
            return return_value

        return wrapper

    return decorator


def remove_item_from_list(base_list, list_to_remove):
    for item in list_to_remove:
        base_list.remove(item)
    return base_list


def sync(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
            raise ex

    return wrapper


if __name__ == '__main__':
    # print(transform_string('28 avenue édouard miçelin'))
    file_path = 'C:/Users/920995/OneDrive - MyFedEx/Documents/AGC/providers/google_api_no_result.xlsx'
