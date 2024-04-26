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
    template_name = "core/core_template.html"

    def get(self, request, *args, **kwargs):
        data = {}
        data.update({
            "student_count": Student.objects.count()
        })
        data.update(StudentPayment.objects.aggregate(Sum("paid", default=0)))
        data.update(Expense.objects.aggregate(Sum("amount", default=0)))
        data.update({"profit": data["paid__sum"] - data["amount__sum"]})
        return render(request, self.template_name, data)


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