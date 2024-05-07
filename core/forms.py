from django.forms import ModelForm
from core.models import Student, Expense, StudentPayment, Teacher


class TeacherForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs['class'] = 'datepicker'
        self.fields['joining_date'].widget.attrs['class'] = 'datepicker'
        self.fields['relieving_date'].widget.attrs['class'] = 'datepicker'
    
    class Meta:
        model = Teacher
        fields = "__all__"


class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs['class'] = 'datepicker'
        self.fields['admission_date'].widget.attrs['class'] = 'datepicker'
    
    class Meta:
        model = Student
        fields = "__all__"


class StudenPaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].widget.attrs['class'] = 'datepicker'
    
    class Meta:
        model = StudentPayment
        exclude = ["student"]


class StudenPaymentDirectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].widget.attrs['class'] = 'datepicker'
    
    class Meta:
        model = StudentPayment
        fields = "__all__"


class ExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_date'].widget.attrs['class'] = 'datepicker'
    
    class Meta:
        model = Expense
        fields = "__all__"
        