import json
import sys
import re

import collections.abc

def replace_cloudshell_tags(s):
    # <walkthrough-tutorial-duration duration="30"></walkthrough-tutorial-duration>
    s = re.sub(
        r'<walkthrough-tutorial-duration duration=\\"(\d+)\\"></walkthrough-tutorial-duration>',
        #r'<div align=right><font color=lightgreen>Duration: \1 min</font></div> ',
        r'![](https://img.shields.io/badge/duration-\1_min-green)',
        s)
    # <walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>
    s = re.sub(
        r'<walkthrough-tutorial-difficulty difficulty=\\"(\d+)\\"></walkthrough-tutorial-difficulty>',
        r'![](https://img.shields.io/badge/difficulty-\1%2F5-red)',
        s)
    # <walkthrough-project-id/>
    s = s.replace("<walkthrough-project-id/>", "<PROJECT_ID>")

    return s

if __name__ == '__main__':
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)

    # load both the context and the book representations from stdin
    context, book = json.load(sys.stdin)
    book_str = json.dumps(book)
    book_str = replace_cloudshell_tags(book_str)

    with open("foo.json", "w") as f:
        print(book_str, file=f)

    # we are done with the book's modification, we can just print it to stdout, 
    print(book_str)
