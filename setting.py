from flask import Flask, jsonify, request, Response
import json
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' +file_path
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
