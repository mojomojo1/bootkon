## Lab 1: Environment Setup

<walkthrough-tutorial-duration duration="30"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

In this lab we will set up your environment, download the data set for this bootkon, put it to Cloud storage,
and do a few other things.

### Enable services

First, we need to enable some Google Cloud Platform (GCP) services. Enabling GCP services is necessary to access and use the resources and capabilities associated with those services. Each GCP service provides a specific set of features for managing cloud infrastructure, data, AI models, and more. Enabling them takes a few minutes.

<walkthrough-enable-apis apis=
  "storage-component.googleapis.com,
  notebooks.googleapis.com,
  serviceusage.googleapis.com,
  cloudresourcemanager.googleapis.com,
  pubsub.googleapis.com,
  compute.googleapis.com,
  metastore.googleapis.com,
  datacatalog.googleapis.com,
  bigquery.googleapis.com,
  dataplex.googleapis.com,
  datalineage.googleapis.com,
  dataform.googleapis.com,
  dataproc.googleapis.com,
  bigqueryconnection.googleapis.com,
  aiplatform.googleapis.com,
  artifactregistry.googleapis.com">
</walkthrough-enable-apis>

### Download data

Next, we download the data set for bootkon and put it into Cloud Storage. Before we do that, we create
a bucket where we place the data into. Let's name it ``{{ PROJECT_ID }}-bucket``:
```bash
gsutil mb -l $REGION gs://{{ PROJECT_ID }}-bucket
```

Next, we download the data from GitHub and extract it (all in one line):
```bash
wget -qO - https://github.com/fhirschmann/bootkon-data/releases/download/v1.3/data.tar.gz | tar xvzf -
```

Let's upload the data to the bucket we just created:
```bash
gsutil -m cp -R bootkon-data/* gs://$PROJECT_ID-bucket/
```

Is the data there? Let's check and open [Cloud Storage](https://console.cloud.google.com/storage/browser/astute-ace-336608-bucket). Once you have checked, you may need to resize the window that just opened
to make it smaller in case you run out of screen real estate.

### Create default VPC

The Google Cloud environment we created for you does not come with a Virtual Private Cloud (VPC) network
created by default. Let's create one:

```bash
gcloud compute networks create default --project=$PROJECT_ID --subnet-mode=auto --bgp-routing-mode="regional"
gcloud compute networks subnets update default --region=$REGION --enable-private-ip-google-access
gcloud compute firewall-rules create "default-allow-all-internal" \
    --network="default" \
    --project=$PROJECT_ID \
    --direction=INGRESS \
    --priority=65534 \
    --source-ranges="10.128.0.0/9" \
    --allow=tcp:0-65535,udp:0-65535,icmp
```

Have a look at <walkthrough-editor-open-file filePath=".scripts/bk-bootstrap">`bk-bootstrap`</walkthrough-editor-open-file> and what it does; exeucte it:
```bash
bk-bootstrap
```

<walkthrough-spotlight-pointer locator="semantic({tab 'Gemini Code Assist'})"></walkthrough-spotlight-pointer>

### Success

🎉 Congratulations{% if MY_NAME %}, {{ MY_NAME }}{% endif %}! You've officially leveled up from "cloud-curious" to "GCP aware"! 🌩️🚀

