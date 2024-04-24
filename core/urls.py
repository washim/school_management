from django.urls import path, include
from django.contrib.auth.decorators import login_required
from core.views import (CoreViewIndex, StudentListView, StudentDetailView, StudentCreateView, 
                        StudentUpdateView, StudentPaymentListView, StudentPaymentCreateView, 
                        StudentPaymentDetailView, StudentPaymentUpdateView, ExpenseListView, 
                        ExpenseCreateView, ExpenseUpdateView, StudentPaymentDirectCreateView)

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
]