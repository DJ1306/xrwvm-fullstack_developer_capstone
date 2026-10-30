"""Download only mongod.exe from the official vendor ZIP using HTTP byte ranges."""
from pathlib import Path
import io,requests,zipfile
URL="https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.14.zip"
session=requests.Session()
length=int(session.head(URL,timeout=20).headers["Content-Length"])
class RemoteZip(io.RawIOBase):
    def __init__(self):self.position=0
    def seek(self,offset,whence=0):
        self.position=offset if whence==0 else self.position+offset if whence==1 else length+offset
        return self.position
    def tell(self):return self.position
    def seekable(self):return True
    def read(self,size=-1):
        end=length-1 if size<0 else min(length-1,self.position+size-1)
        if self.position>end:return b""
        response=session.get(URL,headers={"Range":f"bytes={self.position}-{end}"},timeout=60)
        if response.status_code!=206:raise RuntimeError("Server did not honor byte range")
        data=response.content;self.position+=len(data);return data
root=Path(__file__).resolve().parents[1];dest=root/".mongo-binaries";dest.mkdir(exist_ok=True)
with zipfile.ZipFile(RemoteZip()) as archive:
    member=next(i for i in archive.infolist() if i.filename.endswith("/bin/mongod.exe"))
    print(f"Downloading compressed mongod.exe: {member.compress_size} bytes instead of the {length}-byte bundle",flush=True)
    (dest/"mongod.exe").write_bytes(archive.read(member))
print("MongoDB binary ready",flush=True)
