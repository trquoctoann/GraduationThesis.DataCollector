import json

import gspread
import pandas as pd
from importer.preprocessing.articles_preprocessing import pos_tagging
from oauth2client.service_account import ServiceAccountCredentials
from utils.setup_logger import setup_logger


class ArticlesImporter:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.spreadsheet = self.__get_spread_sheet()
        self.raw_worksheet = self.__get_worksheet("Raw")
        self.labelling_worksheet = self.__get_worksheet("Labelling")
        self.labelled_worksheet = self.__get_worksheet("Labelled")

    def __get_spread_sheet(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]

        # need to enable google sheet api on gcp to get credentials.json
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "src/data_crawler/importer/credentials.json", scope
        )
        client = gspread.authorize(creds)
        try:
            spreadsheet = client.open("Articles")
        except Exception:
            self.logger.debug("Creating new spread sheet")
            spreadsheet = client.create("Articles")
            spreadsheet.share(
                "quoctoan09072002@gmail.com", perm_type="user", role="writer"
            )
        return spreadsheet

    def __get_worksheet(self, worksheet_name):
        try:
            worksheet = self.spreadsheet.worksheet(worksheet_name)
        except Exception:
            self.logger.debug("Creating new worksheet")
            if worksheet_name == "Raw":
                worksheet = self.spreadsheet.add_worksheet(
                    title=worksheet_name, rows=100, cols=5
                )
            elif worksheet_name == "Labelling" or worksheet_name == "Labelled":
                worksheet = self.spreadsheet.add_worksheet(
                    title=worksheet_name, rows=100, cols=4
                )
        return worksheet

    def import_to_sheet(self, new_articles):
        self.logger.debug("Starting the import process for new articles.")
        self.__import_to_sheet_raw(new_articles)
        self.__import_to_sheet_labelling_NER(new_articles)
        self.logger.debug("Completed the import process for new articles.")

    def __import_to_sheet_raw(self, new_articles):
        new_articles_dict = [
            json.loads(article.to_json()) for article in new_articles
        ]
        new_articles_df = pd.DataFrame(new_articles_dict)
        self.raw_worksheet.append_rows(new_articles_df.values.tolist())
        self.logger.debug(
            f"Imported {len(new_articles_df)} raw articles to 'Raw' worksheet successfully"
        )

    def __import_to_sheet_labelling_NER(self, new_articles):
        all_text = " ".join(
            [
                article.title + ". " + article.content
                for article in new_articles
            ]
        )
        result = pos_tagging(all_text)
        self.labelling_worksheet.append_rows(result.values.tolist())
        self.logger.debug(
            f"Imported NER labelling data for {len(result)} words to 'Labelling' worksheet successfully"
        )
