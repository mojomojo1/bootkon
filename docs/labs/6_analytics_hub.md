## Lab 6: Analytics Hub

{{ GCP_USERNAME }}

<walkthrough-tutorial-duration duration="45"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>

Within this lab, you will share the machine learning prediction results to the FraudFix customer while keeping the data securely within the provider's storage environment. Here, you will focus on avoiding sharing PII data. 

### Goal of the Lab
* We have previously created the fraud detection model predictions.   
* After running the dataplex  data discovery job , we noticed a new BigQuery dataset created called ***“bootkon\_raw\_zone”*** , ***data\_prediction*** biglake table were automatically created by Dataplex discovery jobs.  
* The goal of the ***FraudFix*** data scientist team  is to share the results of the data prediction with the customer.  
* The customer will use the PCA data and perform reversed PCA in order to get the result of the predictions.  
* The customer will also use the explainability results from the ***data\_prediction*** data to understand why the decisions have been made to flag a given transaction as fraudulent or not.  
* There is a small caveat, the  ***data\_prediction*** biglake table has the email address of the service account or user who has performed the machine learning tasks. This information is considered PII data (Personal Identifiable Information). In addition you should not share the auto generated transaction id that you have added during the machine learning labs.  
* Data clean room within the Data Analytics Hub will allow you to share the data securely and without leaking any PII information.   
* You have been assigned a group of work. Each group member will play the role of a data provider and a data subscriber of the other group members.    
* You are a data publisher and data subscriber. You are publishing the results of your data prediction and you are subscribing to other team member data prediction.  
* Collect the GCP account addresses of the your group members assigned to you, in order to set up privileges and share the data with them.


### LAB Section : Hands-on on Analytics Hub (Data Clean Room) capabilities

Steps as Data Publisher :
The Data Publisher in this case is the FraudFix technology. They are providers of data prediction results and model prediction explainability.


1. Create a dataset: `ml_datasets_clean_room`  which is for the Authorized View. Authorized View is always recommended over table for enforcing the [privacy policy](https://cloud.google.com/bigquery/docs/privacy-policies). Note how one of the columns are declared as private and put a limit on the lower limit on the aggregated results.  
   The dataset should be in the same region as `bootkon_raw_zone` dataset that Dataplex has created before.
   
   ```bash
   dataset_name='ml_datasets_clean_room'
   bq mk --location=us-central1 \
      --dataset \
      --description "Shared ml dataset" \
      "$dataset_name"
   ```

2. Define an aggregation threshold analysis rule for a view. An aggregation threshold rule for a view requires a minimum number of distinct entities (e.g., users) in a dataset before statistics are included in query results.  It groups data, counts distinct entities within each group, and only returns groups meeting the minimum threshold. 
   A view that includes this analysis rule can also include the [joint restriction analysis rule](https://cloud.google.com/bigquery/docs/analysis-rules#join_restriction_rules).  
   You can define an aggregation threshold analysis rule for a view in a [data clean room](https://cloud.google.com/bigquery/docs/data-clean-rooms) or with the following statement:  
   
   ```
   CREATE OR REPLACE VIEW {{ PROJECT_ID }}.ml_datasets_clean_room.data_prediction_shared
   OPTIONS(
   privacy_policy= '{"aggregation_threshold_policy": {"threshold": 1, "privacy_unit_column": "service_account_email"}}'
   )
   AS ( SELECT * EXCEPT (transaction_id) FROM `{{ PROJECT_ID }}.bootkon_raw_zone.data_prediction` );
   ```

   THRESHOLD: The minimum number of distinct privacy units that need to contribute to each row in the query results. If a potential row doesn't satisfy this threshold, that row is omitted from the query results.

   PRIVACY\_UNIT\_COLUMN: Represents the privacy unit column. A privacy unit column is a unique identifier for a privacy unit. A privacy unit is a value from the privacy unit column that represents the entity in a set of data that is being protected. You can use only one privacy unit column, and the data type for the privacy unit column must be [groupable](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#groupable_data_types). The values in the privacy unit column cannot be directly projected through a query, and you can use only [analysis rule-supported aggregate functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#agg_threshold_policy_functions) to aggregate the data in this column.

3. Try the following query in BigQuery without specifying the without an aggregation threshold 

   ```
   SELECT * 
   FROM `{{ PROJECT_ID }}.ml_datasets_clean_room.data_prediction_shared` 
   LIMIT 1000
   ````

   Note the error: You must use SELECT WITH AGGREGATION\_THRESHOLD for this query because a privacy policy has been set by a data owner.

4. Got to [Analytics Hub](https://console.cloud.google.com/bigquery/analytics-hub/exchanges) and click on <walkthrough-spotlight-pointer locator="semantic({toolbar 'Analytics Hub'} {button 'Create clean room'})">+ CREATE CLEAN ROOM</walkthrough-spotlight-pointer>

5. Create a Data Clean room called `fraudfix-clean-room-{{ GCP_USERNAME_SHORT }}` in the same region as the ***ml\_datasets\_clean\_room*** dataset (**typically us-central1)**. For the primary contact, use your GCP email address provided to you. For the description, you can use *‘Fraudfix shareable fraud detection ML results (yourlastname)’.* Click on create clean room.

   ![][image5]

6. Add your GCP email address in the clean room owner field. Add the ***subscriber*** GCP group member email address in both data contributors and subscribers fields, then click on <walkthrough-spotlight-pointer locator="semantic({button 'Create clean room'})">SET PERMISSIONS</walkthrough-spotlight-pointer> 
   
7. Notice the failed permissions   
   
   ![](../img/lab6/setpermissions.png)

8. After adding the Analytics Hub Admin role to ***your GCP user***,   
   ![](../img/lab6/analyticshubadmin.png)
     
9. Try setting permissions again in step 6\. Now, the permissions should be set correctly.

10. In the clean room, <walkthrough-spotlight-pointer locator="semantic({button 'Add data'})">ADD DATA</walkthrough-spotlight-pointer>. Specify the dataset name `<your project id_ml_datasets_clean_room` and add the Auth View `data_prediction_shared`. Primary contact should be your GCP user. For the description, you can use *‘Fraudfix shareable fraud detection ML results (yourlastname)’.*

11. Click on <walkthrough-spotlight-pointer locator="semantic({button 'Next'})">NEXT</walkthrough-spotlight-pointer>.  
12. Notice the privacy unit column is auto detected by the Analytics Hub.   
13. Let ‘s  allow the subscribers to join data on all columns except the service account email which is a PII data.

   ![](../img/lab6/joinallcolumns.png)

      
14. Choose the join condition not required.  

15. ***Data egress controls*** : Notice you can also disable copy and export of query results.  [Data egress](https://cloud.google.com/bigquery/docs/analytics-hub-introduction#data_egress) controls are automatically enabled to help prevent subscribers from copying and exporting raw data from a data clean room. Data contributors can configure additional controls to help prevent the copy and export of query results that are obtained by the subscribers.

16. Review and click on <walkthrough-spotlight-pointer locator="semantic({button 'Add data'})">ADD DATA</walkthrough-spotlight-pointer> 

17. Review the clean room you just created. Especially those who are allowed to subscribe to it. You can always add new principals when needed. 
 
   ![](../img/lab6/editsubscribers.png)

18. Since the table you want to share is in BigLake table format, grant the `Storage Object Viewer` role to the ***subscriber*** email address. Go to IAM and perform the steps

   ![](../img/lab6/storageobjectviewer.png)


### Steps as Data Subscriber:

The Data Subscriber in this case is FraudFix’s customer. The customer is the owner of the original PCA dataset provided to FraudFix.  
 

1. Go to [Analytics Hub](https://console.cloud.google.com/bigquery/analytics-hub/exchanges) in BigQuery and search for Listings by ‘***Clean rooms***’. The listings shared with you by other group members might take a few minutes to appear.  
* Click on <walkthrough-spotlight-pointer locator="semantic({button 'Search listings'})">SEARCH LISTINGS</walkthrough-spotlight-pointer>  
    
* Then check <walkthrough-spotlight-pointer locator="semantic({checkbox 'Private'})">Private Listings</walkthrough-spotlight-pointer> box from the Filters menu  
    
* The results will show the clean rooms shared with you by the other team members. 

For the remaining steps, we will be working with ***only one***  clean room shared in your listings, so choose ***any*** of the shared clean rooms available to you.  
![][image21]

* Now click on the clean room and click on ***SUBSCRIBE***


  **![][image22]**


* Add the shared dataset to your BigQuery project id environment by clicking again on ***SUBSCRIBE.*** The destination project should be your project id.

  ![][image23]

* Notice the message   
  ![][image24]  
2. Go to BigQuery Studio, Notice the data clean room that the other team members have just shared with you.   
     
   ![][image25]  
     
3. Try to select \* from the shared table. Note the error;   
   *You must use SELECT WITH AGGREGATION\_THRESHOLD for this query because a privacy policy has been set by a data owner.*  
4.  Try to run a simple aggregation but it will fail to do so as the SQL query must be started with  SELECT WITH AGGREGATION\_THRESHOLD  
5. Run the following query to analyze the results when the predicted class value is different from the actual class value.


| *BigQuery SQL : Analyze the results when the predicted class value is different from the actual class value* Replace *your-gcp-project-id* with your GCP project id as a subscriber Replace fraudfix\_clean\_room\_X with the data clean room name shared with you  |
| :---- |
| SELECT class, classes, scores from ( SELECT WITH AGGREGATION\_THRESHOLD   class,   ARRAY(     SELECT  AS STRUCT classes, scores     FROM UNNEST(predicted\_class.classes) classes WITH OFFSET AS pos     JOIN UNNEST(predicted\_class.scores) scores WITH OFFSET AS pos2     ON pos \= pos2     ORDER BY scores DESC     LIMIT 1   )\[OFFSET(0)\].\*, FROM   \`***your-gcp-project-id***.**fraudfix\_clean\_room\_X**.data\_prediction\_shared\` GROUP BY class, classes, scores ) where class \<\> classes order by scores desc |

   

6. *Try to include the privacy column in your query.*    
   

| *BigQuery SQL : As a data consumer , try to query PII field* Replace *your-gcp-project-id* with your GCP project id as a subscriber Replace fraudfix\_clean\_room\_X with the data clean room name shared with you  |
| :---- |
| *SELECT service\_account\_email, class, classes, scores from ( SELECT WITH AGGREGATION\_THRESHOLD   class,   service\_account\_email,   ARRAY(     SELECT  AS STRUCT classes, scores     FROM UNNEST(predicted\_class.classes) classes WITH OFFSET AS pos     JOIN UNNEST(predicted\_class.scores) scores WITH OFFSET AS pos2     ON pos \= pos2     ORDER BY scores DESC     LIMIT 1   )\[OFFSET(0)\].\*, FROM   \`**your-gcp-project-id***.**fraudfix\_clean\_room\_X***.data\_prediction\_shared\` GROUP BY  service\_account\_email, class, classes, scores ) where class \<\> classes order by scores desc* |

   

7. *Note the error : You cannot GROUP BY privacy unit column when using SELECT WITH AGGREGATION\_THRESHOLD*   
8. Run the following SQL query to know which ***attributes*** ***(or features)*** are influencing the model’s decision on flagging transactions as fraudulent (those having highest attribution values)   
   

| *BigQuery SQL : Find the most influential attributes to the  model decision*  Replace *your-gcp-project-id* with your GCP project id as a subscriber Replace fraudfix\_clean\_room\_X with the data clean room name shared with you  |
| :---- |
| *WITH RankedPredictions AS (  SELECT WITH AGGREGATION\_THRESHOLD    class,    Time,    ARRAY(      SELECT AS STRUCT classes, scores      FROM UNNEST(predicted\_Class.classes) classes WITH OFFSET AS pos      JOIN UNNEST(predicted\_Class.scores) scores WITH OFFSET AS pos2      ON pos \= pos2      ORDER BY scores DESC      LIMIT 1    )\[OFFSET(0)\].\*  FROM    \`**your-gcp-project-id***.**fraudfix\_clean\_room\_X***.data\_prediction\_shared\`    GROUP BY Time, class, classes, scores ), FilteredRankedPredictions AS (  SELECT    Time,    class,    classes AS predicted\_class,    scores AS predicted\_score  FROM    RankedPredictions  WHERE    classes \= '1' ), AttributionAverages AS (  SELECT WITH AGGREGATION\_THRESHOLD    AVG(ABS(attribution.featureAttributions.Time)) AS Avg\_Time\_Attribution,    AVG(ABS(attribution.featureAttributions.V1)) AS Avg\_V1\_Attribution,    AVG(ABS(attribution.featureAttributions.V2)) AS Avg\_V2\_Attribution,   AVG(ABS(attribution.featureAttributions.V3)) AS Avg\_V3\_Attribution,   AVG(ABS(attribution.featureAttributions.V4)) AS Avg\_V4\_Attribution,   AVG(ABS(attribution.featureAttributions.V5)) AS Avg\_V5\_Attribution,   AVG(ABS(attribution.featureAttributions.V6)) AS Avg\_V6\_Attribution,   AVG(ABS(attribution.featureAttributions.V7)) AS Avg\_V7\_Attribution,   AVG(ABS(attribution.featureAttributions.V8)) AS Avg\_V8\_Attribution,   AVG(ABS(attribution.featureAttributions.V9)) AS Avg\_V9\_Attribution,   AVG(ABS(attribution.featureAttributions.V10)) AS Avg\_V10\_Attribution,   AVG(ABS(attribution.featureAttributions.V11)) AS Avg\_V11\_Attribution,   AVG(ABS(attribution.featureAttributions.V12)) AS Avg\_V12\_Attribution,   AVG(ABS(attribution.featureAttributions.V13)) AS Avg\_V13\_Attribution,   AVG(ABS(attribution.featureAttributions.V14)) AS Avg\_V14\_Attribution,   AVG(ABS(attribution.featureAttributions.V15)) AS Avg\_V15\_Attribution,   AVG(ABS(attribution.featureAttributions.V16)) AS Avg\_V16\_Attribution,   AVG(ABS(attribution.featureAttributions.V17)) AS Avg\_V17\_Attribution,   AVG(ABS(attribution.featureAttributions.V18)) AS Avg\_V18\_Attribution,   AVG(ABS(attribution.featureAttributions.V19)) AS Avg\_V19\_Attribution,   AVG(ABS(attribution.featureAttributions.V20)) AS Avg\_V20\_Attribution,   AVG(ABS(attribution.featureAttributions.V21)) AS Avg\_V21\_Attribution,   AVG(ABS(attribution.featureAttributions.V22)) AS Avg\_V22\_Attribution,   AVG(ABS(attribution.featureAttributions.V23)) AS Avg\_V23\_Attribution,   AVG(ABS(attribution.featureAttributions.V24)) AS Avg\_V24\_Attribution,   AVG(ABS(attribution.featureAttributions.V25)) AS Avg\_V25\_Attribution,   AVG(ABS(attribution.featureAttributions.V26)) AS Avg\_V26\_Attribution,   AVG(ABS(attribution.featureAttributions.V27)) AS Avg\_V27\_Attribution,    AVG(ABS(attribution.featureAttributions.V28)) AS Avg\_V28\_Attribution,    AVG(ABS(attribution.featureAttributions.Amount)) AS Avg\_Amount\_Attribution  FROM    \`**your-gcp-project-id***.**fraudfix\_clean\_room\_X***.data\_prediction\_shared\` DP  JOIN    FilteredRankedPredictions FRP  ON    DP.Time \= FRP.Time  CROSS JOIN    UNNEST(DP.explanation.attributions) as attribution  WHERE    FRP.class \= '1' ) SELECT \* FROM AttributionAverages *  |

9. Let's map the results of the previous query with our secret metadata PCA mapping table to understand which attributes are heavily influencing the model's fraudulent decisions. Notice we already have a Biglake table created by Dataplex under the ***bootkon\_raw\_zone*** dataset called ***metadata\_mapping***.   
   Using the previous SQL statement, you find out the most influential attributes ; for example V14.  
   This table should be accessible only by the customers of FraudFix and not by FraudFix employees because it can be used to reverse PCA and access customer private information. 

   ![][image26]

10. Query the metadata table ***“metadata\_mapping”*** and take note of the meanings and descriptions of the most influential V\* attributes (both higher value and lower value attributes). For example, ***V14*** is the most influential attribute for ML decisions. ***V14*** corresponds to the dimensional PCA space attribute for ***“Dispute and Chargeback Frequency”.*** It measures the frequency of disputes and chargebacks, which can be a direct indicator of customer dissatisfaction or fraudulent transactions. Remember that when FraudFix received the dataset from their customers, they did not know the meanings of the V\* columns and their values. FraudFix does not have access to the PCA metadata table. However, as a subscriber (FraudFix customer), you have access to the PCA metadata.

**🥳🥳Congratulations on completing Lab 6\!**   
**You can now move on to Lab 7 for further practice. 🥳🥳**

