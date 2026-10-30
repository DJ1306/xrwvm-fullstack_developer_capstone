import json
from functools import wraps
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST
import requests
from .models import CarMake,CarModel
from . import restapis

def api_errors(view):
    @wraps(view)
    def wrapped(*args,**kwargs):
        try:
            return view(*args,**kwargs)
        except (json.JSONDecodeError,UnicodeDecodeError,KeyError,ValueError) as exc:
            return JsonResponse({"error":f"Invalid request: {exc}"},status=400)
        except requests.HTTPError as exc:
            status=404 if exc.response is not None and exc.response.status_code==404 else 502
            return JsonResponse({"error":"Resource not found." if status==404 else "A backend service is unavailable."},status=status)
        except requests.RequestException:
            return JsonResponse({"error":"A backend service is unavailable."},status=502)
    return wrapped

@require_POST
@api_errors
def login_user(request):
    data=json.loads(request.body)
    user=authenticate(request,username=data["userName"],password=data["password"])
    if user is None:
        return JsonResponse({"status":"Invalid credentials"},status=401)
    login(request,user)
    return JsonResponse({"userName":user.username,"status":"Authenticated"})

def logout_request(request):
    logout(request)
    return JsonResponse({"userName":"","status":"Logged out"})

@require_GET
def session_user(request):
    return JsonResponse({"userName":request.user.username if request.user.is_authenticated else ""})

@require_POST
@api_errors
def registration(request):
    data=json.loads(request.body)
    fields=["userName","firstName","lastName","email","password"]
    if any(not str(data.get(field,"")).strip() for field in fields):
        return JsonResponse({"error":"All five fields are required."},status=400)
    try:
        validate_password(data["password"])
        user=User.objects.create_user(username=data["userName"],password=data["password"],first_name=data["firstName"],last_name=data["lastName"],email=data["email"])
    except ValidationError as exc:
        return JsonResponse({"error":" ".join(exc.messages)},status=400)
    except IntegrityError:
        return JsonResponse({"error":"That username is already registered."},status=409)
    login(request,user)
    return JsonResponse({"userName":user.username,"status":"Registered"},status=201)

@require_GET
@api_errors
def get_dealerships(request,state=None):
    endpoint=f"fetchDealers/{state}" if state and state!="All" else "fetchDealers"
    return JsonResponse({"status":200,"dealers":restapis.get_request(endpoint)})

@require_GET
@api_errors
def get_dealer_details(request,dealer_id):
    return JsonResponse({"status":200,"dealer":restapis.get_request(f"fetchDealer/{dealer_id}")})

@require_GET
@api_errors
def get_dealer_reviews(request,dealer_id):
    reviews=restapis.get_request(f"fetchReviews/dealer/{dealer_id}")
    for review in reviews:
        if not review.get("sentiment"):
            review["sentiment"]=restapis.analyze_review_sentiments(review["review"])["sentiment"]
    return JsonResponse({"status":200,"reviews":reviews})

@require_GET
def get_cars(request):
    return JsonResponse({"status":200,"CarMakes":list(CarMake.objects.values("id","name","description")),"CarModels":list(CarModel.objects.values("id","name","car_make","car_make__name","type","year"))})

@require_GET
@api_errors
def analyze_review(request,text):
    return JsonResponse(restapis.analyze_review_sentiments(text))

@require_POST
@api_errors
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error":"Please sign in to post a review."},status=401)
    data=json.loads(request.body)
    if not str(data.get("review","")).strip():
        return JsonResponse({"error":"Review text is required."},status=400)
    restapis.get_request(f"fetchDealer/{int(data['dealership'])}")
    data["name"]=request.user.get_full_name() or request.user.username
    data["sentiment"]=restapis.analyze_review_sentiments(data["review"])["sentiment"]
    return JsonResponse({"status":201,"review":restapis.post_review(data)},status=201)
