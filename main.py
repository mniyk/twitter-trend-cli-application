"""メイン処理
"""
import argparse
import configparser

import tweepy


def get_country(api, woeid: int=None, country_name: str=None):
    response = api.available_trends()

    country = {}
    
    for row in response:
        if row['placeType']['name'] == 'Country':
            if woeid is None and country_name is None:
                country.setdefault(row['woeid'], row['name'])
            elif woeid is not None and row['woeid'] == woeid:
                country.setdefault(row['woeid'], row['name'])
            elif country_name is not None and row['country'] == country_name:
                country.setdefault(row['woeid'], row['name'])                

    return country


def get_city(api, woeid: int=None, country_name: str=None, city_name: str=None):
    response = api.available_trends()

    city = {}
    
    for row in response:
        if row['placeType']['name'] == 'Town':
            if woeid is None and country_name is None and city_name is None:
                city.setdefault(row['woeid'], row['name'])
            elif woeid is not None and row['woeid'] == woeid:
                city.setdefault(row['woeid'], row['name'])
            elif country_name is not None and row['country'] == country_name:
                city.setdefault(row['woeid'], row['name'])
            elif city_name is not None and row['name'] == city_name:
                city.setdefault(row['woeid'], row['name'])
    
    return city


def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    api_key = config.get('TWITTER', 'API_KEY') 
    api_key_secret = config.get('TWITTER', 'API_KEY_SECRET')
    access_token = config.get('TWITTER', 'ACCESS_TOKEN')
    access_token_secret = config.get('TWITTER', 'ACCESS_TOKEN_SECRET')

    parser = argparse.ArgumentParser()
    parser.add_argument('--trend', action='store_true')
    parser.add_argument('--country', action='store_true')
    parser.add_argument('--city', action='store_true')
    parser.add_argument('-w', '--woeid')
    parser.add_argument('--country_name')
    parser.add_argument('--city_name')

    args = parser.parse_args()

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if args.trend:
        if args.woeid:
            response = api.get_place_trends(int(args.woeid))

            country = get_country(api, woeid=int(args.woeid))

            if country:
                print(f'TREND COUNTRY: {country[int(args.woeid)]}')
            else:
                city = get_city(api, woeid=int(args.woeid))

                print(f'TREND CITY: {city[int(args.woeid)]}')

            for i, data in enumerate(response[0]['trends'], start=1):
                print(f'{i:<2} ->')
                print(f'{"":<4}TITLE : {data["name"]}')
                print(f'{"":<4}URL   : {data["url"]}')
                print(f'{"":<4}VOLUME: {data["tweet_volume"]}')
    elif args.country:
        if args.woeid:
            country = get_country(api, woeid=int(args.woeid))
        elif args.country_name:
            country = get_country(api, country_name=args.country_name)
        else:
            country = get_country(api)

        for k, v in country.items():
            print(f'WOEID: {k} NAME: {v}')
    elif args.city:
        if args.woeid:
            city = get_city(api, woeid=int(args.woeid))
        elif args.country_name:
            city = get_city(api, country_name=args.country_name)
        elif args.city_name:
            city = get_city(api, city_name=args.city_name)
        else:
            city = get_city(api)
        
        for k, v in city.items():
            print(f'WOEID: {k} NAME: {v}')


if __name__ == '__main__':
    main()
