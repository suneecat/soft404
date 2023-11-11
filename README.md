# soft404   

A work in progress   

A "soft" 404 page is a page that is served with 200 status, but is really a page that says that content is not available.  

Here we look at urls from commoncrawl and look at predicting which urls are soft 404 types, using 2 different models.  

The 2 models, a bert and a catboost model, are those used in repo https://github.com/internetarchive/tarb_soft404  
The models are found here: https://archive.org/download/tarb-gsoc-2023-soft-404/TARB_GSoC23_Soft404analysis/Models/   
The bert.py and catboost.py code has been derived from code found in repo https://github.com/internetarchive/tarb_soft404   

38330 unique urls have been obtained from commoncrawl CC-MAIN-20230921073711-20230921103711-00000.warc.wat file.   
This file is from the CC-MAIN-2023-40 crawl.   
These urls are in file CC-MAIN-20230921073711-20230921103711-00000-warc-wat-http_sites.dat.  
The same urls are in file http_sites.dat.    

The first 1000 of these urls have been processed with 3 different scripts and the results have been compared.   
1.) get_nocr_response_status.py uses the python requests library to determine the url response status code (200, 404, or other).   
2.) bert_list_predict.py uses the bert model to predict wheter a url is type 200 or 404.   
3.) Catboost_predict_psl2.py uses the catboost model to predict whether a url is type 200 or 404.   
Any \n characters at the end of a url have been removed, hence the _nocr_ indicator in the name.

Comparison of the results from the 3 different scripts is provided in libreoffice file resp_summary_all_noCR.ods.   
The table from the ods file provided in the image below.
![image](https://github.com/suneecat/soft404/assets/6851656/b3a6aa64-1f67-4436-987e-7a2ab796979b)

Of the 878 response types 200 returned by python requests, the BERT model predictor finds 525, or 60%.
The Catboost model predictor finds 772, or 88%.

Of the 27 response types 404 returned by python requests, the BERT model predictor finds 6, or 22%
the Catboost model predictor finds 3, or 11%

Neither the BERT nor the Catboost models are suitable for predicting 404 type responses.
The Catboost model is significantly better than the BERT model in predicting 200 type responses.











