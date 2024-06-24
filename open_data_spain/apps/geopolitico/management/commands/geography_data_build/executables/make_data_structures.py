import os
import csv

from jinja2 import Template

HERE = os.path.dirname(__file__)


def create_municipios(input_file: str, output_file: str, class_name: str):
    res = {}

    with open(input_file, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')

        for row in spamreader:
            cod_comunidad, cod_provincia, cod_municipio, name = row

            res[f"{cod_comunidad}{cod_provincia}{cod_municipio}"] = (cod_comunidad, cod_provincia, cod_municipio, name)

    dict_template = """{{ dict_name }}_BY_CODE = {{ '{' }}
{%- for k, v in values.items() %}
    "{{ k }}": {{ '{' }}
        "cod_comunidad": "{{ v[0] }}",
        "cod_provincia": "{{ v[1] }}",
        "cod_municipio": "{{ v[2] }}",
        "name": "{{ v[3] }}",
    {{ '}' }},
{%- endfor %}
{{ '}' }}

{{ dict_name }}_BY_NAME = {{ '{' }}
{%- for k, v in values.items() %}
    "{{ v[3] }}": {{ '{' }}
        "cod_comunidad": "{{ v[0] }}",
        "cod_provincia": "{{ v[1] }}",
        "cod_municipio": "{{ v[2] }}",
    {{ '}' }},
{%- endfor %}
{{ '}' }}

"""

    template = Template(dict_template)
    rendered_template = template.render({
        "dict_name": class_name,
        "values": res
    })

    with open(output_file, "w") as f:
        f.write(rendered_template)


def create_prov_com(input_file: str, output_file: str, class_name: str):
    res = {}

    with open(input_file, newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        for row in spamreader:
            index, name = row
            res[index] = name

    dict_template = """{{ dict_name }} = {{ '{' }}
{%- for k, v in values.items() %}
    '{{ k }}': '{{ v }}',
{%- endfor %}
{{ '}' }}"""

    template = Template(dict_template)
    rendered_template = template.render({
        "dict_name": class_name,
        "values": res
    })

    with open(output_file, "w") as f:
        f.write(rendered_template)


def main():
    prov_comun = (
        ("provincias", "PROVINCIAS"),
        ("comunidades", "COMUNIDADES")
    )

    for (n, class_name) in prov_comun:
        csv_path = os.path.join(HERE, "../data", f"{n}.es.csv")
        dump_path = os.path.join(HERE, "../data", f"{n}.py")

        create_prov_com(csv_path, dump_path, class_name)

    csv_path = os.path.join(HERE, "../data", f"municipios.es.csv")
    dump_path = os.path.join(HERE, "../data", f"municipios.py")
    create_municipios(csv_path, dump_path, "MUNICIPIOS")


if __name__ == '__main__':
    main()
