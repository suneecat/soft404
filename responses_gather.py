import csv

def write_header(outputfile):
    with open(outputfile, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["Url", "py_response","bert_predict", "catboost_predict"])

def write_details_to_csv(outputfile, url, p_resp, bert_pred, cat_pred):
        with open(outputfile, "a", newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([url, p_resp, bert_pred, cat_pred])

def check_list(type, list):
    k=0
    for lx in list:
        print(f'{k}, {type}, {list[k]},  {lx} ')
        k=k+1


summary_file = "resp_summary_all.csv"
write_header(summary_file)


# get the various csv data
with open('resp_status_chk.csv', newline='') as csvfile:
    py_responses = csv.reader(csvfile, delimiter=',')
    py_list=list(py_responses)

with open('bert_soft404_chk.csv', newline='') as csvfile:
    bert_responses = csv.reader(csvfile, delimiter=',')
    bert_list=list(bert_responses)

with open('catboost_chk.csv', newline='') as csvfile:
    catboost_responses = csv.reader(csvfile, delimiter=',')
    catboost_list=list(catboost_responses)

#check_list("bert", bert_list)




for count in range(1,1001):
#    print(f'count is: {count}')
    bert_row=bert_list[count]
    catboost_row=catboost_list[count]
    bert_pred=bert_row[1]
    cat_pred=catboost_row[1]
    url, p_resp, b_predict, cat_predict = py_list[count][0], py_list[count][1], bert_pred, cat_pred
    write_details_to_csv(summary_file, url, p_resp, b_predict, cat_predict)


print(f"processed {count} lines")
print("FINISHED\n")

