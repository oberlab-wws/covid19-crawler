from datetime import date
#
import xlsxwriter
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.worksheet import convert_cell_args
#
import json
import csv
#


class Covid19Crawler:
    def __init__(self, state, urls_tested = list(), urls_positive = list(), urls_deaths = list()):
        self.state = state
        self.urls_tested = urls_tested
        self.urls_positive = urls_positive
        self.urls_deaths = urls_deaths
        self.tested = None
        self.positive = None
        self.deaths = None
        self.notes_tested = None
        self.notes_positive = None
        self.notes_deaths = None

    def crawl(self):
        pass

    def write_results(self):
        print('results: {}'.format(self.state))
