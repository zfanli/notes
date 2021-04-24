from pathlib import Path
from urllib.parse import quote


def maketable():
    res = {}

    for child in Path(".").parent.iterdir():
        if child.suffix == ".md":
            if child.stem == "README":
                continue
            name = child.stem
            difficulty = name.split("(")[-1].split(")")[0]
            title = name.split(".")[-1].split("(")[0].strip()
            res[int(name.split(".")[0])] = [title, difficulty, child.name]

    table = [
        "",
    ]

    for key in sorted(res):
        row = "|"
        row += str(key) + "|"
        row += f"[{res[key][0]}](./{quote(res[key][2])})|"
        row += res[key][1] + "|"
        table.append(row)

    table.append("|-|-|-|")
    table.append("|#|Title|difficulty|")
    table.append("")

    return "\n".join(reversed(table))


if __name__ == "__main__":
    print(maketable())
