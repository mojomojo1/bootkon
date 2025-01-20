## Lab 4: ML Operations with Vertex AI

<walkthrough-tutorial-duration duration="60"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

In this lab, you will create a Vertex AI Workbench Instance and perform machine learning on the data set you previously ingested.

Vertex AI Workbench is a Jupyter notebook-based development environment for the entire data science workflow. You can interact with Vertex AI and other Google Cloud services from within a Vertex AI Workbench instance's Jupyter notebook.

Vertex AI Workbench integrations and features can make it easier to access your data, process data faster, schedule notebook runs, and more.

For example, Vertex AI Workbench lets you:

- Access and explore your data from within a Jupyter notebook by using BigQuery and Cloud Storage integrations.
- Automate recurring updates to your model by using scheduled executions of your notebook's code that run on Vertex AI.
- Process data quickly by running a notebook on a Dataproc cluster.
- Run a notebook as a step in a pipeline by using Vertex AI Pipelines.


You can [create](https://cloud.google.com/vertex-ai/docs/workbench/instances/create#gcloud) such an instance either through the UI, or using the following command:

```bash
gcloud workbench instances create bootkon-notebook3 \
    --project=$PROJECT_ID \
    --location=${REGION}-a \
    --vm-image-project=cloud-notebooks-managed \
    --vm-image-name=workbench-instances-v20230822-debian-11-py310 \
    --machine-type=e2-standard-4 \
    --metadata=post-startup-script=gs://${PROJECT_ID}-bucket/bootstrap_workbench.sh
```

Open the [Vertex AI Console](https://console.cloud.google.com/vertex-ai/workbench/locations/us-central1-a/instances/bootkon-notebook) and as soon as the instance is ready, click on `OPEN JUPYTERLAB`. The bootkon repository has been automatically cloned using the `post-startup-script` we passed earlier.

Now, please open `notebooks/bootkon_lab4_vertex.ipynb` and continue your journey.

{% if MDBOOK_VIEW %}

---

<div class="mdbook-alerts mdbook-alerts-caution">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  caution
</p>
<p>
Below you can find the content of <code>notebooks/bootkon_lab4_vertex.ipynb</code>. Feel free to skim over it, but please open it from your JupyterLab instance you created above.
</p>
</div>

{{ jupyter('notebooks/bootkon_lab4_vertex.ipynb') }}

{% endif %}