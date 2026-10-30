# Deployment

The supplied Dockerfiles and Kubernetes resources are configuration, not evidence
that deployment has occurred.

## Docker Compose

Set DJANGO_SECRET_KEY in a root .env file, then run:
```sh
docker compose up --build
docker compose exec web python manage.py createsuperuser
```

## Kubernetes

Build/push web, database, and sentiment images to your registry. Set the three
image references in k8s/dealership.yaml. Create the Django secret:
```sh
kubectl create secret generic dealership-secrets --from-literal=django-secret-key=YOUR_GENERATED_SECRET
kubectl apply -f k8s/dealership.yaml
```
The Django ALLOWED_HOSTS configuration must name your ingress hostname; configure
HTTPS at your ingress and set COOKIE_SECURE=true. The sample service is ClusterIP:
publish it through your cluster's approved ingress configuration. The MongoDB
instance and SQLite database each use a persistent volume.

## IBM Cloud Code Engine

Deploy the Node API with an externally managed MongoDB URI, the sentiment
Dockerfile from server/djangoapp/microservices, and the Django Dockerfile from
server. Set BACKEND_URL, SENTIMENT_ANALYZER_URL, DJANGO_ALLOWED_HOSTS,
DJANGO_SECRET_KEY, DJANGO_DEBUG=false and COOKIE_SECURE=true.
Use an external persistent database for Django when the runtime lacks a suitable
persistent volume; the local SQLite default is not persistent on ephemeral replicas.

## Collect final evidence

After pushing your repository, wait for GitHub Actions to pass. Save the actual
workflow job log to CICD. After deployment, save its real public HTTPS URL to
deploymentURL. Use that URL in a browser for the four deployed screenshots.
