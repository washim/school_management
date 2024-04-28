import csv
import os
import urllib.request
from django.core.management.base import BaseCommand, CommandError
from school_management.settings import BASE_DIR, BASE_URL
from core.models import Student


class Command(BaseCommand):
    help = "Bulk student update"

    def handle(self, *args, **options):
        students = Student.objects.all()
        for student in students:
            student.section = str(student.section).replace("(", "").replace(")", "").replace(".", "")
            student.academic_session = str(student.academic_session).replace("2024-25", "2024-2025")
            
            try:
                status_code = urllib.request.urlopen(BASE_URL + student.photo.url).getcode()
                if status_code != 200:
                    student.photo = None
            
            except Exception:
                student.photo = None
            
            student.save()
            self.stdout.write(
                self.style.SUCCESS('Student Updated "%s"' % student.name)
            )