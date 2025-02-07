## Lab 4: ML Operations with Vertex AI

<walkthrough-tutorial-duration duration="60"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

In this lab, you will create a Vertex AI Workbench Instance and perform machine learning on the data set you previously ingested.

### Vertex AI Workbench

Vertex AI Workbench is a Jupyter notebook-based development environment for the entire data science workflow. You can interact with Vertex AI and other Google Cloud services from within a Vertex AI Workbench instance's Jupyter notebook.

Vertex AI Workbench integrations and features can make it easier to access your data, process data faster, schedule notebook runs, and more.

For example, Vertex AI Workbench lets you:

- Access and explore your data from within a Jupyter notebook by using BigQuery and Cloud Storage integrations.
- Automate recurring updates to your model by using scheduled executions of your notebook's code that run on Vertex AI.
- Process data quickly by running a notebook on a Dataproc cluster.
- Run a notebook as a step in a pipeline by using Vertex AI Pipelines.

You can [create](https://cloud.google.com/vertex-ai/docs/workbench/instances/create#gcloud) such an instance either through the UI, Terraform, or using the following command:

```bash
gcloud workbench instances create bootkon-notebook \
    --project=$PROJECT_ID \
    --location=${REGION}-a \
    --vm-image-project=cloud-notebooks-managed \
    --machine-type=e2-standard-4 \
    --vm-image-name workbench-instances-v20241118 \
    --metadata=post-startup-script=gs://${PROJECT_ID}-bucket/bootstrap_workbench.sh
```

Once the command has finished, please

1. Open [Vertex AI Console](https://console.cloud.google.com/vertex-ai/workbench)
2. Click on <walkthrough-spotlight-pointer locator="semantic({link 'bootkon-notebook'})">bootkon-notebook</walkthrough-spotlight-pointer>
2. Wait for the instance to become `Active`
3. and as soon as the instance is ready, click on `OPEN JUPYTERLAB`. 

The bootkon repository has been automatically cloned using the `post-startup-script` we passed earlier. Please note that you are working on a completely different machine and the files you modified on Cloud Shell are not reflected on Vertex AI Workbench.

Now, please open `notebooks/bootkon_vertex.ipynb` and continue your journey.

❗ Once you have gone through the Jupyter notebook, please come back here.

### Results in the Cloud Console

You've gone through the notebook -- great! Let's inspect the resources we created in Vertex AI.

1. Open [Vertex AI Console](https://console.cloud.google.com/vertex-ai?cloudshell=true&inv=1&invt=Abovkw)
2. Click <walkthrough-spotlight-pointer locator="css(a[id$=cfctest-section-nav-item-ai-platform-training])">Training</walkthrough-spotlight-pointer> in the navigation menu

Here you can see the training jobs you started both through the Python SDK as well as through Vertex AI Pipelines. Next, have a look at the model registry.

1. Click <walkthrough-spotlight-pointer locator="css(a[id$=cfctest-section-nav-item-ai-platform-models])">Model Registry</walkthrough-spotlight-pointer> in the nevigation menu
2. Click <walkthrough-spotlight-pointer locator="semantic({link 'bootkon-custom-model'})">bootkon-custom-model</walkthrough-spotlight-pointer>
3. Click <walkthrough-spotlight-pointer locator="semantic({tab 'Version details'})">VERSION DETAILS</walkthrough-spotlight-pointer>

Here you can can see that a model in the Vertex AI Model Registry is made up from a ***Container image*** als well as a **Model artifact location**. When you deploy a model, Vertex AI simply starts the container and points it to the artifact location.

The model has already been deployed to an endpoint. Let's have a look at them:

1. Click <walkthrough-spotlight-pointer locator="css(a[id$=cfctest-section-nav-item-ai-platform-online-prediction])">Online Prediction</walkthrough-spotlight-pointer> in the navigation menu
2. Click <walkthrough-spotlight-pointer locator="semantic({link 'bootkon-endpoint-custom'})">bootkon-endpoint-custom</walkthrough-spotlight-pointer>

You can see that the endpoint has one model deployed currently, and all the traffic is routed to it (traffic split is 100%). When scrolling down, you get live graphs as soon as predictions are coming in.

You can also train and deploy models on Vertex in the UI only. Let's have a more detailed look. Click <walkthrough-spotlight-pointer locator="semantic({button 'Edit settings'})">EDIT SETTINGS</walkthrough-spotlight-pointer>. Here you can find many options for model monitoring -- why don't you try to enable prediction drift detection?

Let's have a look at the Pipeline as well.

1. Click <walkthrough-spotlight-pointer locator="css(a[id$=cfctest-section-nav-item-ai-platform-ml-pipelines])">Pipelines</walkthrough-spotlight-pointer> in the navigation menu
2. Click <walkthrough-spotlight-pointer locator="semantic({link 'bootkon-pipeline-'})">bootkon-pipeline-...</walkthrough-spotlight-pointer>

You can now see the individual steps in the pipeline. Please click through the individual steps of the pipeline and have a look at the *Pipeline run analysis* on the right hand side as you cycle pipeline steps. 

Click on *Expand Artifacts*. Now, you can see expanded yellow boxes. These are Vertex AI artifacts that are created as a result of the previous step.

Feel free to explore the UI in more detail on your own!

Congratulations, intrepid ML explorer{% if MY_NAME %} {{ MY_NAME }}{% endif %}! 🚀 You've successfully wrangled data, trained models, and unleashed the power of Vertex AI. If your model underperforms, remember: it's not a bug—it's just an underfitting feature! Keep iterating, keep optimizing, and may your loss functions always converge. Happy coding! 🤖✨

{% if MDBOOK_VIEW %}

---

<div class="mdbook-alerts mdbook-alerts-caution">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  caution
</p>
<p>
Below you can find the content of <code>notebooks/bootkon_vertex.ipynb</code>. Feel free to skim over it, but please open it from your JupyterLab instance you created above.
</p>
</div>

{{ jupyter('notebooks/bootkon_vertex.ipynb') }}

{% endif %}