import json
import sys
import re
import os

import jinja2

GITHUB_REPOSITORY=os.environ.get("GITHUB_REPOSITORY", "fhirschmann/bootkon")


if __name__ == '__main__':
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)

    # load both the context and the book representations from stdin
    context, book = json.load(sys.stdin)
    book_str = json.dumps(book)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="docs"))
    template = environment.from_string(book_str)

    # we are done with the book's modification, we can just print it to stdout.
    rendered = template.render(
        GITHUB_REPOSITORY=GITHUB_REPOSITORY,
        MDBOOK_VIEW=True
    )
    print(rendered)
