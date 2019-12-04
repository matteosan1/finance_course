import request, json, os
from sys import exit

url = "http://lx000000700503.testfactory.copergmps:7074/deployarchive/check"

user = os.environ.get("GITLAB_USER_LOGIN")
project = os.environ.get("CI_PROJECT_NAME")
merge_id = os.environ.get("CI_MERGE_REQUEST_ID")

data = {"project":project, "user":user, "id":merge_id}
headers = {'Content-type':'application/json', 'Accept':'application/json'}

print (data)
