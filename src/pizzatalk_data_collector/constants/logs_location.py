from enum import Enum


class LogsLocation(Enum):
    CRAWLER = "logs/crawler.log"
    GENERATOR = "logs/generator.log"
    IMPORTER = "logs/importer.log"
