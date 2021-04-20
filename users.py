import database
import datetime
from geosky import geo_plug
import json
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import datetime

country = (geo_plug.all_Country_StateNames())
countries = json.loads(country)
new_countries = {}


class Users(object):
    def __init__(self, first_name, last_name, email, password, country, state_province, date, _id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.country = country
        self.state_province = state_province
        self.date = date
        self._id = _id
        self.image = None

    def signup(self):
        # database.create_table()
        database.insert_into_user_table(self.first_name, self.last_name, self.email, self.password, self.country,
                                        self.state_province, self._id, self.date, self.image)
        return True

    @staticmethod
    def get_countries():
        country_list = []
        for i in countries:
            for countryy, capital in i.items():
                country_list.append(countryy)
        return country_list

    @staticmethod
    def check_user(email):
        return database.get_user(email)

    @staticmethod
    def ret_country():
        for count in countries:
            new_countries.update(count)
        return new_countries

    @staticmethod
    def get_city_time(captital):
        geolocator = Nominatim(user_agent='Thomas')
        location = geolocator.geocode(captital)
        tf = TimezoneFinder()
        time_zone = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        tz = pytz.timezone(time_zone)
        new_town = datetime.datetime.now(tz)
        current_time = new_town.strftime("%H:%M:%S")
        return current_time

    @staticmethod
    def user_image(image, email):
        database.update_image(image, email)
        return True

# date = datetime.datetime.now()
# pop = Users("James", "Ebere", "opop@gmail.com", "prick", "Nigeria", "Lagos", date, "9000")
# print(pop.check_user('deji@gmail.com'))
# if pop.check_user('jpkere@gmail.comn'):
#     print("Yes")
# else:
#     print('No')
# pop.status()
