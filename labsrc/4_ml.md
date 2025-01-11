## Lab 4: ML Operations with Vertex AI

<walkthrough-tutorial-duration duration="60"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>

Original document: [here](https://docs.google.com/document/d/1UdI1ffZdjy--_2xNmemQKzPCRXvCVw8JAroZqewiPMs/edit?usp=drive_link)


***Note: You can start Hands-on Lab 5 while the Hands-on Lab 4 training jobs in Notebooks 2 & 3 are still running.***  

**Finally, we create a Vertex AI Notebook (JupyterLab)**

1. Go to Vertex AI in the GCP console.

      ![alt vertexai](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/vertexai.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/vertexai.png?raw=true" target="_parent">View image</a>

2. Click on the Workbench section.

      ![alt workbench](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/workbench.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/workbench.png?raw=true" target="_parent">View image</a>

3. Select “User managed notebooks” 

      ![alt usermanagednotebooks](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/usermanagednotebooks.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/usermanagednotebooks.png?raw=true" target="_parent">View image</a>

4.  “Create new”

      ![alt createnew](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/createnew.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/createnew.png?raw=true" target="_parent">View image</a>

   

5. Name the notebook “***bootkon***” and leave the default network and environment. Leave the cheapest machine type; e2-standard-4 selected; 4 vCPUs and 16GB of RAM are more than enough to perform the ML labs using jupyter notebooks. Do not attach a GPU. Normally it takes around 10 minutes to get the instance created.

   ![alt notebookbootkon](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/notebookbootkon.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/notebookbootkon.png?raw=true" target="_parent">View image</a>

6. Open the Jupyter Lab;

   ![alt openjupyter](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/openjupyter.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/openjupyter.png?raw=true" target="_parent">View image</a>

7. From the Jupyter Lab top menu, click on Git \-\> Clone a Repository 

   ![alt clonerepo](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo.png?raw=true" target="_parent">View image</a>

8. Enter [https://github.com/fhirschmann/bootkon-h2-2024.git](https://github.com/fhirschmann/bootkon-h2-2024.git) and click on **clone**

   ![alt clonerepo2](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo2.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo2.png?raw=true" target="_parent">View image</a>