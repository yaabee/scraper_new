def rm_escape_chars(string_value: str) -> str:
    """
    remove escape chars from given field
    """
    assert isinstance(string_value, str), "field_value ist kein string"
    string_value = " ".join(string_value.splitlines())
    escapes = "".join([chr(char) for char in range(1, 32)])
    translator = str.maketrans("", "", escapes)
    return " ".join([x for x in string_value.translate(translator).split(" ") if x])
