## Lab 4: ML Operations with Vertex AI

<walkthrough-tutorial-duration duration="60"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>
<walkthrough-project-setup></walkthrough-project-setup>
<bootkon-cloud-shell-note/>

Original document: [here](https://docs.google.com/document/d/1UdI1ffZdjy--_2xNmemQKzPCRXvCVw8JAroZqewiPMs/edit?usp=drive_link)

In this lab, you will create a JupyterLab notebook and perform machine learning on the data set you previously ingested.

Create a Vertex AI Workbench instance:

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

Now, please open `notebooks/xxx.ipynb` and continue your journey.