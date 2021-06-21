from datetime import datetime

from dateutil import parser
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from database import db
from models.investors import Investor
import re


class XlsxParser(object):
    week_start: datetime.date = None
    week_end: datetime.date = None
    DATES_INDEX = 2
    START_VALID_DATA_INDEX = 6

    def __init__(self, wb: Workbook) -> None:
        self.investors = []
        self.wb = wb

    def bulk_insert(self) -> None:
        db.session.bulk_save_objects(self.investors)
        db.session.commit()
        self.investors.clear()

    def get_page_data(self, worksheet: Worksheet):
        for index, row in enumerate(worksheet.iter_rows(values_only=True)):
            if index == self.DATES_INDEX:
                test = re.findall("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", row[0])  # noqa
                self.week_start = parser.parse(test[0])
                self.week_end = parser.parse(test[1])

            elif index >= self.START_VALID_DATA_INDEX and row[0] and not row[0].lower().__contains__('total'):
                self.investors.append(Investor(
                    title=row[0],
                    total=row[3],
                    week_end=self.week_end,
                    week_start=self.week_start
                ))

    def parse_data(self) -> None:
        self.clean_investors_data()
        for page_nr, _ in enumerate(self.wb.sheetnames):
            self.wb.active = page_nr
            self.get_page_data(self.wb.active)
            self.bulk_insert()

    @staticmethod
    def clean_investors_data() -> None:
        Investor.query.delete()
