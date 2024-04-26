import csv
import os
from django.core.management.base import BaseCommand, CommandError
from school_management.settings import BASE_DIR
from core.models import Student


class Command(BaseCommand):
    help = "Bulk student create"

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, "core/static/iqra_english_school_id_card.csv")
        with open(file_path, 'rb') as csv_file:
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                dd, mm, yyyy = str(row["dob"]).split("/", 3)
                dob = yyyy + "-" + mm + "-" + dd
                students = Student(code_no=row["codeno"], photo="students_picture/" + row["codeno"] + ".jpg", name=str(row["name"]).lower().title(), 
                                    father_name=str(row["father_name"]).lower().title(), date_of_birth=dob, 
                                    section=row["class"], mobile_no=row["mobile"], academic_session=row["academic_session"], 
                                    admission_date="2019-06-01", village=str(row["village"]).lower().title(), 
                                    post_office=str(row["post_office"]).lower().title(), police_station=str(row["police_station"]).lower().title(), 
                                    district=str(row["district"]).lower().title())
                students.save()
                self.stdout.write(
                    self.style.SUCCESS('Student Created "%s"' % row["name"])
                )