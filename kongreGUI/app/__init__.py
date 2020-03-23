from flask import Flask
import os

app= Flask(__name__, instance_relative_config=True )

from app import views

app.config.from_object('config')
