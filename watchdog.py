import requests, json, os
from sys import exit

url = "http://lx000000700503.testfactory.copergmps:7074/deployarchive/check"

user = os.environ.get("GITLAB_USER_LOGIN")
project = os.environ.get("CI_PROJECT_NAME")
merge_id = os.environ.get("CI_MERGE_REQUEST_ID")

data = {"project":project, "user":user, "id":merge_id}
headers = {'Content-type':'application/json', 'Accept':'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)

result = json.loads(r.text)

if result["result"]:
    if user == result["user"]:
        print ("Merge request can be approved !")
        exit(0)
    else:
        print ("An owner cannot apprve his/her merge requests...")
        exit(255)
else:
    if "error" in result.keys():
        print (result["error"])
        exit(200)
    else:
        print ("The merge request {} for project {} has been created succesfully. Now an impartial approval is required.".format(merge_id, project))
        exit(1)
