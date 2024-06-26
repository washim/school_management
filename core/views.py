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


class PrintBalanceSheet(View):
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
        
        return render(request, "core/printout_balancesheet.html", data)


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
        if request.GET.get("records"):
            arr_data = Student.objects.filter(identity_card_issued="No").exclude(photo="").all()[:int(request.GET.get("records"))]
        else:
            arr_data = Student.objects.filter(identity_card_issued="No").exclude(photo="").all()
        
        data = dict(students=arr_data)
        return render(request, "core/printout_students_id_card.html", data)


class PrintTeachersIDCard(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("records"):
            arr_data = Teacher.objects.filter(identity_card_issued="No").exclude(photo="").all()[:int(request.GET.get("records"))]
        else:
            arr_data = Teacher.objects.filter(identity_card_issued="No").exclude(photo="").all()

        data = dict(teachers=arr_data)
        return render(request, "core/printout_teachers_id_card.html", data)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_income"] = self.get_queryset().filter(mode="cash").aggregate(paid_sum=Sum("tuition_fee_paid", default=0) + Sum("admission_fee_paid", default=0) + Sum("learning_material_fee_paid", default=0) + Sum("others_fee_paid", default=0))
        context["total_income_online"] = self.get_queryset().filter(mode="online").aggregate(paid_sum=Sum("tuition_fee_paid", default=0) + Sum("admission_fee_paid", default=0) + Sum("learning_material_fee_paid", default=0) + Sum("others_fee_paid", default=0))
        return context

    def get_queryset(self, **kwargs):
       qs = super().get_queryset(**kwargs)
       
       if self.request.GET.get('start_date') and self.request.GET.get('end_date'):
            return qs.filter(created__gte=self.request.GET.get("start_date"), created__lte=self.request.GET.get("end_date"))
       
       else:
            return qs.all()


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
        trans = Transaction(transaction_id=self.object.pk, transaction_type="income", details=self.object.student, 
                            mode=self.object.mode, debit=0, credit=paid, closing=closing + paid)
        trans.save()
        messages.success(self.request, "Income successfully added.")
        
        return result


class StudentPaymentCreateView(CreateView):
    model = StudentPayment
    form_class = StudentPaymentForm

    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, pk=self.kwargs["pk"])
        result = super().form_valid(form)
        closing = 0

        try:
            latest = Transaction.objects.filter(mode=self.object.mode).last()
            closing = latest.closing
        except Exception:
            pass

        paid = self.object.tuition_fee_paid + self.object.admission_fee_paid + self.object.learning_material_fee_paid + self.object.others_fee_paid
        trans = Transaction(transaction_id=self.object.pk, transaction_type="income", details=self.object.student, 
                            mode=self.object.mode, debit=0, credit=paid, closing=closing + paid)
        trans.save()
        messages.success(self.request, "Income successfully added.")
        
        return result


class StudentPaymentUpdateView(UpdateView):
    model = StudentPayment
    form_class = StudentPaymentForm

    def form_valid(self, form):
        previous_data = get_object_or_404(StudentPayment, pk=self.object.pk)
        previous_paid = previous_data.tuition_fee_paid + previous_data.admission_fee_paid + previous_data.learning_material_fee_paid + previous_data.others_fee_paid

        result = super().form_valid(form)
        closing = 0

        try:
            latest = Transaction.objects.filter(mode=self.object.mode).last()
            closing = latest.closing
        except Exception:
            pass

        current_paid = self.object.tuition_fee_paid + self.object.admission_fee_paid + self.object.learning_material_fee_paid + self.object.others_fee_paid
        change = current_paid - previous_paid

        if change:
            if change > 0:
                credit = change
                debit = 0
                close = closing + credit
            else:
                credit = 0
                debit = abs(change)
                close = closing - debit

            trans = Transaction(transaction_id=self.object.pk, transaction_type="income", details=str(self.object.student) + " - Adj*", 
                                mode=self.object.mode, debit=debit, credit=credit, closing=close)
            trans.save()
            messages.success(self.request, "Income successfully updated.")

        return result


class ExpenseListView(ListView):
    model = Expense

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_expense"] = self.get_queryset().filter(mode="cash").aggregate(Sum("amount", default=0))
        context["total_expense_online"] = self.get_queryset().filter(mode="online").aggregate(Sum("amount", default=0))
        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        
        if self.request.GET.get('start_date') and self.request.GET.get('end_date'):
            return qs.filter(created__gte=self.request.GET.get("start_date"), created__lte=self.request.GET.get("end_date"))
        
        else:
            return qs.all()


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

    def form_valid(self, form):
        previous_data = get_object_or_404(Expense, pk=self.object.pk)
        
        result = super().form_valid(form)
        closing = 0
        
        try:
            latest = Transaction.objects.filter(mode=self.object.mode).last()
            closing = latest.closing
        except Exception:
            pass

        change = self.object.amount - previous_data.amount

        if change:
            if change > 0:
                credit = 0
                debit = change
                close = closing - debit
            else:
                credit = abs(change)
                debit = 0
                close = closing + credit

            trans = Transaction(transaction_id=self.object.pk, transaction_type="expense", details=self.object.details + " - Adj*",
                                mode=self.object.mode, debit=debit, credit=credit, closing=close)
            trans.save()
            messages.success(self.request, "Expense successfully added.")

        return result


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