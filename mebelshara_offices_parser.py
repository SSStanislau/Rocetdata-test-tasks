import requests
import json
from bs4 import BeautifulSoup
import re


MEBELSHARA_URL = 'https://www.mebelshara.ru/contacts'


def parse_working_days(days):
    if re.match(r'.+:$', days):
        return days[:-1]
    return re.sub(r':\s', ' ', days)


def parse():
    response = requests.get(MEBELSHARA_URL).content
    soup = BeautifulSoup(response, 'html.parser')
    divs = soup.findAll("div", {"class": "expand-block top-border"})
    parsed_data = []
    for div in divs:
        city = div.findAll("h4", {"class": "js-city-name"})[0].text
        shops = div.findAll("div", {"class": "shop-list-item"})
        for shop in shops:
            address = f"{city}, {shop.attrs['data-shop-address']}"
            latlon = [float(shop.attrs['data-shop-latitude']), float(shop.attrs['data-shop-longitude'])]
            name = shop.attrs['data-shop-name']
            phone = [shop.attrs['data-shop-phone']]
            working_days = [parse_working_days(shop.attrs['data-shop-mode1']),
                            parse_working_days(shop.attrs['data-shop-mode2'])]
            parsed_data.append(
                {
                    'address': address,
                    'latlon': latlon,
                    'name': name,
                    'phones': phone,
                    'working_hours': working_days
                }
            )
    return parsed_data


def export_json(parsed_data):
    with open("mebelshara_contacts.json", "x") as write_file:
        json.dump(parsed_data, write_file, ensure_ascii=False)


def main():
    parsed_data = parse()
    export_json(parsed_data)


if __name__ == "__main__":
    main()
