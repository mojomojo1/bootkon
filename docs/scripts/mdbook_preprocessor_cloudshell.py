import json
import sys
import re

CLOUD_SHELL_NOTE = """
<div class="mdbook-alerts mdbook-alerts-caution">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  caution
</p>
<p>You are viewing this lab from the handbook. However, this lab is meant to be loaded as Cloud Shell tutorial.</p>
</div>
"""

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


def replace_cloudshell_tags(s):
    # <walkthrough-tutorial-duration duration="30"></walkthrough-tutorial-duration>
    s = re.sub(
        r'<walkthrough-tutorial-duration duration="(\d+)"></walkthrough-tutorial-duration>',
        #r'<div align=right><font color=lightgreen>Duration: \1 min</font></div> ',
        r'![](https://img.shields.io/badge/duration-\1_min-green)',
        s)
    # <walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>
    s = re.sub(
        r'<walkthrough-tutorial-difficulty difficulty="(\d+)"></walkthrough-tutorial-difficulty>',
        r'![](https://img.shields.io/badge/difficulty-\1%2F5-red)',
        s)
    # <walkthrough-project-id/>
    s = s.replace("<walkthrough-project-id/>", "<PROJECT_ID>")
    s = s.replace("<bootkon-cloud-shell-note/>", CLOUD_SHELL_NOTE)

    return s

if __name__ == '__main__':
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)

    # load both the context and the book representations from stdin
    context, book = json.load(sys.stdin)
    apply_to_content(book, replace_cloudshell_tags)

    # we are done with the book's modification, we can just print it to stdout, 
    print(json.dumps(book))
