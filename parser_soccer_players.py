import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from pandas import DataFrame

ua = UserAgent()
headers = {
    'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.7',
    'user-agent': ua.random
}


def main():
    df = pd.read_csv('data_blank.csv', encoding='utf-8')
    names = list(df['Aaron Cresswell'])
    names_df = ['Aaron Cresswell']
    positions_df = ['LB']
    clubs_df = ['West Ham United']
    ages_df = ['33']
    nats_df = ['England']
    values_df = ['3.00m']  # All this data is already filled into the sheet, so I can use it as a start point for all lists that will contain similar data
    counter = 0

    for name in names:
        print(f'Итерация {counter}')
        counter += 1
        url_no_name = 'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query='
        req = requests.get(url=(url_no_name + f'{name.replace(" ", "+")}'), headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        if soup.find_all('td', class_='zentriert')[0:4] and soup.find('td', class_='rechts hauptlink'):
            pos_club_age_nat = soup.find_all('td', class_='zentriert')[0:4]  # Getting slice here is obviously not the best decision, but it still works, so... Who cares?
            value = soup.find('td', class_='rechts hauptlink')

            try:  # In order to create a DataFrame object, not a single field must be empty, so everything is wrapped into try-except blocks
                names_df.append(name)
            except Exception or not name:
                names_df.append('Имя неизвестно')

            try:
                values_df.append(value.text.strip('€'))
            except Exception or not value.text.strip('€'):
                values_df.append('Стоимость неизвестна')

            for thing in range(len(pos_club_age_nat)):
                if thing == 0:
                    try:
                        positions_df.append(pos_club_age_nat[thing].text)
                        print(pos_club_age_nat[thing].text)
                    except Exception or not pos_club_age_nat[thing].text:
                        positions_df.append('Позиция неизвестна')

                elif thing == 1:
                    try:
                        club = pos_club_age_nat[thing].find('a').get('title')
                        clubs_df.append(club)
                        print(club)
                    except Exception or not pos_club_age_nat[thing].find('a').get('title'):
                        clubs_df.append('Клуба нет')

                elif thing == 2:
                    try:
                        ages_df.append(pos_club_age_nat[thing].text)
                        print(pos_club_age_nat[thing].text)
                    except Exception or not pos_club_age_nat[thing].text:
                        ages_df.append('Возраст неизвестен')

                elif thing == 3:  # All these elif-s are whispering me that I am a bad programmer...
                    try:
                        nat = pos_club_age_nat[thing].find('img').get('title')
                        nats_df.append(nat)
                    except Exception or not pos_club_age_nat[thing].find('img').get('title'):
                        nats_df.append('Национальность неизвестна')

        else:  # In case if not a single piece of info is found
            names_df.append(name)
            ages_df.append('Информация про игрока не найдена')
            positions_df.append('Информация про игрока не найдена')
            clubs_df.append('Информация про игрока не найдена')
            nats_df.append('Информация про игрока не найдена')
            values_df.append('Информация про игрока не найдена')

    data = {
        'Names': names_df,
        'Ages': ages_df,
        'Positions': positions_df,
        'Clubs': clubs_df,
        'Nationalities': nats_df,
        'Values, €': values_df
    }
    dataframe = DataFrame(data=data)
    csv_file = dataframe.to_csv('data_filled.csv')
    print(csv_file)  # Unnecessary conclusion


if __name__ == '__main__':
    main()
