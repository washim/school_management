from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from core.models import Student, StudentPayment, Expense, Transaction, Config, Teacher
from core.forms import ExpenseForm, StudentPaymentForm, StudentPaymentDirectForm, StudentForm, TeacherForm
from django.db.models import Sum


class CoreViewIndex(View):
    def get(self, request, *args, **kwargs):
        data = {}
        data.update({
            "student_count": Student.objects.count()
        })
        data.update(StudentPayment.objects.aggregate(paid_sum=Sum("tuition_fee_paid", default=0) + Sum("admission_fee_paid", default=0) + Sum("learning_material_fee_paid", default=0) + Sum("others_fee_paid", default=0)))
        data.update(Expense.objects.aggregate(Sum("amount", default=0)))
        data.update({"profit": data["paid_sum"] - data["amount__sum"]})
        return render(request, "core/core_template.html", data)

class BalanceSheet(View):
    def get(self, request, *args, **kwargs):
        data = {}
        try:
            if request.GET.get("start_date") > request.GET.get("end_date"):
                messages.error(self.request, "Date range enter by you is invalid.")
                transactions = Transaction.objects.all()
            else:
                transactions = Transaction.objects.filter(created__gte=request.GET.get("start_date"), created__lte=request.GET.get("end_date")).all()
        except Exception:
            transactions = Transaction.objects.all()

        data["transactions"] = transactions

        return render(request, "core/balance_sheet.html", data)


class PrintStudentDetails(View):
    def get(self, request, *args, **kwargs):
        data = dict(student=get_object_or_404(Student, pk=kwargs["pk"]))
        return render(request, "core/printout_student.html", data)


class PrintStudentIncome(View):
    def get(self, request, *args, **kwargs):
        data = dict(income=get_object_or_404(StudentPayment, pk=kwargs["pk"]))
        return render(request, "core/printout_student_income.html", data)


class PrintStudentsIDCard(View):
    def get(self, request, *args, **kwargs):
        data = dict(students=Student.objects.filter(identity_card_issued="No").exclude(photo="").all())
        return render(request, "core/printout_students_id_card.html", data)


class StudentListView(ListView):
    paginate_by = 10
    model = Student

    def get_queryset(self, **kwargs):
       qs = super().get_queryset(**kwargs)
       if self.request.GET.get('codeno'):
            return qs.filter(code_no=self.request.GET.get('codeno'))
       else:
            return qs.all()


class StudentDetailView(DetailView):
    model = Student


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm


class StudentPaymentListView(ListView):
    model = StudentPayment


class StudentPaymentDetailView(DetailView):
    model = StudentPayment


class StudentPaymentDirectCreateView(CreateView):
    model = StudentPayment
    form_class = StudentPaymentDirectForm

    def form_valid(self, form):
        result = super().form_valid(form)
        closing = 0

        try:
            latest = Transaction.objects.filter(mode=self.object.mode).last()
            closing = latest.closing
        except Exception:
            pass
        
        paid = self.object.tuition_fee_paid + self.object.admission_fee_paid + self.object.learning_material_fee_paid + self.object.others_fee_paid
        trans = Transaction(transaction_id=self.object.pk, transaction_type="income", details=self.object.note, 
                            mode=self.object.mode, debit=0, credit=paid, closing=closing + paid)
        trans.save()
        messages.success(self.request, "Income successfully added.")
        
        return result


class StudentPaymentCreateView(CreateView):
    model = StudentPayment
    form_class = StudentPaymentForm

    def form_valid(self, form):
        result = super().form_valid(form)
        closing = 0

        try:
            latest = Transaction.objects.filter(mode=self.object.mode).last()
            closing = latest.closing
        except Exception:
            pass

        paid = self.object.tuition_fee_paid + self.object.admission_fee_paid + self.object.learning_material_fee_paid + self.object.others_fee_paid
        trans = Transaction(transaction_id=self.object.pk, transaction_type="income", details=self.object.note, 
                            mode=self.object.mode, debit=0, credit=paid, closing=closing + paid)
        trans.save()
        messages.success(self.request, "Income successfully added.")
        
        return result


class StudentPaymentUpdateView(UpdateView):
    model = StudentPayment
    form_class = StudentPaymentForm


class ExpenseListView(ListView):
    model = Expense


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm

    def form_valid(self, form):
        result = super().form_valid(form)
        closing = 0
        
        try:
            latest = Transaction.objects.filter(mode=self.object.mode).last()
            closing = latest.closing
        except Exception:
            pass
        
        trans = Transaction(transaction_id=self.object.pk, transaction_type="expense", details=self.object.details,
                            mode=self.object.mode, debit=self.object.amount, credit=0, closing=closing - self.object.amount)
        trans.save()
        messages.success(self.request, "Expense successfully added.")
        return result


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm


class TeacherListView(ListView):
    paginate_by = 10
    model = Teacher

    def get_queryset(self, **kwargs):
       qs = super().get_queryset(**kwargs)
       if self.request.GET.get('empid'):
            return qs.filter(emp_id=self.request.GET.get('empid'))
       else:
            return qs.all()


class TeacherDetailView(DetailView):
    model = Teacher


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm


class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm