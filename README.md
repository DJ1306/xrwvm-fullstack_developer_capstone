# Cars Dealership Review Application

- **Repository name:** cars-dealership-capstone
- **Project name:** Cars Dealership Review Application
- **Course:** IBM Cloud Native Full Stack Development Capstone

A responsive React application for finding US car dealerships, filtering by state,
reading customer reviews, and posting a review after signing in.

## Architecture

- React and Vite: dealer directory, registration, login, vehicle selection, reviews.
- Django and SQLite: session authentication, car makes/models, administration, API gateway.
- Node.js, Express and MongoDB: dealership and review storage.
- Flask and NLTK VADER: sentiment analysis.
- Docker Compose and Kubernetes manifests: deployment configuration.
- GitHub Actions: Django checks/tests, frontend build, and static asset collection.

## Run locally

Python 3.12+, Node.js 22+, and MongoDB are required.
For development, `npm run start:local` starts an actual local MongoDB process
using mongodb-memory-server; the first run downloads the vendor binary.

```sh
python -m venv .venv
# Activate .venv using the command for your OS.
pip install -r server/requirements.txt
cd server/database
npm ci
cd ../frontend
npm ci
npm run build
cd ..
python manage.py migrate
python manage.py seed_cars
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Start the API with `npm run start:local` in `server/database`, the sentiment
service with `python djangoapp/microservices/app.py` in `server`, and Django with
`python manage.py runserver 127.0.0.1:8000` in `server`.
Alternatively, run `python scripts/run_local.py` from the repository root
after installing dependencies.

Visit http://127.0.0.1:8000/ and register your own user.
The generated local evidence uses a disposable `capstone_demo` account.
No real account credentials are included in this repository.

## Production configuration

Set DJANGO_SECRET_KEY to a unique secret, DJANGO_DEBUG=false, DJANGO_ALLOWED_HOSTS
to your public hostname, COOKIE_SECURE=true, BACKEND_URL to the Node service,
and SENTIMENT_ANALYZER_URL to the Flask service. SQLite needs persistent storage;
use one Django replica with the supplied persistent volume or configure a
shared production database before scaling. MongoDB also requires persistent
storage. Review `compose.yaml`, `k8s/`, and `DEPLOYMENT.md`.

## Validate

```sh
cd server
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test djangoapp -v 2
cd frontend
npm run build
```

`scripts/collect_evidence.py` executes real cURL requests against the local
services and saves their command/output pairs in the ignored `evidence/`
folder. It requires the disposable demo user created in the local setup.
Local evidence is not proof of public deployment or a GitHub Actions run.

## Course submission

See `SUBMISSION_MAP.md` for the exact Question 1–27 order. The assessment
combines tasks 14 and 15 into Question 14, so subsequent question numbers are
one lower than the task numbers.

## Credits

Based on IBM Developer Skills Network's
[xrwvm-fullstack_developer_capstone](https://github.com/ibm-developer-skills-network/xrwvm-fullstack_developer_capstone).
Starter dealership, review, vehicle, and car image data are retained for education.
Team photos are stock portraits from Random User (https://randomuser.me/).
The named team profiles and contact information are illustrative examples.
