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

EXPENSE_CATEGORY = (
    ("salary", "PAYROLL"), 
    ("rent", "RENT"),
    ("labour", "LABOR"),
    ("material", "MATERIAL"),
    ("travel", "TRAVEL"),
    ("marketing", "MARKETING"),
    ("loan", "LOAN"),
    ("others", "OTHERS"),
)

class Teacher(models.Model):
    emp_id = models.CharField(max_length=255, unique=True)
    photo = ResizedImageField(size=[200, 200], upload_to="teachers_picture", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("Male", "Male"), ("Female", "Female")), null=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, help_text="Example: English Teacher")
    qualification = models.CharField(max_length=255)
    experience = models.FloatField(max_length=2, help_text="Employee work experience in years in time of joining")
    mobile_no = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    relieving_date = models.DateField(null=True, blank=True, help_text="Provide this date if employee is leaving from organization")
    identity_card_issued = models.CharField(max_length=3, choices=(("Yes", "Yes"), ("No", "No")), default="No", null=True)
    permanent_address = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teacher-details", kwargs={"pk": self.pk})


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
        return str(self.name).lower().title() + " (%s)" % self.code_no

    def get_absolute_url(self):
        return reverse("student-details", kwargs={"pk": self.pk})


class StudentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments", null=True)
    tuition_fee_total = models.PositiveIntegerField(blank=True, null=True, default=0)
    tuition_fee_paid = models.PositiveIntegerField(blank=True, null=True, default=0)
    tuition_fee_due = models.PositiveIntegerField(blank=True, null=True, default=0)
    admission_fee_total = models.PositiveIntegerField(blank=True, null=True, default=0)
    admission_fee_paid = models.PositiveIntegerField(blank=True, null=True, default=0)
    admission_fee_due = models.PositiveIntegerField(blank=True, null=True, default=0)
    learning_material_fee_total = models.PositiveIntegerField(blank=True, null=True, default=0)
    learning_material_fee_paid = models.PositiveIntegerField(blank=True, null=True, default=0)
    learning_material_fee_due = models.PositiveIntegerField(blank=True, null=True, default=0)
    others_fee_total = models.PositiveIntegerField(blank=True, null=True, default=0)
    others_fee_paid = models.PositiveIntegerField(blank=True, null=True, default=0)
    others_fee_due = models.PositiveIntegerField(blank=True, null=True, default=0)
    mode = models.CharField(max_length=8, choices=(("cash", "CASH"), ("online", "ONLINE")), null=True)
    payment_reference_code = models.CharField(max_length=100, null=True, blank=True, help_text="Please provide reference number for online payment.")
    note = models.TextField(blank=True, help_text="Please add note for future auditing purpose")
    created = models.DateField(auto_now_add=True, null=True)
    updated = models.DateField(auto_now=True, null=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("student-details", kwargs={"pk": self.student.pk})

    def paid(self):
        return self.tuition_fee_paid + self.admission_fee_paid + self.learning_material_fee_paid + self.others_fee_paid

    def due(self):
        return self.tuition_fee_due + self.admission_fee_due + self.learning_material_fee_due + self.others_fee_due


class Expense(models.Model):
    amount = models.PositiveIntegerField()
    expense_for = models.CharField(max_length=100, choices=EXPENSE_CATEGORY)
    mode = models.CharField(max_length=8, choices=(("cash", "CASH"), ("online", "ONLINE")), null=True)
    expense_reference_code = models.CharField(max_length=100, null=True, blank=True, help_text="Please provide reference number for online expense.")
    expense_date = models.DateField()
    details = models.CharField(max_length=255, help_text="Please add details for future auditing purpose")
    created = models.DateField(auto_now_add=True, null=True)
    updated = models.DateField(auto_now=True, null=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("expenses")


class Transaction(models.Model):
    transaction_id = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=(("income", "INCOME"), ("expense", "EXPENSE")))
    details = models.CharField(max_length=255, null=True, blank=True)
    mode = models.CharField(max_length=8, choices=(("cash", "CASH"), ("online", "ONLINE")), null=True)
    debit = models.PositiveIntegerField(default=0)
    credit = models.PositiveIntegerField(default=0)
    closing = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True, null=True)


class Config(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key