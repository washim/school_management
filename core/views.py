from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from core.models import Student, StudentPayment, Expense
from core.forms import ExpenseForm, StudenPaymentForm, StudenPaymentDirectForm, StudentForm
from django.db.models import Sum


class CoreViewIndex(View):
    def get(self, request, *args, **kwargs):
        data = {}
        data.update({
            "student_count": Student.objects.count()
        })
        data.update(StudentPayment.objects.aggregate(Sum("paid", default=0)))
        data.update(Expense.objects.aggregate(Sum("amount", default=0)))
        data.update({"profit": data["paid__sum"] - data["amount__sum"]})
        return render(request, "core/core_template.html", data)


class BalanceSheet(View):
    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get("start_date") > request.GET.get("end_date"):
                messages.error(self.request, "Date range enter by you is invalid.")

            else:
                data = dict(
                    income=StudentPayment.objects.filter(paid__gt=0, payment_date__gte=request.GET.get("start_date"), payment_date__lte=request.GET.get("end_date")).all(),
                    expenses=Expense.objects.filter(expense_date__gte=request.GET.get("start_date"), expense_date__lte=request.GET.get("end_date")).all()
                )
                data["total_income"] = sum([item.paid for item in data["income"]])
                data["total_expense"] = sum([item.amount for item in data["expenses"]])
                data["loss_profit"] = data.get("total_income", 0) - data.get("total_expense", 0)
                
                return render(request, "core/balance_sheet.html", data)
        
        except Exception:
            pass
        
        data = dict(
            income=StudentPayment.objects.filter(paid__gt=0).all(),
            expenses=Expense.objects.all()
        )
        data["total_income"] = sum([item.paid for item in data["income"]])
        data["total_expense"] = sum([item.amount for item in data["expenses"]])
        data["loss_profit"] = data.get("total_income", 0) - data.get("total_expense", 0)
        
        return render(request, "core/balance_sheet.html", data)


class PrintStudentDetails(View):
    def get(self, request, *args, **kwargs):
        data = dict(student=get_object_or_404(Student, pk=kwargs["pk"]))
        return render(request, "core/printout_student.html", data)


class PrintStudentsIDCard(View):
    def get(self, request, *args, **kwargs):
        data = dict(students=Student.objects.filter(identity_card_issued="No").exclude(photo="").all())
        return render(request, "core/printout_students_id_card.html", data)


class StudentListView(ListView):
    paginate_by = 10
    model = Student


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
    form_class = StudenPaymentDirectForm


class StudentPaymentCreateView(CreateView):
    model = StudentPayment
    form_class = StudenPaymentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, pk=self.kwargs["pk"])
        messages.success(self.request, "Record successfully added.")
        return super().form_valid(form)


class StudentPaymentUpdateView(UpdateView):
    model = StudentPayment
    form_class = StudenPaymentForm


class ExpenseListView(ListView):
    model = Expense


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm