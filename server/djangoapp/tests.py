import json
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
import requests
from .models import CarMake,CarModel

class DealershipTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user("driver",password="TestJourney!2026",first_name="Demo",last_name="Driver")
    def post(self,path,data):
        return self.client.post("/djangoapp/"+path,json.dumps(data),content_type="application/json")
    def test_login_creates_session_and_logout_clears_it(self):
        response=self.post("login",{"userName":"driver","password":"TestJourney!2026"})
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.client.get("/djangoapp/session").json()["userName"],"driver")
        self.client.get("/djangoapp/logout")
        self.assertEqual(self.client.get("/djangoapp/session").json()["userName"],"")
    def test_invalid_credentials_are_rejected(self):
        self.assertEqual(self.post("login",{"userName":"driver","password":"incorrect"}).status_code,401)
    def test_registration_requires_all_five_fields(self):
        self.assertEqual(self.post("register",{"userName":"missing"}).status_code,400)
    def test_registration_rejects_duplicate_username(self):
        self.assertEqual(self.post("register",{"userName":"driver","firstName":"Demo","lastName":"Driver","email":"demo@example.com","password":"GoodJourney!2026"}).status_code,409)
    def test_registration_authenticates_new_user(self):
        response=self.post("register",{"userName":"newdriver","firstName":"New","lastName":"Driver","email":"new@example.com","password":"GoodJourney!2026"})
        self.assertEqual(response.status_code,201)
        self.assertEqual(self.client.get("/djangoapp/session").json()["userName"],"newdriver")
    def test_malformed_json_returns_bad_request(self):
        self.assertEqual(self.client.post("/djangoapp/login","{",content_type="application/json").status_code,400)
    def test_unauthenticated_review_is_rejected(self):
        self.assertEqual(self.post("add_review",{"review":"Excellent"}).status_code,401)
    @patch("djangoapp.restapis.get_request")
    def test_kansas_filter_uses_backend_state_endpoint(self,get):
        get.return_value=[{"id":7,"state":"Kansas"}]
        response=self.client.get("/djangoapp/get_dealers/Kansas")
        self.assertEqual(response.json()["dealers"][0]["state"],"Kansas")
        get.assert_called_once_with("fetchDealers/Kansas")
    @patch("djangoapp.restapis.get_request",side_effect=requests.ConnectionError)
    def test_upstream_failure_returns_service_error(self,get):
        self.assertEqual(self.client.get("/djangoapp/get_dealers").status_code,502)
    @patch("djangoapp.restapis.get_request")
    def test_unknown_dealer_preserves_not_found_status(self,get):
        upstream=requests.Response()
        upstream.status_code=404
        get.side_effect=requests.HTTPError(response=upstream)
        self.assertEqual(self.client.get("/djangoapp/dealer/99999").status_code,404)
    @patch("djangoapp.restapis.post_review")
    @patch("djangoapp.restapis.analyze_review_sentiments",return_value={"sentiment":"positive"})
    @patch("djangoapp.restapis.get_request",return_value={"id":1})
    def test_review_author_comes_from_authenticated_session(self,get,analyze,post):
        self.client.force_login(self.user)
        post.side_effect=lambda data:data
        result=self.post("add_review",{"dealership":1,"review":"Fantastic services","name":"Impersonated"})
        self.assertEqual(result.status_code,201)
        self.assertEqual(result.json()["review"]["name"],"Demo Driver")
        self.assertEqual(result.json()["review"]["sentiment"],"positive")
    def test_catalog_includes_make_and_model(self):
        make=CarMake.objects.create(name="Nissan")
        CarModel.objects.create(car_make=make,name="Pathfinder",type="SUV",year=2023)
        data=self.client.get("/djangoapp/get_cars").json()
        self.assertEqual(data["CarMakes"][0]["name"],"Nissan")
        self.assertEqual(data["CarModels"][0]["car_make__name"],"Nissan")
    def test_about_contact_and_registration_source_exist(self):
        self.assertContains(self.client.get("/about"),"Customer Experience Lead")
        self.assertContains(self.client.get("/contact"),'aria-current="page"')
