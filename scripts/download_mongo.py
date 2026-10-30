from pathlib import Path
import requests,zipfile
root=Path(__file__).resolve().parents[1]
dest=root/".mongo-binaries";dest.mkdir(exist_ok=True)
binary=dest/"mongod.exe"
if not binary.exists():
    archive=dest/"mongodb.zip"
    with requests.get("https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.14.zip",stream=True,timeout=60) as response:
        response.raise_for_status()
        with archive.open("wb") as handle:
            for chunk in response.iter_content(1024*1024):handle.write(chunk)
    with zipfile.ZipFile(archive) as zipped:
        name=next(n for n in zipped.namelist() if n.endswith("/bin/mongod.exe"))
        binary.write_bytes(zipped.read(name))
print(binary)
