# Run your own Data & AI Bootkon

Do you want to contribute to Data & AI Bootkon or run your own fork? Then this section is for you.

Data & AI Bootkon is set up to be a scalable asset that can be forked and modified to alter its content with ease.
There is one GitHub Action you should be aware of.

- Book creation: the handbook is rendered through mdbook and a custom jinja2 preprocessor by a GitHub action. The book's main file is located at `docs/SUMMARY.md`.

We recommend using Cloud Shell on GCP to develop Data & AI Bootkon. However, you can of course use any (local) editor you like.
Cloud Shell has the advantage that the tutorial markdown can be rendered without having to commit to GitHub or reloading Cloud Shell, drastically reducing the feedback time in the development cycle.