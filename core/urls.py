from django.urls import path, include
from django.contrib.auth.decorators import login_required
from core.views import (CoreViewIndex, StudentListView, StudentDetailView, StudentCreateView, 
                        StudentUpdateView, StudentPaymentListView, StudentPaymentCreateView, 
                        StudentPaymentDetailView, StudentPaymentUpdateView, ExpenseListView, 
                        ExpenseCreateView, ExpenseUpdateView, StudentPaymentDirectCreateView,
                        PrintStudentDetails, PrintStudentsIDCard, PrintStudentIncome, TeacherCreateView,
                        TeacherUpdateView, BalanceSheet, TeacherListView, TeacherDetailView, PrintTeachersIDCard)

urlpatterns = [
    path("", login_required(CoreViewIndex.as_view()), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", login_required(CoreViewIndex.as_view()), name="dashboard"),
    path("students/", login_required(StudentListView.as_view()), name="students"),
    path("student/<int:pk>/", login_required(StudentDetailView.as_view()), name="student-details"),
    path("student/add/", login_required(StudentCreateView.as_view()), name="student-add"),
    path("student/<int:pk>/update/", login_required(StudentUpdateView.as_view()), name="student-update"),
    path("student-payments/", login_required(StudentPaymentListView.as_view()), name="student-payments"),
    path("student-payment-direct/add/", login_required(StudentPaymentDirectCreateView.as_view()), name="student-payment-direct-add"),
    path("student-payment/<int:pk>/add/", login_required(StudentPaymentCreateView.as_view()), name="student-payment-add"),
    path("student-payment/<int:pk>/update/", login_required(StudentPaymentUpdateView.as_view()), name="student-payment-update"),
    path("expenses/", login_required(ExpenseListView.as_view()), name="expenses"),
    path("expense/add/", login_required(ExpenseCreateView.as_view()), name="expense-add"),
    path("expense/<int:pk>/update/", login_required(ExpenseUpdateView.as_view()), name="expense-update"),
    path("printout-student/<int:pk>", login_required(PrintStudentDetails.as_view()), name="print-student"),
    path("printout-payment/<int:pk>", login_required(PrintStudentIncome.as_view()), name="print-income"),
    path("printout-idcards/", login_required(PrintStudentsIDCard.as_view()), name="print-idcards"),
    path("printout-teachers-idcards/", login_required(PrintTeachersIDCard.as_view()), name="print-teachers-idcards"),
    path("balance-sheet/", login_required(BalanceSheet.as_view()), name="balance-sheet"),
    path("teachers/", login_required(TeacherListView.as_view()), name="teachers"),
    path("teacher/<int:pk>/", login_required(TeacherDetailView.as_view()), name="teacher-details"),
    path("teacher/add/", login_required(TeacherCreateView.as_view()), name="teacher-add"),
    path("teacher/<int:pk>/update/", login_required(TeacherUpdateView.as_view()), name="teacher-update"),
]