"""Start the three real services. Uses a local MongoDB process for development."""
from pathlib import Path
import os,subprocess,sys,time
root=Path(__file__).resolve().parents[1]
evidence=root/"evidence";evidence.mkdir(exist_ok=True)
processes=[]
try:
    for name,args,cwd in [
        ("database",["node","local.js"],root/"server/database"),
        ("sentiment",[sys.executable,"djangoapp/microservices/app.py"],root/"server"),
        ("django_server",[sys.executable,"-u","manage.py","runserver","127.0.0.1:8000","--noreload"],root/"server"),
    ]:
        log=(evidence/name).open("w",encoding="utf-8")
        env={**os.environ,"PYTHONUNBUFFERED":"1","MONGOMS_DOWNLOAD_DIR":str(root/".mongo-binaries")}
        if (root/".mongo-binaries/mongod.exe").exists():
            env["MONGOMS_SYSTEM_BINARY"]=str(root/".mongo-binaries/mongod.exe")
        processes.append(subprocess.Popen(args,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,env=env))
        print(f"Started {name}, PID {processes[-1].pid}",flush=True)
    print("Local site: http://127.0.0.1:8000 — Ctrl+C stops all services.",flush=True)
    while all(p.poll() is None for p in processes):time.sleep(1)
finally:
    for p in processes:
        if p.poll() is None:p.terminate()
