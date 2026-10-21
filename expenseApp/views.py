from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView,ListAPIView
from rest_framework import authentication,permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from expenseApp.models import Expense
from expenseApp.serializer import UserSerializer,ExpenseSerializer
from django.contrib.auth.models import User

# Create your views here.

# 1. User Registration View
class UserCreateView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

# 2. List and Create Expenses View
class ExpenseCreateListView(ListAPIView,CreateAPIView):
    serializer_class=ExpenseSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields=['category','payment']
    search_fields=['title']
    ordering_fields=['amount','created_at']

    def get_queryset(self):
        # Only return expenses belonging to the logged-in user
        return Expense.objects.filter(owner=self.request.user)

    def perform_create(self,serializer):
        # Automatically assign the logged-in user as the owner
        serializer.save(owner=self.request.user)

# 3. Retrieve, Update, and Delete Expense View (Using <int:id>)
class ExpenseRetrieveUpdateDeleteView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'  

    def get_queryset(self):
        # Ensure users can only access or modify their own expenses
        return Expense.objects.filter(owner=self.request.user)
