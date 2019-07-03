import os


def remove_empty_lines(text: str) -> str:
    """Removes empty lines from a multi-line str

    :param text: the input multi-line string
    :return: only non-empty trimmed lines as one string
    """
    return "\n".join([line.rstrip() for line in text.splitlines() if line.strip()])


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
