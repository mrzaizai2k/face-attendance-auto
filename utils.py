import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
import selenium
import time
import yaml
from datetime import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def config_parser(data_config_path = 'config/config.yaml'):
    with open(data_config_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def initialize_camera(index=0):
    # You might need to change the camera index (0, 1, 2, etc.) based on your system setup
    camera_index = index
    cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
    return cap

def detect_faces(frame):
    detector = MTCNN()
    faces = detector.detect_faces(frame)
    return faces

class FaceScraper:

    def __init__(self, show_UI = False):
        self.data_config = config_parser()
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.media_stream_camera": 1
            })

        self.show_UI = show_UI
        if self.show_UI:
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            chrome_options.add_argument("--headless") # Ensure GUI is off
            self.driver = webdriver.Chrome(options=chrome_options)

    def signin(self):
        self.driver.get("your-web")
        time.sleep(1)
        button_class = "cta"
        button_element = self.driver.find_element(By.CLASS_NAME, button_class)
        button_element.click()

        time.sleep(1)
        # Check the cust_no value
        self.cust_cif = self.driver.find_element(By.ID, "cust_no").text
        self.cust_name = self.driver.find_element(By.ID, "emp_name").text
        self.date = self.driver.find_element(By.ID, "date").text

        if self.cust_cif == str(self.data_config.get('user_cif')):
            print(f"User {self.cust_name } đã điểm danh lúc {self.date}")
            self.write_time()
            return True
        return False
    
    def write_time(self):
        # Parse the date
        date_object = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
        time_in = None
        time_out = None
        new_data ={}
        # Check hour and set variables
        if date_object.hour >= 17:
            new_data = {'date': [date_object.date()], 
                    'cif': [self.data_config.get('user_cif')], 
                    'name': [self.data_config.get('user_name')], 
                    'time_in': '', 
                    'time_out': [date_object.time()]}
        elif date_object.hour <= 8:
            new_data = {'date': [date_object.date()], 
                    'cif': [self.data_config.get('user_cif')], 
                    'name': [self.data_config.get('user_name')], 
                    'time_in': [date_object.time()], 
                    'time_out': ''}
        # File path
        file_diemdanh_path = self.data_config.get('file_diemdanh_path')
        print('new_data', new_data)
        df = pd.DataFrame(new_data)
        df.to_csv(file_diemdanh_path, mode='a', header=False, index=False)

    def close_broser(self):
        self.driver.quit()
