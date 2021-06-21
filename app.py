import os
from pathlib import Path

import openpyxl
from dotenv import dotenv_values
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from database import db
from utils.parsers import XlsxParser
from views.investors import InvestorResources

app = Flask(__name__)
api = Api(app)
config = dotenv_values(".env")

DATABASE_NAME = config['POSTGRES_DB']
DATABASE_PASSWORD = config['POSTGRES_PASSWORD']
DATABASE_USER = config['POSTGRES_USER']
DATABASE_HOST = config['DB_HOST']
DATABASE_PORT = config['DB_PORT']
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DATABASE_USER}' \
                                        f':{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
basedir = os.path.abspath(os.path.dirname(__file__))
api.add_resource(InvestorResources, '/data')


@app.cli.command("seed-db")
def seed_from_xlsx() -> None:
    xlsx_files = [path for path in Path('seeds').rglob('*.xlsx')]
    wbs = [openpyxl.load_workbook(wb) for wb in xlsx_files]
    for wb in wbs:
        XlsxParser(wb).parse_data()


if __name__ == '__main__':
    app.run(port=8080)
