
DATA_PATH = "data/champion"
LANGUAGES = ["en"]
mode = "js"

import json

print("----- Mission Start -----")
for language in LANGUAGES:
    fileName = language + ".json"
    outFileName = language + ".js"
    with open(f"{DATA_PATH}/{fileName}", 'r') as f, open(f"{DATA_PATH}/{outFileName}", 'w') as fout:
        data = json.loads(f.read())
        champions = data["data"]

        if mode == "dom":
            fout.write("<select name='b1'>\\\n")
        if mode == "js":
            fout.write("switch(name) {\n")

        for champion in champions:
            name = str(champions[champion]["name"])
            key = str(champions[champion]["key"])
            if mode == "dom":
                line = f"    <option value='{key}' style='color:black'>{name}</option>\\\n"
            if mode == "csv":
                line = f"{key},{name}\n"
            if mode == "js":
                line = f'    case {key}: return "{name}";\n'
            fout.write(line)

        if mode == "dom":
            fout.write("</select>")
        if mode == "js":
            fout.write('    default: return "No Result";\n')
            fout.write("}")
    print("Language "+language+" done")
print("----- Mission Complete -----")
