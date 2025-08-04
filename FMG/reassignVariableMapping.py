import requests
import urllib3
import sys
import json
import pandas

#tested with quests 2.32.4 and urllib3 2.5.0

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def help():
    structure = '''
    USAGE:
    
    ./RevisionAdomAndDiff.py ip username password adom vdom_to_assign

    #this script reassigns all variables associated with a device-vdom-global to device-vdom_to_assign

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
        print(loginReq.json())
        print("Login error")
        exit(1)

def createParams(id=1,method="",data={},url="",session=""):
    params = [{"data": data, "url": url}]
    req = {"id": id, "method": method, "params": params, "session": session}
    return json.dumps(req)

def createParamsUrl(id=1,method="",url="",session=""):
    params = [{"url": url}]
    req = {"id": id, "method": method, "params": params, "session": session}
    return json.dumps(req)

def lockAdom(ip,session,adom):
    requests.post(f"https://{ip}/jsonrpc", createParamsUrl(1,"exec",f"/dvmdb/adom/{adom}/workspace/lock",session),verify=False)

def commitAdom(ip,session,adom):
    requests.post(f"https://{ip}/jsonrpc", createParamsUrl(1,"exec",f"/dvmdb/adom/{adom}/workspace/commit",session),verify=False)

def unlockAdom(ip,session,adom):
    requests.post(f"https://{ip}/jsonrpc", createParamsUrl(1,"exec",f"/dvmdb/adom/{adom}/workspace/unlock",session),verify=False)

def getMetadata(ip,session,adom):
    req = requests.post(f"https://{ip}/jsonrpc", createParamsUrl(1,"exec", f"/pm/config/adom/{adom}/_fmgvar/export",session), verify=False)
    req = req.json()
    return req["result"][0]["data"]

def reassignVariable(ip,session,adom,vdom_to_assign,list):
    lockAdom(ip,session,adom)
    for item in list["variables"]:
        try:
            for vdom in item["mapping"]:
                if vdom["vdom"] == "":
                    data = [{"name": vdom["device"], "vdom": vdom_to_assign}]
                    req = requests.post(f"https://{ip}/jsonrpc", createParams(1,"set",data,f'/pm/config/adom/{adom}/obj/fmg/variable/{item["name"]}/dynamic_mapping/{vdom["device"]}/global/_scope',session),verify=False)
                    print(req.json())
                    if req.json()["result"][0]["status"]["message"] != "OK":
                        print(req.json())
                        print("Error during reassignment")
        except:
            pass
    commitAdom(ip,session,adom)
    unlockAdom(ip,session,adom)

if __name__ == "__main__":
    ip,user,password = "","",""
    if len(sys.argv) < 5:
        help()
        quit()
    ip,user,password = sys.argv[1],sys.argv[2],sys.argv[3]
    adom,vdom_to_assign = sys.argv[4],sys.argv[5]
    loginReq = login(ip, user, password)
    session = loginReq["session"]
    reassignVariable(ip, session, adom, vdom_to_assign,json.loads(getMetadata(ip,session,adom)["data"]))
    logout(session)

