'''
@author Vikram Ramavarapu

Server side for starting viz via commandline argument
'''

import json

from flask import Flask, jsonify  # Import flask


JSON_FILE = '/Users/vikram/Documents/Research/El-Kebir/mach2-viz/mach2viz-client/src/samples/A1/A1.json'

class Viz:
    ''' Visualizer class. Stores json data and has methods to open the visualizer GUI'''

    def __init__(self, filename):
        self.filename = filename

        # Setup the flask app by creating an instance of Flask
        self.app = Flask(__name__, static_url_path='/mach2-viz/')

        @self.app.route('/')
        def home():
            ''' Home route to open the page '''

            # Return index.html from the static folder
            return self.app.send_static_file('index.html')

        @self.app.route('/json')
        def send_json():
            ''' API Gateway to send json data '''

            # Open the JSON file
            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                # Load the JSON data
                json_data = json.load(file)

            return jsonify({"data": json.dumps(json_data)})

    def run(self):
        ''' Open visualizer '''
        self.app.run()


if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app = Viz(JSON_FILE)
    app.run()  # Start the server
