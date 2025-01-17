#!/usr/bin/env python
# mdBook preprocessor to render markdown using the jinja2 template engine
# author: Fabian Hirschmann

import json
import sys
import os
import nbformat
import base64
from nbconvert import HTMLExporter, MarkdownExporter

import jinja2

GITHUB_REPOSITORY=os.environ.get("GITHUB_REPOSITORY", "fhirschmann/bootkon")


def apply_to_content(data, func):
    """
    Recursively apply a function to the value of the key 'content' in a nested dictionary or list.

    :param data: The dictionary or list to process.
    :param func: The function to apply to 'content' values.
    :return: The modified dictionary or list.
    """
    if isinstance(data, dict):
        # Check if the key 'content' exists, and apply the function to its value.
        if "content" in data:
            data["content"] = func(data["content"])
        # Recursively apply the function to nested dictionaries or lists.
        for key, value in data.items():
            apply_to_content(value, func)
    elif isinstance(data, list):
        # Recursively apply the function to each item in the list.
        for item in data:
            apply_to_content(item, func)
    return data


def jupyter(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
        exporter = HTMLExporter()
        exporter = MarkdownExporter()
        body, resource = exporter.from_notebook_node(nb)
        with open("test.md", "w") as f:
            f.write(body)
        for k, v in resource["outputs"].items():
            if k.endswith(".png"):
                enc = base64.b64encode(v).decode()
                body = body.replace(
                    f"![png]({k})",
                    f'<img src="data:image/png;base64,{enc}" />'
                )

        return body
    


def render(content):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="docs"))
    template = environment.from_string(content)

    rendered = template.render(
        GITHUB_REPOSITORY=GITHUB_REPOSITORY,
        MDBOOK_VIEW=True,
        jupyter=jupyter
    )

    return rendered


if __name__ == '__main__':
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)

    # load both the context and the book representations from stdin
    context, book = json.load(sys.stdin)
    apply_to_content(book, render)

    # we are done with the book's modification, we can just print it to stdout.
    print(json.dumps(book))
