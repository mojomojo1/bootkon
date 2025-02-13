This directory contains the markdown file both the book as well as the Cloud Shell tutorial are built from.
These markdown files are passed through the [jinja](https://jinja.palletsprojects.com/en/stable/templates/) template engine in both cases.
```
.
├── SUMMARY.md: master document of the book (the navigation bar on the left hand side)
├── TUTORIAL.md: master document of the Cloud Shell tutorial
├── book: markdown files solely used in the book
├── css: additional css for the book
├── img: images
├── labs: code lab sources
    ├── 1_environment_setup.md
    ├── 2_data_ingestion.md
    ├── 3_dataform.md
    ├── 4_ml.md
```
