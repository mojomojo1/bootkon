# Run your own Data & AI Bootkon

Do you want to contribute to Data & AI Bootkon or run your own fork? Then this section is for you.

Data & AI Bootkon is set up to be a scalable asset that can be forked and modified to alter its content with ease.

We recommend using Cloud Shell on GCP to develop Data & AI Bootkon. However, you can of course use any (local) editor you like.
Cloud Shell has the advantage that the tutorial markdown can be rendered without having to commit to GitHub or reloading Cloud Shell, drastically reducing the feedback time in the development cycle.

There are several utility scripts in the `.scripts` directory that are added to `$PATH` when you install bootkon in Cloud Shell.

| Script                    | Description                                                                                                                  |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `bk`            | Main Bootkon initialization script. Clones the repo, sets environment variables, installs packages, opens the tutorial.    |
| `bk-bootstrap`| Sets up necessary GCP permissions for Bootkon.                                                                          |
| `bk-bootstrap-accounts` | Given a CSV file with usernames (*@gcplab.me) in the first column, grants editor and IAM editor permission. |
| `bk-deactivate`| Deactivates the auto-loading of bootkon. |
| `bk-mdbook`    | Serves the handbook using `mdbook` after preprocessing with `jinja2`.                                                 |
| `bk-tutorial`   | Opens a specified tutorial Markdown file in the Cloud Shell editor.                                                            |
| `bk-delete-resources` | Script to delete resources (e.g. Vertex) when rerunning the tutorial. |
| `bk-info` | Displays information about the current bootkon installation. |