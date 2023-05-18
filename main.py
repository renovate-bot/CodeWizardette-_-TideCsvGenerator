import csv
from datetime import datetime, timedelta
import math
import pytz


cities = {
    'Istanbul': (41.0082, 28.9784),
    'Izmir': (38.4237, 27.1428),
    'Antalya': (36.8969, 30.7133),
    'Mersin': (36.8000, 34.6333),
    'Samsun': (41.2866, 36.3306),
    'Trabzon': (40.9948, 39.7849),
    'Sinop': (42.0226, 35.1531),
    'Bodrum': (37.0343, 27.4305),
    'Fethiye': (36.6212, 29.1162),
    'Kuşadası': (37.8575, 27.2619),
    'Alanya': (36.5445, 32.0055),
    'Sile': (41.1754, 29.6134),
    'Amasra': (41.7466, 32.3864),
    'Giresun': (40.9128, 38.3895),
    'Ordu': (40.9863, 37.8797),
    'Rize': (41.0201, 40.5234),
    'Gümüşhane': (40.4608, 39.4813),
    'Hop': (40.8588, 42.1411),
    'Bartın': (41.6357, 32.3378),
    'Zonguldak': (41.4557, 31.7896)
}

def high_tide_time(day, latitude):
    moon_longitude = 198.4454 + 13.176396 * day
    moon_mean_anomaly = 134.9634 + 13.064993 * day
    moon_evection = 1.2739 * math.sin(math.radians(2 * (moon_longitude - math.radians(latitude))))
    moon_variation = 0.6583 * math.sin(math.radians(2 * moon_longitude))
    moon_long_corr = moon_evection + moon_variation
    moon_ascension = 13.064993 * day + 280.461 + moon_long_corr
    moon_declination = math.degrees(math.asin(math.sin(math.radians(moon_ascension)) * math.sin(math.radians(5.1454))))
    local_hour_angle = math.degrees(math.acos((math.sin(math.radians(-.583))) - math.sin(math.radians(latitude)) * math.sin(math.radians(moon_declination))) / (math.cos(math.radians(latitude)) * math.cos(math.radians(moon_declination))))
    return (datetime(day.year, day.month, day.day, 0, 0, 0) + timedelta(hours=local_hour_angle / 15)).astimezone(pytz.UTC)

start_date = datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

end_date = datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

header = ['Date', 'City', 'Latitude', 'Longitude', 'Tide Height', 'Tide Type']

with open('tides.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    current_date = start_date
    while current_date <= end_date:
        for city, coords in cities.items():
            high_tide = high_tide_time(current_date, coords[0])
            prediction = predict_tide(coords[0], coords[1], current_date)
            tide = prediction['tide']
            tide_type = prediction['type']
            if current_date <= high_tide + timedelta(hours=1) and current_date >= high_tide - timedelta(hours=1):
                tidecurrent_date += timedelta(days=1)

print('Veriler başarıyla kaydedildi.')

