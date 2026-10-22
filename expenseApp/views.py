from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView,ListAPIView
from rest_framework import authentication,permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from expenseApp.models import Expense
from expenseApp.serializer import UserSerializer,ExpenseSerializer
from django.contrib.auth.models import User

# Create your views here.

class UserCreateView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class ExpenseCreateListView(ListAPIView,CreateAPIView):
    serializer_class=ExpenseSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields=['category','payment']
    search_fields=['title']
    ordering_fields=['amount','created_at']

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class ExpenseRetrieveUpdateDeleteView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    serializer_class=ExpenseSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'  

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)
