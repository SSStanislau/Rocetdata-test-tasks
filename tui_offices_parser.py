import json
import requests
import re


URL = 'https://apigate.tui.ru/api/office/list'
PARAMS = {
    'cityId': 1,
    'subwayId': '',
    'hoursFrom': '',
    'hoursTo': '',
    'serviceIds': 'all',
    'toBeOpenOnHolidays': 'false'
}


def is_weekend(day):
    if day['isDayOff']:
        return 'выходной'
    return f"{day['startStr']}-{day['endStr']}"


def remove_zip_code(address):
    return re.sub(r'^\d+,\s', '', address)


def parse_workdays(workdays: dict):
    working_hours = []
    weekdays = f"пн-пт {workdays['workdays']['startStr']} до {workdays['workdays']['endStr']}"
    working_hours.append(weekdays)
    saturday = is_weekend(workdays['saturday'])
    sunday = is_weekend(workdays['sunday'])
    if saturday == sunday:
        working_hours.append(f"сб-вс {saturday}")
    else:
        working_hours.extend([f"сб {saturday}", f"вс {sunday}"])
    return working_hours


def parse():
    response = requests.get(URL, PARAMS)
    offices = json.loads(response.text)['offices']
    parsed_data = []
    for office in offices:
        name = office['name']
        latlon = [office['latitude'], office['longitude']]
        address = remove_zip_code(office['address'])
        phones = office['phone'].split('; ')
        workdays = parse_workdays(office['hoursOfOperation'])
        parsed_data.append(
            {
                "address": address,
                "latlon": latlon,
                "name": name,
                "phones": phones,
                "working_hours": workdays
            }
        )
    return parsed_data


def export_json(parsed_data):
    with open("tui_offices.json", "x") as write_file:
        json.dump(parsed_data, write_file, ensure_ascii=False)


def main():
    parsed_data = parse()
    export_json(parsed_data)


if __name__ == "__main__":
    main()




