from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from core.models import Student, StudentPayment, Expense, Transaction, Config, Teacher
from core.forms import ExpenseForm, StudenPaymentForm, StudenPaymentDirectForm, StudentForm, TeacherForm
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
                transactions = Transaction.objects.all()
            else:
                transactions = Transaction.objects.filter(created__gte=request.GET.get("start_date"), created__lte=request.GET.get("end_date")).all()
        
        except Exception:
            transactions = Transaction.objects.all()
        
        all_transactions = []
        cash_opening_balance = Config.objects.get(key="cash_opening_balance")
        bank_opening_balance = Config.objects.get(key="bank_opening_balance")
        for trans in transactions:
            if trans.transaction_type == "income":
                income = StudentPayment.objects.get(pk=trans.transaction_id)
                trans.amount = income.paid
                trans.category = income.payment_for
                
                if income.mode == "cash":
                    trans.cash_opening_balance = float(cash_opening_balance.value)
                    trans.cash_closing_balance = trans.cash_opening_balance + income.paid
                    cash_opening_balance.value = trans.cash_closing_balance

                    trans.bank_opening_balance = float(bank_opening_balance.value)
                    trans.bank_closing_balance = trans.bank_opening_balance

                    trans.mode = income.mode
                    bank_opening_balance.value = trans.bank_closing_balance
                
                if income.mode == "online":
                    trans.bank_opening_balance = float(bank_opening_balance.value)
                    trans.bank_closing_balance = trans.bank_opening_balance + income.paid
                    bank_opening_balance.value = trans.bank_closing_balance

                    trans.cash_opening_balance = float(cash_opening_balance.value)
                    trans.cash_closing_balance = trans.cash_opening_balance

                    trans.mode = income.mode
                    cash_opening_balance.value = trans.cash_closing_balance
            
            if trans.transaction_type == "expense":
                expense = Expense.objects.get(pk=trans.transaction_id)
                trans.amount = expense.amount
                trans.category = expense.expense_for

                if expense.mode == "cash":
                    trans.cash_opening_balance = float(cash_opening_balance.value)
                    trans.cash_closing_balance = trans.cash_opening_balance - expense.amount
                    cash_opening_balance.value = trans.cash_closing_balance

                    trans.bank_opening_balance = float(bank_opening_balance.value)
                    trans.bank_closing_balance = trans.bank_opening_balance

                    trans.mode = expense.mode
                    bank_opening_balance.value = trans.bank_closing_balance

                if expense.mode == "online":
                    trans.bank_opening_balance = float(bank_opening_balance.value)
                    trans.bank_closing_balance = trans.bank_opening_balance - expense.amount
                    bank_opening_balance.value = trans.bank_closing_balance

                    trans.cash_opening_balance = float(cash_opening_balance.value)
                    trans.cash_closing_balance = trans.cash_opening_balance

                    trans.mode = expense.mode
                    cash_opening_balance.value = trans.cash_closing_balance

            all_transactions.append(trans)
        
        data = dict(transactions=all_transactions)
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
        result = super().form_valid(form)
        trans = Transaction(transaction_id=self.object.pk, transaction_type="income")
        trans.save()
        messages.success(self.request, "Income successfully added.")
        return result


class StudentPaymentUpdateView(UpdateView):
    model = StudentPayment
    form_class = StudenPaymentForm


class ExpenseListView(ListView):
    model = Expense


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm

    def form_valid(self, form):
        result = super().form_valid(form)
        trans = Transaction(transaction_id=self.object.pk, transaction_type="expense")
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