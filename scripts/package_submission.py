from pathlib import Path
import shutil,zipfile
root=Path(__file__).resolve().parents[1]
out=root.parents[1]/"outputs/capstone-course"
out.mkdir(parents=True,exist_ok=True)
answers=out/"answers";answers.mkdir(exist_ok=True)
mapping={2:"django_server",5:"loginuser",6:"logoutuser",8:"getdealerreviews",9:"getalldealers",10:"getdealerbyid",11:"getdealersbyState",14:"getallcarmakes",15:"analyzereview"}
parts=["# Capstone: real local text answers\n\nThese nine answers were captured from the running local Django, Node/MongoDB, and Flask services.\nPublic GitHub links, screenshots, CI logs, and public deployment are still pending.\n"]
for question,name in mapping.items():
    text=(root/"evidence"/name).read_text(encoding="utf-8-sig")
    (answers/(name+".txt")).write_text(text,encoding="utf-8")
    parts.append(f"## Question {question}\n\nCopy the entire block below.\n\n```text\n{text.rstrip()}\n```\n")
(out/"COPY_PASTE_ANSWERS.md").write_text("\n".join(parts),encoding="utf-8")
(out/"COPY_PASTE_ANSWERS.txt").write_text("\n\n".join(f"QUESTION {q}\n"+(answers/(name+".txt")).read_text() for q,name in mapping.items()),encoding="utf-8")
shutil.copy2(root/"SUBMISSION_MAP.md",out/"UPLOAD_ORDER.md")
shutil.copy2(root/"evidence/local-tests.txt",out/"local-tests.txt")
(out/"STATUS.txt").write_text("""PREPARED LOCALLY — NOT YET A COMPLETE GRADED SUBMISSION

Ready:
- Implemented Django/React application, Node/Express/MongoDB API, and Flask sentiment service.
- About, Contact and five-field Registration source files.
- 13 Django tests passed; React production build passed.
- Actual MongoDB-backed live API checks passed.
- Nine actual text answers in COPY_PASTE_ANSWERS.txt and the answers folder.
- Docker, Kubernetes and GitHub Actions configurations included in project-source.zip.

Pending:
- Your public capstone repository URL / publication: Questions 1, 3, 4, 7.
- Browser access and twelve real screenshots: Questions 12, 13, 16–21, 24–27.
- An actual successful GitHub Actions job log: Question 22.
- A real public Django deployment URL: Question 23.
No CI success, public deployment, screenshots or grades are claimed.

Local application: http://127.0.0.1:8000/
Local demo username: capstone_demo
Local demo password: CourseDemo!2026
These are disposable local-only demonstration credentials, not a personal account.
The demo review is on Bytecard Car Dealership, dealer ID 8 (Kansas).

Question 14 covers tasks 14 AND 15; Question 15 is task 16.
Use question numbers in UPLOAD_ORDER.md.
""",encoding="utf-8")
excluded={".git",".venv","node_modules","__pycache__",".mongo",".mongo-binaries","evidence","build","static"}
def source_files():
    for path in root.rglob("*"):
        rel=path.relative_to(root)
        if not path.is_file() or any(part in excluded for part in rel.parts[:-1]):continue
        if path.suffix in {".pyc",".sqlite3",".log"} or path.name==".env":continue
        # frontend/static is required project source, unlike collected server/static.
        yield path,rel
# Preserve frontend/static explicitly, while excluding only generated static roots.
def included(path):
    rel=path.relative_to(root)
    if any(part in {".git",".venv","node_modules","__pycache__",".mongo",".mongo-binaries","evidence"} for part in rel.parts):return False
    if rel.parts[:2]==("server","static") or rel.parts[:3]==("server","frontend","build"):return False
    return path.is_file() and path.suffix not in {".pyc",".sqlite3",".log"} and path.name!=".env"
with zipfile.ZipFile(out/"project-source.zip","w",zipfile.ZIP_DEFLATED) as zipped:
    for path in root.rglob("*"):
        if included(path):zipped.write(path,Path(root.name)/path.relative_to(root))
with zipfile.ZipFile(out/"capstone-prepared-files.zip","w",zipfile.ZIP_DEFLATED) as zipped:
    for path in out.rglob("*"):
        if path.is_file() and path.name!="capstone-prepared-files.zip":zipped.write(path,path.relative_to(out))
for name in ["project-source.zip","capstone-prepared-files.zip"]:
    with zipfile.ZipFile(out/name) as zipped:
        assert zipped.testzip() is None
        print(name,":",len(zipped.namelist()),"files,", (out/name).stat().st_size,"bytes")
print("Prepared answers:",list(mapping))
