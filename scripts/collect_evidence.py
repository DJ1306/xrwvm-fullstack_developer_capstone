"""Execute real curl commands, saving exactly the command and its returned output."""
import json,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/"evidence";out.mkdir(exist_ok=True)
base="http://127.0.0.1:8000"
jar=out/"demo-session.cookies"
def capture(name,path,data=None,cookies=False):
    args=["curl.exe" if __import__("os").name=="nt" else "curl","--silent","--show-error","--fail-with-body"]
    command="curl --silent --show-error --fail-with-body"
    if cookies:
        args+=["-b",str(jar),"-c",str(jar)];command+=" -b demo-session.cookies -c demo-session.cookies"
    if data is not None:
        body=json.dumps(data)
        payload=out/(name+".json");payload.write_text(body)
        args+=["-H","Content-Type: application/json","--data",body]
        command+=' -H "Content-Type: application/json" --data '+repr(body)
    url=base+path;args.append(url);command+=' "'+url+'"'
    result=subprocess.run(args,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stderr+result.stdout)
    (out/name).write_text(command+"\n"+result.stdout+"\n",encoding="utf-8")
    print(name+": captured "+str(len(result.stdout))+" characters")
    return json.loads(result.stdout)
capture("loginuser","/djangoapp/login",{"userName":"capstone_demo","password":"CourseDemo!2026"},True)
assert capture("session-check","/djangoapp/session",cookies=True)["userName"]=="capstone_demo"
dealers=capture("getalldealers","/djangoapp/get_dealers")["dealers"]
selected=next(d for d in dealers if d["state"]=="Kansas")
dealer_id=selected["id"]
capture("getdealerbyid",f"/djangoapp/dealer/{dealer_id}")
kansas=capture("getdealersbyState","/djangoapp/get_dealers/Kansas")["dealers"]
assert kansas and all(d["state"]=="Kansas" for d in kansas)
capture("getallcarmakes","/djangoapp/get_cars")
assert capture("analyzereview","/djangoapp/analyze/Fantastic%20services")["sentiment"]=="positive"
review={"dealership":dealer_id,"review":"Fantastic services. The team explained the options clearly and made my visit easy.","purchase":True,"purchase_date":"2026-10-29","car_make":"Nissan","car_model":"Pathfinder","car_year":2023}
existing=capture("reviews-before-post",f"/djangoapp/reviews/dealer/{dealer_id}")["reviews"]
if not any(r["review"]==review["review"] for r in existing):
    capture("posted_review","/djangoapp/add_review",review,True)
reviews=capture("getdealerreviews",f"/djangoapp/reviews/dealer/{dealer_id}")["reviews"]
assert any(r["review"]==review["review"] for r in reviews)
capture("logoutuser","/djangoapp/logout",cookies=True)
assert capture("logged-out-check","/djangoapp/session",cookies=True)["userName"]==""
(out/"selected_dealer.json").write_text(json.dumps(selected,indent=2))
print("All live API evidence checks passed.")
