# Run your own Data & AI Bootkon

Do you want to contribute to Data & AI Bootkon or run your own fork? Then this section is for you.

Data & AI Bootkon is set up to be a scalable asset that can be forked and modified to alter its content with ease.
There are two GitHub actions you should be aware of:

1. Rendering of `.TUTORIAL.md`: the labs are rendered by a GitHub action from a jinja2 template in `docs/TUTORIAL.md`.
2. Book creation: the handbook is rendered through mdbook and a custom jinja2 preprocessor by a GitHub action. The book's main file is located at `docs/SUMMARY.md`.

We recommend using Cloud Shell on GCP to develop Data & AI Bootkon. However, you can of course use any (local) editor you like.
Cloud Shell has the advantage that the tutorial markdown can be rendered without having to commit to GitHub or reloading Cloud Shell, drastically reducing the feedback time in the development cycle.

<div class="mdbook-alerts mdbook-alerts-tip">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  Tip
</p>
<p>Please also read through the <a href="../labs/main.html">common pitfalls</a> with Cloud Shell before proceeding.</p>
</div>