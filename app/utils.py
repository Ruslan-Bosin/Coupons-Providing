from app import app
import jinja2
import os


@app.template_filter("style")
def style(style_path, data):
    path, filename = os.path.split(style_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./")).get_template(filename).render(data=data)
