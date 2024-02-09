import glob
import os

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


def aggregate_today_response(today):
    folder_path = "conversations"
    output_filename = f"response_{today}.txt"
    output_path = os.path.join(folder_path, output_filename)
    for file_path in glob.glob(os.path.join(folder_path, "*.txt")):
        filename = os.path.basename(file_path)
        file_date = filename[9:17]
        if file_date == today:
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
