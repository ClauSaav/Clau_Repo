import urllib.request
url = "http://spatialkeydocs.s3.amazonaws.com/FL_insurance_sample.csv.zip"
file_name = "../data/downloaded.zip"
# Download the file from `url` and save it locally under `file_name`:
urllib.request.urlretrieve(url, file_name)
