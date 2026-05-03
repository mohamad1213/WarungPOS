import os
import sys

# Add project directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Django WSGI application
from kasir_project.wsgi import application