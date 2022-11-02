from app import app
from jinja2 import Environment, FileSystemLoader
from os import path as os_path


@app.template_filter("style")
def style(style_path, data_css=None):

    absolute_path = (os_path.abspath(__file__).replace(f"\\{os_path.basename(__file__)}", '') + style_path)\
        .replace("/", "\\")
    path, filename = os_path.split(absolute_path)

    file_loader = FileSystemLoader(path)
    environment = Environment(loader=file_loader)
    template = environment.get_template(filename)

    if data_css is None:
        return template.render()
    return template.render(data_css)
