## Lab 3: Dataform

<walkthrough-tutorial-duration duration="45"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

Original document [here](https://docs.google.com/document/d/1NxfggQunrCn6ZfwGXAaA_lABDmXtRsfH88jkMDbqlJo/edit?usp=drive_link)

During this lab, you gather user feedback to assess the impact of model adjustments on real-world use (prediction), ensuring that our fraud detection system effectively balances accuracy with user satisfaction. 
* Use Dataform , BigQuery and Gemini to Perform sentiment analysis of customer feedback.

### **Dataform** 

Dataform is a fully managed service that helps data teams build, version control, and orchestrate SQL workflows in BigQuery. It provides an end-to-end experience for data transformation, including:

* Table definition: Dataform provides a central repository for managing table definitions, column descriptions, and data quality assertions. This makes it easy to keep track of your data schema and ensure that your data is consistent and reliable.  
* Dependency management: Dataform automatically manages the dependencies between your tables, ensuring that they are always processed in the correct order. This simplifies the development and maintenance of complex data pipelines.  
* Orchestration: Dataform orchestrates the execution of your SQL workflows, taking care of all the operational overhead. This frees you up to focus on developing and refining your data pipelines.

Dataform is built on top of Dataform Core, an open source SQL-based language for managing data transformations. Dataform Core provides a variety of features that make it easy to develop and maintain data pipelines, including:

* Incremental updates: Dataform Core can incrementally update your tables, only processing the data that has changed since the last update. This can significantly improve the performance and scalability of your data pipelines.  
* Slowly changing dimensions: Dataform Core provides built-in support for slowly changing dimensions, which are a common type of data in data warehouses. This simplifies the development and maintenance of data pipelines that involve slowly changing dimensions.  
* Reusable code: Dataform Core allows you to write reusable code in JavaScript, which can be used to implement complex data transformations and workflows.

Dataform is integrated with a variety of other Google Cloud services, including GitHub, GitLab, Cloud Composer, and Workflows. This makes it easy to integrate Dataform with your existing development and orchestration workflows.  
Benefits of using Dataform in Google Cloud  
There are many benefits to using Dataform in Google Cloud, including:

* Increased productivity: Dataform can help you to increase the productivity of your data team by automating the development, testing, and execution of data pipelines.  
* Improved data quality: Dataform can help you to improve the quality of your data by providing a central repository for managing table definitions, column descriptions, and data quality assertions.  
* Reduced costs: Dataform can help you to reduce the costs associated with data processing by optimizing the execution of your SQL workflows.  
* Increased scalability: Dataform can help you to scale your data pipelines to meet the needs of your growing business.

### **Use cases for Dataform**

Dataform can be used for a variety of use cases, including:

* Data Warehousing: Dataform can be used to build and maintain data warehouses that are scalable and reliable.  
* Data Engineering: Dataform can be used to develop and maintain data pipelines that transform and load data into data warehouses.  
* Data Analytics: Dataform can be used to develop and maintain data pipelines that prepare data for analysis.  
* Machine Learning: Dataform can be used to develop and maintain data pipelines that prepare data for machine learning models.

### ***LAB Section : Dataform Prerequisites*** 

### **Using Large Language Models from Vertex AI  (info only)**

Google Cloud’s language models are available within the Vertex AI Studio inside the Vertex AI service.  
**![][image3]**

5. ### **Prompt design (info only)**

Prompt design is the process of creating prompts that elicit the desired response from language models. Writing well structured prompts is an essential part of ensuring accurate, high quality responses from a language model.  
If you need to understand this concept a bit more this is a page that introduces some basic concepts, strategies, and best practices to get you started in designing prompts ([https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)).  
The reference page above also goes into the more advanced settings you can see on the right hand side of the prompt box such as temperature, top K, top P etc.

### ***LAB Section : Creating a Dataform Pipeline***

First step in implementing a pipeline in Dataform is to set up a repository and a development environment. Detailed quickstart and instructions can be found [here](https://cloud.google.com/dataform/docs/quickstart-create-workflow).

Navigate to the BigQuery section in the Google Cloud Platform console, and then select Dataform.  
![][image4]

1. ### **Create a Repository in Dataform** 

Click the “+ CREATE REPOSITORY” button near the top of the page.  
![][image5]  
Use the following values when creating the repository:

- Repository ID: “hackathon-repository”  
- Region: (us-central1)  
- Service Account: (Default Dataform service account)  
  ![][image6]

And click “CREATE”

2. ### **Dataform Service Account** 

Take note and save somewhere the newly created service account for Dataform.  
Example: service-112412469323@gcp-sa-dataform.iam.gserviceaccount.com

![][image7]  
Click “GO TO REPOSITORIES”, and then click on the “hackathon-repository”, the new repository you just created.  
![][image8]

3. ### **Create and initialize a Dataform development workspace**

You should now be in the “DEVELOPMENT WORKSPACES” tab of the hackathon-repository page.

1. Click add **Create development workspace**.  
2. In the **Create development workspace** window, do the following:  
   1. In the **Workspace ID** field, enter “hackathon-\<YOURLASTNAME\>-workspace” (replace \<YOURLASTNAME\> with your name)  
   2. Click **Create**.  
3. The development workspace page appears.  
4. Click on the newly created development workspace   
5. Click **Initialize workspace**.

6. You will copy the dataform files from the following repository, in the next steps.   
   [https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform](https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform)   
7. *Edit  **workflow\_settings.yaml** file :*   
* *Replace defaultDataset value with **ml\_datasets ,***   
* make sure defaultProject value is ***your project id***   
  ***Note:*** Nevermind if you have a different dataform core version, just continue

  *![][image9]*  
* Click on Install Packages ***Only*** ***Once***. You should see a message at the bottom of the page:

  *Package installation succeeded*

8. *Remove the default auto-generated SQLX files; Delete the following files from the “definitions” folder:*  
* *first\_view.sqlx*  
* *second\_view.sqlx*

  *![][image10]*

9. *Click on definitions and create a new directory called “models”:* 

   *![][image11]*

10. *Click on models directory and create 2 new files ;  (make sure all file names are in lowercase and avoid adding spaces to the file names)*  
* [create\_dataset.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/models/create_dataset.sqlx)  
* [llm\_model\_connection.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/models/llm_model_connection.sqlx)

	  
Those files should be created under ***definitions/models*** directory

*Example:*

*![][image12]*

11. *Copy the contents from [https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions/models](https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions/models)  to each of those files.*  
12. *Click on definitions and create 3 new files: (make sure all file names are in lowercase and avoid adding spaces to the file names)*  
* [mview\_ulb\_fraud\_detection.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/mview_ulb_fraud_detection.sqlx)  
* [sentiment\_inference.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/sentiment_inference.sqlx)  
* [ulb\_fraud\_detection.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/ulb_fraud_detection.sqlx)


Those files should be created under ***definitions*** directory

*Example:* 

*![][image13]*

13. *Copy the contents from [https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions](https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions) to each of those files.*  
14. *Set the database value to your project ID value in ulb\_fraud\_detection.sqlx file:*

    *![][image14]*

15. *In llm\_model\_connection.sqlx, replace the \`us.llm-connection\` connection with the connection name you have created in LAB 2 during the BigLake section.  If you have followed the steps in LAB 2, the connected name should be “**us.fraud-transactions-conn***”  
    Notice the usage of $ref in line 11, of ***definitions/mview\_ulb\_fraud\_detection.sqlx***  
     “sqlx” file. The advantages of using $ref in Dataform are

* Automatic Reference Management: Ensures correct fully-qualified names for tables and views, avoiding hardcoding and simplifying environment configuration.  
* Dependency Tracking: Builds a dependency graph, ensuring correct creation order and automatic updates when referenced tables change.  
* Enhanced Maintainability: Supports modular and reusable SQL scripts, making the codebase easier to maintain and less error-prone.

5. *Run the dataset creation by TAG. TAG allows you to just execute parts of the workflows and not the entire workflow. Click on Start Execution \> Tags \> "dataset\_ulb\_fraud\_detection\_llm” \> Start Execution*  
   

   *![][image15]*  
6. *Click on Details;*

   *![][image16]*

7. *Notice the Access Denied error on BigQuery for the dataform service account XXX@gcp-sa-dataform.iam.gserviceaccount.com;*

   *![][image17]*

8.  Go to IAM & Admin  \> Grant access and grant ***BigQuery Data Editor , BigQuery Job User and BigQuery Connection User***  to the data from the service account.  Click on Save.


   ![][image18]

   ***Note:*** If you encounter the following policy update screen, just click on update.

   ![][image19]

9. Go back to dataform from the BigQuery console, and retry step ***5***. Notice the execution status. It should be a success.  
   ![][image20]  
10. Click on Compiled graph and explore it;  
    Go to ***Dataform \> hackathon-\<lastname\>-workspace \> Compiled Graph***  
    ![][image21]

### ***LAB Section : Execute the workspace workflow***

1. For  the sentiment inference step to succeed . You need to grant the external connection service account the Vertex AI user privilege. More details can be found in this [link](https://cloud.google.com/bigquery/docs/generate-text-tutorial#grant-permissions). You can find the service account ID under BigQuery Studio \> Your project ID  (example: bootkon-dryrun24ber-886) \> External connections \> fraud-transactions-conn  
     
   ![][image22]  
    ![][image23]

2. Take note of the service account and grant it the ***Vertex AI User*** role.   
   ![][image24]  
     
3. *Back in your Dataform workspace, click **START EXECUTION** from the top menu, then* **“Execute actions”***.*  
   ![][image25]  
4. Click on ***ALL ACTIONS*** Tab then Click on ***START EXECUTION***  
   ![][image26]

5. Check the execution status. It should be a success.  
6. Verify the new table **sentiment\_inference** in the ml\_datasets dataset in BigQuery.  
7. Query the BigQuery table content (At this point you should be familiar with running BigQuery SQL)  
   

| *BigQuery SQL : Check few rows of* sentiment\_inference table |
| :---- |

```
SELECT distinct ml_generate_text_llm_result,
prompt,
Feedback
FROM `ml_datasets.sentiment_inference` LIMIT 10;
```
   

8. **\[Max 2 minutes\]** Discuss the table results within your team group.

9. Before moving to the challenge section of the Lab, go back to the CODE section of the Dataform workspace. At the top of the “Files” section on the left, click ***“Commit X Changes”*** (X should be about 7), add a commit message like, “Bootkon Lab 3”, then click “***Commit all files***” and then ***“Push to Default Branch”***   
   ***![][image27]***

You should now have the message   
***![][image28]***

# ***CHALLENGE Section : Production, Scheduling and Automation*** 

Automate and schedule the compilation and execution of the pipeline. This is done using release configurations and workflow configurations.

***Release Configurations:***  
Release configurations allow you to compile your pipeline code at specific intervals that suit your use case. You can define:

* Branch, Tag, or Commit SHA: Specify which version of your code to use.  
* Frequency: Set how often the compilation should occur, such as daily or weekly.  
* Compilation Overrides: Use settings for testing and development, such as running the pipeline in an isolated project or dataset/table.  
    
  Common practice includes setting up release configurations for both test and production environments. For more information, refer to the [release configuration documentation](https://cloud.google.com/dataform/docs/release-configurations).  
    
  **Workflow Configurations**  
    
  To execute a pipeline based on your specifications and code structure, you need to set up a workflow configuration. This acts as a scheduler where you define:  
    
* Release Configuration: Choose the release configuration to use.  
* Frequency: Set how often the pipeline should run.  
* Actions to Execute: Specify what actions to perform during each run.

  The pipeline will run at the defined frequency using the compiled code from the specified release configuration. For more information, refer to the [workflow configurations documentation](https://cloud.google.com/dataform/docs/workflow-configurations).

  *\[TASK\] Challenge : Take up to 10 minutes to Setup a Daily Frequency Execution of the Workflow*


  ***Goal:*** Set up a daily schedule to automate and execute the workflow you created.

1. Automate and schedule the pipeline’s compilation and execution.  
2. Define release configurations for one production environment (optionally: you can create another one for dev environment)  
3. Set up workflow configurations to schedule pipeline execution (use dataform service account).  
4. Set up a 3 minute frequency execution of the workflow you have created.  
     
     
   ***Note:*** If you are stuck and cannot figure out how to proceed after a few minutes, ask the event moderator for help.

**🥳🥳Congratulations on completing Lab 3\!**   
**You can now move on to Lab 4 for further practice. 🥳🥳**  




# **\<Lunch Time: 60 Minutes\>**