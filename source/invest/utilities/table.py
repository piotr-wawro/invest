def print_table(data: list[list], name: str|None = None) -> str:
    width = col_width(data)

    res = ''
    if name:
        res += print_name(data[0], width, name)
    res += print_header(data[0], width)

    res += print_sep(data[0], width)
    for row in data[1:]:
        res += print_row(row, width)
    res += print_sep(row, width)

    return res

def print_name(row: list[str], width: list[int], name: str) -> str:
    n = sum(width) + len(row) - 1

    res = ''
    res += print_sep(row, width)
    res += f"|{name.center(n)}|\n"
    return res

def print_header(row: list[str], width: list[int]) -> str:
    res = ''
    res += print_sep(row, width)
    res += print_row(row, width, 'c')
    return res

def print_row(row: list[str], width: list[int], padding: str = 'l') -> str:
    if padding == 'l':
        transform = lambda x, w: f" {x.ljust(w-1)}"
    elif padding == 'c':
        transform = lambda x, w: f"{x.center(w)}"
    elif padding == 'r':
        transform = lambda x, w: f"{x.rjust(w-1)} "
    else:
        transform = lambda x, w: f" {x.ljust(w-1)}"

    res = ''
    for c, w in zip(row, width):
        res += f"|{transform(str(c), w)}"
    res += '|\n'
    return res

def print_sep(row: list[str], width: list[int]) -> str:
    n = sum(width) + len(row) - 1
    res = f"+{'-'*n}+\n"
    return res

def col_width(data: list[list]) -> list[int]:
    data = zip(*data)
    length = [[len(str(x)) for x in col] for col in data]
    res = [max(col)+2 for col in length]
    return res
