import requests
import urllib3
import sys
import json
import pandas

#tested with quests 2.32.4 and urllib3 2.5.0

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def createParams(id=1,method="",data={},url="",session=""):
    params = [{"data": data, "url": url}]
    req = {"id": id, "method": method, "params": params, "session": session}
    return json.dumps(req)

def createParamsDiff(id=1,method="",token="",url="",session=""):
    params = [{"token": token, "url": url}]
    req = {"id": id, "method": method, "params": params, "session": session}
    return json.dumps(req)

def help():
    structure = '''
    USAGE:
    
    ./RevisionAdomAndDiff.py ip username password adom revision_id

    #this script compares current adom configuration against an old adom revision diff identified by revision_id

    '''
    print(structure)

def logout(session):
    requests.post(f'https://{ip}/jsonrpc', createParams(1,"exec",{},"/sys/logout",session), verify=False)

def login(ip, user, password):
    data = [{"user":user,"passwd":password}]
    loginReq = requests.post(f'https://{ip}/jsonrpc', createParams(1,"exec",data,"/sys/login/user"), verify=False)
    if loginReq.status_code == 200:
        return loginReq.json()
    else:
        print("Login error")
        exit(1)

def getRevisionDiff(adom, revision_id, session, ip):
    data = [{"dst": f"adom/{adom}","src": f"adom/{adom}/revision/{revision_id}"}]
    token = requests.post(f'https://{ip}/jsonrpc', createParams(1,"exec", data, "/cache/diff/start", session), verify=False)
    token = token.json()["result"][0]["data"]["token"]
    finished = 0
    while finished < 100:
        result = requests.post(f'https://{ip}/jsonrpc', createParamsDiff(1, "exec",  token, "/cache/diff/get/summary", session), verify=False)
        try:
            finished = result.json()["result"][0]["data"]["percent"]
        except:
            pass
    report = requests.post(f'https://{ip}/jsonrpc', createParamsDiff(1, "exec", token, "cache/diff/get/detail/obj/all objs", session), verify=False)
    return report.json()["result"][0]["data"][0]["data"]

"""
def getRevision(adom,revision_id,session,ip):
    print(createParams(1,"get",{}, f"/sys/status", session))
    summary = requests.post(f'https://{ip}/jsonrpc', createParams(1,"get",{}, f"/sys/status", session), verify=False)
    print(summary.json())
"""

if __name__ == "__main__":
    ip,user,password = "","",""
    if len(sys.argv) < 5:
        help()
        quit()
    ip,user,password = sys.argv[1],sys.argv[2],sys.argv[3]
    adom,revision_id = sys.argv[4],sys.argv[5]
    loginReq = login(ip, user, password)
    session = loginReq["session"]
    changedList = []
    """ TO BE COMPLETED, DEFINE WHAT NEEDS TO BE WRITTEN TO FILE
    f = open( 'file.csv', 'w')
    for i in getRevisionDiff(adom, revision_id, session, ip):
        changedList.append(i["name"])
    f.write(changedList.__str__())
    f.close
    logout(session)
    """
