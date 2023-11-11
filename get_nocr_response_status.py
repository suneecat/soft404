import requests
import csv
import time


def write_header(outputfile):
    with open(outputfile, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["Url", "response_type", "isError"])

def write_details_to_csv(outputfile, url, resp_type):
        with open(outputfile, "a", newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([url, resp_type])

def write_error_to_csv(outputfile, url, err, resp_type):
        with open(outputfile, "a", newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([url, err, resp_type])


# get the list of URLs you want to visit; remove <CR> from end if it is there    
with open('http_sites.dat', 'r') as f:
    urls = [line.rstrip('\n') for line in f]	   

outputfile = "resp_nocr_1000urls_status.csv"
write_header(outputfile)

count=0
for url in urls:
    count=count+1
    if count==1001:
        break
    try:
        
        # Check the HTTP status code using the requests library
        response = requests.get(url)
        status_code = response.status_code
	
        url=url[:-1]     # strip the <cr> at the end of url	
#        print(f"URL: {url}, Status Code: {status_code}")
        write_details_to_csv(outputfile, url, status_code)

    except requests.exceptions.RequestException as e:
        url=url[:-1]     # strip the <cr> at the end of url		
#        print(f"URL: {url}, Exception occured {e}")
        write_error_to_csv(outputfile, url, "ERROR", e)
	
    print(f'url no. {count}')
 

print(f"/n count={count}; FINISHED/n")



