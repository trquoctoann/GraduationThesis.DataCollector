def read_lines_from_given_position(file_path, num_lines):
    last_read_position = (
        "src\\pizzatalk_data_collector\\labeller\\last_read_position.txt"
    )

    try:
        with open(last_read_position, "r", encoding="utf-8") as pos_file:
            start_line = int(pos_file.read().strip() or 0)
    except FileNotFoundError:
        start_line = 0

    lines_read = []
    with open(file_path, "r", encoding="utf-8") as file:
        for _ in range(start_line):
            next(file, None)
        for _ in range(num_lines):
            line = next(file, None)
            if line is None:
                break
            lines_read.append(line.strip())

    new_start_line = start_line + len(lines_read)
    with open(last_read_position, "w", encoding="utf-8") as pos_file:
        pos_file.write(str(new_start_line))

    return "\\n".join(lines_read)
