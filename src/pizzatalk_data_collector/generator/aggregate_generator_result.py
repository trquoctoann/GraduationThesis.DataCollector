import glob
import os
from datetime import timedelta

import send2trash


def read_unique_lines(file_path):
    unique_lines = set()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                cleaned_line = line.strip()
                unique_lines.add(cleaned_line)
    except Exception:
        return None
    unique_lines_list = list(unique_lines)
    return unique_lines_list


def aggregate_specified_date_response(
    specified_date, folder_contain_response="conversations"
):
    output_filename = f"response_{specified_date}.txt"
    output_path = os.path.join(folder_contain_response, output_filename)
    for file_path in glob.glob(
        os.path.join(folder_contain_response, "response_*_*.txt")
    ):
        filename = os.path.basename(file_path)
        file_date = filename[9:17]
        if file_date == str(specified_date):
            unique_sentences = read_unique_lines(file_path)
            if unique_sentences is not None:
                for sentence in unique_sentences:
                    with open(
                        output_path,
                        "a",
                        encoding="utf-8",
                    ) as file:
                        file.write(f"{sentence}\n")
            send2trash.send2trash(file_path)


def aggregate_response_in_date_range(
    start_date,
    end_date,
    output_filename,
    folder_contain_response="conversations",
):
    output_path = os.path.join(folder_contain_response, output_filename)
    current_date = start_date
    all_unique_sentences = []
    while current_date <= end_date:
        for file_path in glob.glob(
            os.path.join(folder_contain_response, "response_*.txt")
        ):
            filename = os.path.basename(file_path)
            file_date = filename[9:17]
            if file_date == str(current_date.strftime("%Y%m%d")):
                unique_sentences = read_unique_lines(file_path)
                if unique_sentences is not None:
                    all_unique_sentences += unique_sentences
                send2trash.send2trash(file_path)
        current_date += timedelta(days=1)
    with open(output_path, "a", encoding="utf-8") as file:
        for sentence in set(all_unique_sentences):
            file.write(f"{sentence}\n")
