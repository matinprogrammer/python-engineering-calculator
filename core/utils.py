def isnumber(number_str: str) -> bool:
    for char in number_str:
        if not (char.isnumeric() or char == "." or char == "-"):
            return False
    return True
