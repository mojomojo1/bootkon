## Lab 1: Environment Setup

<walkthrough-tutorial-duration duration="30"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

In this lab you will grant permissions and set up a default VPC network as a preparatory step.

### **Choice of GCP Product and Service Location**

You are free to choose any GCP region location for your labs. Ensure all your resources are created in the chosen location to avoid connectivity issues and minimize latency and cost. If you don’t have a preferred GCP location, use ***us-central1*** for simplicity.

### **Setup your environment**

Open `vars.sh` <walkthrough-editor-open-file filePath="vars.sh"> in the Cloud Shell editor </walkthrough-editor-open-file> and adapt it. Don't forget to save it.

Now, export the variables to your environment:
```bash
source vars.sh
```

Verify that they have been set correctly:
```bash
echo "PROJECT_ID=$PROJECT_ID REGION=$REGION GCP_USERNAME=$GCP_USERNAME"
```

Please also select your project in the next widget and ignore the comment about creating a new project.

<walkthrough-project-setup></walkthrough-project-setup>

Have a <walkthrough-editor-open-file filePath="bootstrap.sh">look</walkthrough-editor-open-file> at the bootstrap script and what it does; exeucte it:
```bash
./bootstrap.sh
```

Well done, your environment is now ready for the first lab!
