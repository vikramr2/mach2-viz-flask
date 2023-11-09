'''
@author Vikram Ramavarapu

Server side for starting viz via commandline argument
'''

import json
import webbrowser
import threading
from sys import argv

from flask import Flask, jsonify  # Import flask


class Viz:
    ''' Visualizer class. Stores json data and has methods to open the visualizer GUI'''

    def __init__(self, filename):
        self.filename = filename

        # Setup the flask app by creating an instance of Flask
        self.app = Flask(__name__, static_url_path='/mach2-viz/')

        # Open the JSON file
        with open(self.filename, 'r', encoding='utf-8') as file:
            # Load the JSON data
            json_data = json.load(file)
            self.labeling = json_data['solutions'][0]['name']

        @self.app.route('/')
        def home():
            ''' Home route to open the page '''

            # Return index.html from the static folder
            return self.app.send_static_file('index.html')

        @self.app.route('/json')
        def send_json():
            ''' API Gateway to send json data '''

            return jsonify({"data": json.dumps(json_data)})

    def run(self):
        ''' Open visualizer '''
        # Open the URL in the default web browser
        url = f'http://127.0.0.1:5000/#/viz?labeling={self.labeling}&labeling2={self.labeling}'
        threading.Timer(1, lambda: webbrowser.open(url)).start()

        self.app.run()


if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    JSON_FILE = argv[1]

    app = Viz(JSON_FILE)
    app.run()  # Start the server
