import json, csv, os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from schemas import is_config, is_signatures_list


def select_config(path):
    try:
        with open(path, "r") as file:
            config = json.load(file)
            if type(config) is not list or len(config) == 0:
                print("No se ha encontrado ninguna configuración válida.")
                return None
            else:
                for i, c in enumerate(config):
                    if not is_config(c):
                        print(f"La configuración {i + 1} no tiene el formato correcto.")
                        return None

            if len(config) == 1:
                print(
                    f"Se ha encontrado una única configuración ({config[0]['id']}). Usándola..."
                )
                return config[0]
            else:
                print(f"Se han encontrado {len(config)} configuraciones:")
                for i, c in enumerate(config):
                    print(f"{i+1}. {c['id']}")
                input_config = input(
                    f"Selecciona una configuración [1-{len(config)}]: "
                )
                try:
                    index = int(input_config) - 1
                    if index < 0 or index >= len(config):
                        print("Selección inválida.")
                        return None
                    else:
                        print(f"Usando configuración: {config[index]['id']}")
                        return config[index]
                except ValueError:
                    print("Selección inválida.")
                    return None
    except:
        print(f"Error al leer el archivo {path}.")
        return None


def load_signatures_list():
    path = (
        input(
            "Introduce la ruta del archivo CSV con la lista de firmas a realizar (signatures_list.csv): "
        ).strip()
        or "signatures_list.csv"
    )
    try:
        with open(path, newline="") as file:
            signatures_list = list(csv.reader(file, delimiter=",", quotechar='"'))
            if not is_signatures_list(signatures_list):
                print("La primera fila contiene nombres de columnas inválidos.")
                return None
            elif len(signatures_list) < 2:
                print(
                    "La lista de firmas a generar no tiene suficientes filas. Ten en cuenta que la primera fila debe contener los nombres de las columnas."
                )
                return None
            return signatures_list
    except FileNotFoundError:
        print(f"No se ha encontrado el archivo {path}.")
        return None
    except:
        print(f"Error al leer el archivo {path}.")
        return None


def gen_signatures(config, signatures_list, template_path):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_path)
    cols = {
        value.lower().strip(): index
        for index, value in enumerate(signatures_list.pop(0))
    }
    os.makedirs(config["output_path"], exist_ok=True)

    config["date"] = datetime.now().strftime("%Y-%m-%d")
    for i, row in enumerate(signatures_list):
        for val in config:
            if isinstance(config[val], str):
                config[val] = config[val].strip()
        for col in cols:
            val = row[cols[col]]
            if isinstance(val, str):
                val = val.strip()
                if val == "None":
                    config.pop(col, None)
                elif val != "":
                    config[col] = val

            else:
                if val is not None:
                    config[col] = val

        if "output" not in config or config["output"] == "":
            config["output"] = f"signature{i}"

        content = template.render(config)
        with open(
            config["output_path"] + "/" + config["output"] + ".html", "w"
        ) as file:
            file.write(content)


def main():
    config = select_config("signatures.json")
    if config is None:
        return
    signatures_list = load_signatures_list()
    if signatures_list is None:
        return
    gen_signatures(config, signatures_list, "template.html.j2")


if __name__ == "__main__":
    main()
