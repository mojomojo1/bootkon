## Lab 5: Data governance with Dataplex

<walkthrough-tutorial-duration duration="60"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

In this lab you will 
- Understand Dataplex product capabilities
- Leverage Dataplex features to better understand, govern your data and metadata.
- Build data quality checks on top of the fraud detection prediction results.

About Dataplex

With Dataplex you can organize different data assets, from different projects under new organizational concepts of Lakes and Zones. Organization is logical only and does not require any data movement.  Dataplex supports managing datasets in BigQuery and GCS buckets.  You can use lakes to define your organizational boundary or regional boundary  (e.g. marketing lake/sales lake Or  US lake/ UK lake etc), while zones can be used to group the data logically or by use cases (e.g. raw_zone/curated_zone or analytics_zone/data_science_zone).
Dataplex can also be used to build a data mesh architecture with decentralized data ownership among domain data owners.

Security - GCS / BQ

With Dataplex you can apply data access permissions using IAM groups across multiple buckets and BQ datasets by granting permissions at a lake or zone-level. Dataplex will do the heavy lifting of propagating desired policies and updating access policies of the buckets/datasets  that are part of that lake or data zone. Dataplex will also apply those permissions to any new buckets/datasets that get created under that data zone. This takes away the need to manually manage individual bucket permissions and also provides a way to automatically apply permissions to any new data added to your lakes.

Note that the permissions are applied in “Additive” fashion. I.e. Dataplex does not replace the existing permissions when pushing down permissions. Dataplex also provides “exclusive” permission push down as an opt-in feature.
Discovery [semi structured and structured data].

You can configure discovery jobs in Dataplex that can sample data on GCS, infer its schema, and automatically register it with Data Catalog so you can easily search and discover the data you have in your lakes.
In addition to registering metadata with Data Catalog, for data in CSV, JSON, AVRO, ORC, and Parquet formats, the discovery jobs also register technical metadata, including hive-style partitions, with a managed Hive metastore (Dataproc Metastore) & as external tables in BigQuery(BQ).  Discovery jobs can be configured to run on a schedule to discover any new tables or partitions. For new partitions, discovery jobs incrementally scan new data, check for data and schema compatibility, and register only compatible schema to the Hive metastore/ BQ so that your table definitions never go out of sync with your data.

Actions - Profiling, Quality, Lineage, Discovery

Dataplex has the capability to profile data assets (BigQuery tables), auto detect data lineage for BigQuery transformations. You can also use Dataplex for data discovery across GCS, BigQuery, Spanner, PubSub, Dataproc metastore, Bigtable and Vertex AI models. Dataplex automatic data quality, which lets you define and measure the quality of your data. You can automate the scanning of data, validate data against defined rules, and log alerts if your data doesn't meet quality requirements. You can manage data quality rules and deployments as code, improving the integrity of data production pipelines.

--- 

### LAB Section: Create a Dataplex Lake

1. Enable the Dataplex, Dataproc, Dataproc Metastore, Data Catalog, BigQuery, and Cloud Storage. APIs.  (you can skip this step if you completed LAB 1)
2. Make sure you have the predefined roles roles/dataplex.admin or roles/dataplex.editor granted to you so that you can create and manage your lake. (you can skip this step if you completed LAB 1)
3. Go to Dataplex in the Google Cloud console or search for it from the search section of the GCP console.
**IMAGE**
4. Navigate to the Manage view.
5. Click Create Lake.
6. Enter a Display name. For example: bootkon-lake
The lake ID is automatically generated for you. If you prefer, you can provide your own ID.
7. Optional: Enter a Description. For Example: Dataplex Lake for bootkon data assets
8. Specify the Region where the GCS buckets and BigQuery datasets were created during previous Labs. If you have followed the previous Labs, it should be us-central1. Ensure that the region is consistent with the locations used in prior steps.

9. Optional: Add labels to your lake. For example, use location for the key and berlin for the value.
10. Lets skip the metastore creation for now and click on create. 
    The creation should take 2-3 minutes to finish.
**IMAGE** 

***

#### LAB Section: Add Dataplex Zones

We will add 2 zones; one for raw zone and another one for curated zone.

1. Click on the bootkon-lake lake you just created.
2. In the Zones tab, click + Add zone.
3. Enter a Display name for your zone. For example ; bootkon-raw-zone
4. Click the Type drop-down. Choose Raw Zone. Learn more about supported zone types.
5. Optional: Enter a description. For example, Dataplex zone for bootkon raw data assets
6. Under Data locations, select either Regional or Multi-regional. The region has to match where the GCS buckets and BigQuery datasets were created during previous Labs. If you have followed the previous Labs, it should be Regional us-central1.
7. Add labels to your zone. For example, use zone for the key and raw for the value.
8. Enable metadata discovery, which allows Dataplex to automatically scan and extract metadata from the data in your zone. Let's leave the default settings. 
9. Expand the Discovery settings submenu.
10. Make sure Enable metadata discovery is selected.
11. Optional: Under Include patterns, list the files to include in the discovery scans.
Important: Under Exclude patterns, list the files to exclude from the discovery scans. If you enter both include and exclude patterns, exclude patterns are applied first. Exclude the source code files by specifying **/src/*.
12. Click the Repeats drop-down and select a frequency.
13. Click the Timezone drop-down and select a timezone (for example: Germany).
14. If under Repeats you selected Custom, under Schedule, enter a job schedule. Otherwise, the Schedule value is automatically filled for you.
15. Click Create.
16. When the zone creation succeeds, the zone automatically enters an active state. If it fails, then the lake is rolled back to its previous state.
After you create your zone, you can map data stored in Cloud Storage buckets and BigQuery datasets as assets in your zone.
Repeat the same steps from 1 to 11 but this time, change the display name to bootkon-curated-zone and choose Choose Curated Zone for the Type. You might also change the label and description values. 
The creation should take 2-3 minutes to finish.

---

### LAB Section: Add Zone Data Assets
Lets map data stored in Cloud Storage buckets and BigQuery datasets as assets in your zone.
1. Click on bootkon-raw-zone
2. Click on + ADD ASSETS
3. Click on ADD AN ASSET
4. Choose storage bucket
5. Display name : bootkon-gcs-raw-asset
6. Optionally add a description 
7. Browse the bucket name and choose the bucket created in LAB 1. If you followed the instructions, it should be named <your project id>-bucket.
8. Select the bucket
9. Let's skip upgrading to the managed option. When you upgrade a Cloud Storage bucket asset, Dataplex removes the attached external tables and creates BigLake tables. We have already created in LAB 2 biglake table so this option is not necessary. 
10. Optionally add a label
11. Click on continue
12. Leave the discovery setting to be inherited by the lake settings we have just created during lake creation steps. Click on continue.
13. Click on submit. 
*IMAGE*
Lets add another data assets but for the bootkon-curated-zone
14. Click on bootkon-curated-zone
15. Click on + ADD ASSETS
16. Click on ADD AN ASSET
17. Choose BigQuery Dataset
18. Display name : bootkon-bq-curated-asset
19. Optionally add a description 
20. Browse the BigQuery Dataset and choose the dataset created in LAB 1. If you followed the instructions, it should be named ml_datasets.
21. Select the  BigQuery Dataset
22. Optionally add a label
23. Click on continue
24. Leave the discovery setting to be inherited by the lake settings we have just created during lake creation steps. Click on continue.
25. Click on submit. 

*IMAGE*

---

### LAB Section: Explore data assets with Dataplex Search 

During this lab go to the Search section of the Dataplex and search for the lakes, zones and assets you just created. Spend 5 minutes exploring before moving to the next LAB.

---

### LAB Section: Explore Biglake object tables created automatically by Dataplex in BigQuey

As a result of the data discovery (takes up to approximately 5 minutes), notice a new BigQuery dataset created called “bootkon_raw_zone” under the BigQuery console section. New Biglake tables were automatically created by Dataplex discovery jobs. During the next sections of the labs, we will be using the data_prediction biglake table. 

During previous machine learning with Vertex AI lab, we discussed that batch prediction jobs may take more than 2 hours to complete. Therefore, we made available the results of the job prediction in parquet files here. Ensure these files were already copied into your GCS bucket <gcp project id>-bucket during Lab1.

---

### LAB Section: Data Profiling

Dataplex data profiling lets you identify common statistical characteristics of the columns in your BigQuery tables. This information helps you to understand and analyze your data more effectively.
Information like typical data values, data distribution, and null counts can accelerate analysis. When combined with data classification, data profiling can detect data classes or sensitive information that, in turn, can enable access control policies.
Dataplex also uses this information to recommend rules for data quality checks.
Dataplex lets you better understand the profile of your data by creating a data profiling scan.
The following diagram shows how Dataplex scans data to report on statistical characteristics.

---

Configuration options
This section describes the configuration options available for running data profiling scans.

Scheduling options

You can schedule a data profiling scan with a defined frequency or on demand through the API or the Google Cloud console.

Scope

As part of the specification of a data profiling scan, you can specify the scope of a job as one of the following options:
* Full table: The entire table is scanned in the data profiling scan. Sampling, row filters, and column filters are applied on the entire table before calculating the profiling statistics.
* Incremental: Incremental data that you specify is scanned in the data profile scan. Specify a Date or Timestamp column in the table to be used as an increment. Typically, this is the column on which the table is partitioned. Sampling, row filters, and column filters are applied on the incremental data before calculating the profiling statistics.

Filter data

You can filter data to be scanned for profiling by using row filters and column filters. Using filters helps you reduce the execution time and cost, and exclude sensitive and unuseful data.
* Row filters: Row filters let you focus on data within a specific time period or from a specific segment, such as region. For example, you can filter out data with a timestamp before a certain date.
* Column filters: Column filters lets you include and exclude specific columns from your table to run the data profiling scan.

Sample data

Dataplex lets you specify a percentage of records from your data to sample for running a data profiling scan. Creating data profiling scans on a smaller sample of data can reduce the execution time and cost of querying the entire dataset.

---

Lab Instructions

1. Go to Profile section in Dataplex
2. Click on +CREATE DATA PROFILE SCAN
3. Display Name: bootkon-dprofile-fraud-prediction for example 
4. Optionally add a description. For example, data profile scans for fraud detection predictions
5. Leave the “browse within dataplex lakes” option turned off
6. Click on browse to filter on data_prediction  bigquery table (Dataset: bootkon_raw_zone). 
*IMAGE*

7. Select data_prediction bigquery table
8. Choose “entire data” as scope of the data profiling job
9. Choose All data on sampling size
10. Turn on publishing option
11. Choose on demand schedule
12. Click on continue, leave the rest as default and click on create.

It will take a couple of minutes for the profiling to show up on the console.

*IMAGE*

13. Click on the bootkon-dprofile-fraud-prediction profile and click on RUN NOW. 
14. Click on Job ID and monitor the job execution. 
15. Notice what the job is doing. The Job should succeed in less than 10 minutes.
16. Explore the data profiling results of the CLASS column name. We have less than 0.1% of fraudulent transactions. Also notice that predicted_class of type RECORD were not fully  profiled, only the percentage of null and unique values were correctly profiled. Refer to the supported data types here.
*IMAGE*
17. As they train further and continuously the fraud detection ML models, data professionals would like to set up an automatic check on data quality and be notified when there are huge discrepancies between predicted_class  and CLASS values. This is where Dataplex data quality could help the team. 

---

### LAB Section: Setup Data Quality Jobs
After setting up the data profiling scan we have seen that we still have no clear visibility on fluctuation between predicted classes vs actual CLASS ratio. Our goal is to have a percentage of matched values between CLASS and predicted classes more than 99.99 %. Any lower percentage would indicate that we would have to further train the ML model or add more features or use another model architecture.

You can use the following SQL query in BigQuery to check the percentage of matched values between CLASS and predicted classes. 

*TABLE*
BigQuery SQL : Check the percentage of matched values between CLASS and predicted classes
Replace  your-project-id with your project id
CODECODECODE in a table

We will set up the Dataplex automatic data quality, which lets you define and measure the quality of your data. You can automate the scanning of data, validate data against defined rules, and log alerts if your data doesn't meet quality requirements. You can manage data quality rules and deployments as code, improving the integrity of data production pipelines.
During the previous lab, We got started by using Dataplex data profiling rule recommendations to drive initial conclusions on areas of attention. Dataplex provides monitoring, troubleshooting, and Cloud Logging alerting that's integrated with Dataplex auto data quality.

**Conceptual Model**

*IMAGE*

A data scan is a Dataplex job that samples data from BigQuery and Cloud Storage and infers various types of metadata. To measure the quality of a table using auto data quality, you create a DataScan object of type data quality. The scan runs on only one BigQuery table. The scan uses resources in a Google tenant project, so you don't need to set up your own infrastructure.
Creating and using a data quality scan consists of the following steps:
1. Rule definition
2. Rule execution
3. Monitoring and alerting
4. Troubleshooting


*Lab Instructions* 
1. Go to Data Quality section in Dataplex
2. Click on +CREATE DATA QUALITY SCAN
3. Display Name: bootkon-dquality-fraud-prediction for example 
4. Optionally add a description. For example, data quality scans for fraud detection predictions
5. Leave the “browse with dataplex lakes” option turned off 
6. Click on browse to filter on the data_prediction BigQuery table.(Dataset: bootkon_raw_zone). 
*IMAGE*
7. Select data_prediction bigquery table
8. Choose “entire data” as scope of the data profiling job
9. Choose All data on sampling size
10. Turn on publishing option
11. Choose on demand schedule
12. Click on continue,
13. Now lets define quality rules, click on ADD RULES > SQL Assertion Rule

*IMAGE*

14. Choose Accuracy as dimension 
15. Rule name: bootkon-dquality-ml-fraud-prediction
16. Description : regularly check the ML fraud detection prediction quality results 
17. Leave the column name empty
18. Provide the following SQL statement. Dataplex will utilize this SQL statement to create a SQL clause of the form SELECT COUNT(*) FROM (sql statement) to return success/failure. The assertion rule is passed if the returned assertion row count is 0.

*TABLE*

19. Click on ADD
20. Click on Continue
*IMAGE*
21. Run SCAN 
22. The display name may take a moment to appear on the screen.
23. Monitor the job execution. Notice the job succeeded but the rule failed because our model accuracy percentage on the whole data predicted does not exceed the 99.99% threshold that we set
*IMAGE*


Congratulations {% if MY_NAME %} {{ MY_NAME }}{% endif %} on completing Lab5 ! 🚀 You've successfuly set up data quality checks 🤖✨
You can now move on to Lab 6 for further practice. 🥳🥳

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