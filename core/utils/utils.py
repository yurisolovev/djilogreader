import os
import subprocess
import uuid
import datetime
import shutil
import fnmatch
import csv

from .generate_kml import generate_kml
from .generate_gpx import generate_gpx


#
# ------------------------------ Classes -------------------------------------
#
class DjiLogParser:
    """ Extract csv, *.jpg files (if they are in a log) with 'djiparsetxt' application,
        generate KML and GPX from *.csv and save results into db.
    """
    def __init__(self, instance, parser='djiparsetxt', log_path='', csv_path='', kml_path='', gpx_path=''):
        self.log = instance
        self.log_path = log_path or instance.log_file.path
        self.csv_path = csv_path or instance.log_file.path.replace('.txt', '.csv')
        self.kml_path = kml_path or instance.log_file.path.replace('.txt', '.kml')
        self.gpx_path = gpx_path or instance.log_file.path.replace('.txt', '.gpx')
        self.log_directory = os.path.dirname(instance.log_file.path)
        self.cwd = os.path.dirname(instance.log_file.path)
        self.log_parser = parser

    def create_csv(self):
        command = '{} {} > {}'.format(self.log_parser, self.log_path, self.csv_path)
        try:
            subprocess.run(command, cwd=self.cwd, shell=True, check=True)
        except subprocess.CalledProcessError:
            shutil.rmtree(self.log_directory, ignore_errors=True)
            return False
        else:
            csv_path = self.log.log_file.name.replace('.txt', '.csv')
            self.log.csv_file = csv_path
            self.log.log_directory = self.log_directory
            self.log.save()
        return True

    def create_kml(self):
        try:
            generate_kml(self.csv_path, self.kml_path)
        except EnvironmentError:
            shutil.rmtree(self.log_directory, ignore_errors=True)
            return False
        else:
            kml_path = self.log.log_file.name.replace('.txt', '.kml')
            self.log.kml_file = kml_path
            self.log.save()
        return True

    def create_gpx(self):
        try:
            generate_gpx(self.csv_path, self.gpx_path)
        except EnvironmentError:
            shutil.rmtree(self.log_directory, ignore_errors=True)
            return False
        else:
            gpx_path = self.log.log_file.name.replace('.txt', '.gpx')
            self.log.gpx_file = gpx_path
            self.log.save()
        return True

    def create_all(self):
        """ create *.csv and *.gpx"""
        csv_created = self.create_csv()
        if csv_created and self.create_gpx():
            return True
        else:
            return False


#
# ------------------------------ Functions -------------------------------------
#
def profile_photo_upload_to(instance, filename):
    """ Function returns upload path for user photo """
    return os.path.join(instance.user.username, 'profile_photo', instance.user.username + os.path.splitext(filename)[1])


def log_upload_to(instance, filename):
    """ Function return upload path for log-file """
    suffix = datetime.datetime.now().strftime("_upload_%d%m%y_%H%M%S")
    new_filename = str(uuid.uuid4())+'.txt'
    return os.path.join(instance.user.username, 'logs', 'DJIFlightRecord'+suffix, new_filename)


def get_images_list(path):
    images = []
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*.jpg'):
            images.append(file)
    middle = len(images) // 2
    images = sorted(images)
    img, thmb = images[0:middle], images[middle:]
    return dict(zip(img, thmb))


def get_data(log):
    data = {}
    path = log.csv_file.path
    with open(path, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = {'aircraft_name': row['DETAILS.aircraftName'],
                        'drone_type': row['RECOVER.droneType'],
                        'app_version': row['DETAILS.appVersion'],
                        'app_type': row['RECOVER.appType'],
                        'start_engines': row['DETAILS.timestamp'] + '+0000',
                        'stop_engines': row['CUSTOM.updateTime'] + '+0000',
                        'latitude': row['DETAILS.latitude'],
                        'longitude': row['DETAILS.longitude'],
                        'aircraft_sn': row['DETAILS.aircraftSn'],
                        'battery_sn': row['DETAILS.batterySn'],
                        'camera_sn': row['DETAILS.cameraSn']
                        }
        except UnicodeDecodeError:
            pass
    if data:
        log.start_time = datetime.datetime.strptime(data['start_engines'], '%Y/%m/%d %H:%M:%S.%f%z')
        log.end_time = datetime.datetime.strptime(data['stop_engines'], '%Y/%m/%d %H:%M:%S.%f%z')
        log.data = data
        log.save()


def delete_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
