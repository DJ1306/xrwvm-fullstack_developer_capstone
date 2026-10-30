import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoapp.models import CarMake,CarModel
class Command(BaseCommand):
    help="Load the starter vehicle catalog without deleting existing records."
    def handle(self,*args,**kwargs):
        records=json.loads((Path(settings.BASE_DIR)/"database/data/car_records.json").read_text())["cars"]
        for row in records:
            make,_=CarMake.objects.get_or_create(name=row["make"])
            CarModel.objects.get_or_create(car_make=make,name=row["model"],year=min(2023,max(2015,int(row["year"]))),defaults={"type":row["bodyType"]})
        self.stdout.write(self.style.SUCCESS(f"Loaded {CarMake.objects.count()} makes and {CarModel.objects.count()} models."))
