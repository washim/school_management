from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField


STUDENT_CLASSES = (
    ("LKG", "LKG"), ("UKG", "UKG"),
    ("I", "I"), ("II", "II"), ("III", "III"), ("IV", "IV"), ("V", "V"),
    ("VI", "VI"), ("VII", "VII"), ("VIII", "VIII"), ("IX", "IX"), ("X", "X")
)

ACADEMIC_SESSION = (
    ("2023-2024", "2023-2024"), ("2024-2025", "2024-2025"), ("2025-2026", "2025-2026")
)

PAYMENT_FOR = (
    ("tuition_fee", "TUITION FEE"), 
    ("admission_fee", "ADMISSION FEE"),
    ("learning_material_fee", "LEARNING MATERIAL FEE"),
    ("uniform_fee", "UNIFORM FEE"),
    ("hostel_fee", "HOSTEL FEE"),
    ("transport_fee", "TRANSPORT FEE"),
    ("food_fee", "FOOD FEE"),
    ("other_fee", "OTHER FEE"),
)

EXPENSE_CATEGORY = (
    ("salary", "PAYROLL"), 
    ("rent", "RENT"),
    ("labour", "LABOR"),
    ("material", "MATERIAL"),
    ("travel", "TRAVEL"),
    ("marketing", "MARKETING"),
    ("loan", "LOAN"),
)

class Student(models.Model):
    code_no = models.CharField(max_length=255, unique=True)
    photo = ResizedImageField(size=[200, 200], upload_to="students_picture", null=True, blank=True)
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(("Male", "Male"), ("Female", "Female")), null=True)
    section = models.CharField("Class", max_length=5, choices=STUDENT_CLASSES)
    mobile_no = models.CharField(max_length=10)
    academic_session = models.CharField(max_length=10, choices=ACADEMIC_SESSION)
    identity_card_issued = models.CharField(max_length=3, choices=(("Yes", "Yes"), ("No", "No")), default="No", null=True)
    admission_date = models.DateField()
    village = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    police_station = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.name).lower().title() + " (Code No: %s)" % self.code_no

    def get_absolute_url(self):
        return reverse("student-details", kwargs={"pk": self.pk})


class StudentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    due = models.FloatField(max_length=6)
    paid = models.FloatField(max_length=6)
    payment_date = models.DateField()
    payment_for = models.CharField(max_length=100, choices=PAYMENT_FOR, null=True)
    mode = models.CharField(max_length=8, choices=(("cash", "CASH"), ("online", "ONLINE")), null=True)
    payment_reference_code = models.CharField(max_length=100, null=True, blank=True, help_text="Please provide reference number for online payment.")
    note = models.TextField(blank=True, help_text="Please add note for future auditing purpose")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("student-details", kwargs={"pk": self.student.pk})


class Expense(models.Model):
    amount = models.FloatField(max_length=6)
    expense_for = models.CharField(max_length=100, choices=EXPENSE_CATEGORY)
    expense_date = models.DateField()
    details = models.CharField(max_length=255, help_text="Please add details for future auditing purpose")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("expenses")