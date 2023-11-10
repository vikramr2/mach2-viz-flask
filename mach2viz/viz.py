'''
@author Vikram Ramavarapu

Server side for starting viz via commandline argument
'''

import fnmatch
import os
import re
import socket
import json
import webbrowser
import threading
from sys import argv

from flask import Flask, jsonify  # Import flask


class Viz:
    ''' Visualizer class. Stores json data and has methods to open the visualizer GUI'''

    def __init__(self, filename=None, solution=None):
        # Argument error handling
        if (not filename and not solution):
            raise TypeError('The visualizer requires either a filename or a solution object')

        if (filename and solution):
            raise TypeError(
                'The visualizer requires either a filename or a solution object, not both.'
            )

        # Setup the flask app by creating an instance of Flask
        self.app = Flask(__name__, static_url_path='/mach2-viz/')

        # Set port to be the first free port
        self.port = self._find_next_open_port(5000)

        # Change client port number
        self._change_port_in_client()

        # If a filename to a json is given, parse it and load data
        if filename:
            self.filename = filename

            # Open the JSON file
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Load the JSON data
                json_data = json.load(file)
                self.labeling = json_data['solutions'][0]['name']

        # If data is given directly, no need to parse
        if solution:
            json_data = solution

            self.solution = solution
            self.labeling = self.solution['solutions'][0]['name']

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
        url = f'http://127.0.0.1:{self.port}/#/viz?labeling={self.labeling}&labeling2={self.labeling}'
        threading.Timer(1, lambda: webbrowser.open(url)).start()

        self.app.run(port=self.port)

    def _find_next_open_port(self, start_port):
        current_port = start_port
        while True:
            try:
                # Try to create a socket on the current port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', current_port))
                return current_port
            except OSError:
                # Port is not available, try the next one
                current_port += 1

    def _change_port_in_client(self):
        ''' Goes through the client code and changes hardcoded port number '''
        directory = 'static/static/js'
        pattern = 'main*chunk.js*'

        result = self._find_files(directory, pattern)

        for file in result:
            self._replace_port_number_in_file(file, self.port)

    def _find_files(self, directory, pattern):
        matches = []
        for root, _, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
        return matches

    def _replace_port_number_in_file(self, file_path, new_port_number):
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Define the regular expression pattern to match the substring
        pattern = r"fetch\(['\"]http://127.0.0.1:(\d+)/json['\"]\)"

        # Use re.sub to replace the matched port number with the new port number
        replaced_content = re.sub(pattern, f"fetch('http://127.0.0.1:{new_port_number}/json')", file_content)

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(replaced_content)


if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    JSON_FILE = argv[1]

    app = Viz(filename=JSON_FILE)
    app.run()  # Start the server
