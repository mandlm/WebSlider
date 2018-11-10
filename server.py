#!/usr/bin/python3

from waitress import serve

import slider

serve(slider.app, host="0.0.0.0", port=8080)

