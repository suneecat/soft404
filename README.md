# soft404  
A "soft" 404 page is a page that is served with 200 status, but is really a page that says that content is not available.  

Here we look at urls from commoncrawl and look at predicting which urls are soft 404 types, using 2 different models.  

The 2 models, a bert and a catboost model, are those used in repo https://github.com/internetarchive/tarb_soft404  
The models are found here: https://archive.org/download/tarb-gsoc-2023-soft-404/TARB_GSoC23_Soft404analysis/Models/   
The bert.py and catboost.py code has been derived from code found in repo https://github.com/internetarchive/tarb_soft404   

38330 unique urls have been obtained from commoncrawl CC-MAIN-20230921073711-20230921103711-00000.warc.wat file.   
This file is from the CC-MAIN-2023-40 crawl.   
These urls are in file CC-MAIN-20230921073711-20230921103711-00000-warc-wat-http_sites.dat.  

The first 1000 of these urls have been processed with 3 different scripts and the results have been compard.   
get_response_status.py uses the python requests library to determine the url response status code (200, 404, or other).   
bert_list_predict.py uses the bert model to predict wheter a url is type 200 or 404.   
Catboost_predict_psl2.py uses the catboost model to predict whether a url is type 300 or 404.   

Comparison of the results from the 3 different scripts is provided in libreoffice file resp_summary_all.ods.   
The table from the ods file provided in the image below.
![image](https://github.com/suneecat/soft404/assets/6851656/cea87d76-0edb-4b6d-acff-17e2fda328f3)
There is very poor correlation between py_response of the python request library and either of the 2 models.
This is being investigated.
The fairly high number of 404 responses of py_request are also being investigated.










