# Run your own bootkon

Do you want to contribute to bootkon or run your own fork? Then this section is for you.

Bootkon is set up to be a scalable asset that can be forked and modified to alter its content with ease.
There are two GitHub actions you should be aware of:

1. Rendering of `.TUTORIAL.md`: the labs are rendered by a GitHub action from a jinja2 template in `docs/TUTORIAL.md`.
2. Book creation: the handbook is rendered through mdbook and a custom jinja2 preprocessor by a GitHub action. The book's main file is located at `docs/SUMMARY.md`.

Continue onto the next subsection to create your own bootkon version.