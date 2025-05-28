from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Sum
from .models import CalendarEvent, Transaction, PettyCash, Bill, Sale
from .serializers import TransactionSerializer, CalendarEventSerializer, PettyCashSerializer, BillSerializer, SaleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import localtime
from django.utils.dateparse import parse_date
from .permissions import IsSuperAdminOrOwner
from django_filters import rest_framework as filters

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
    })

@api_view(["POST"])
def logout_view(request):
    response = Response({"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        response = Response({"message": "Login successful"})

        # Set httpOnly cookies
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return response


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {
        'transaction_type': ['exact'],
        'date': ['exact', 'range', 'gte', 'lte'],
        'category': ['exact'],
    }

    @action(detail=False, methods=['get'])
    def filter_by_category(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            transactions = self.queryset.filter(category__id=category_id)
        else:
            transactions = self.queryset

        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def todays_transactions(self, request):
        local_today = localtime(timezone.now()).date()
        transactions = self.queryset.filter(date=local_today)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def filter_by_transaction_type(self, request):
        transaction_type = request.query_params.get('transaction_type')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        filters = {}

        if transaction_type:
            filters["transaction_type"] = transaction_type
        if date_from and date_to:
            filters["date__range"] = [date_from, date_to]
        elif date_from:
            filters["date__gte"] = date_from
        elif date_to:
            filters["date__lte"] = date_to

        transactions = self.queryset.filter(**filters) if filters else self.queryset

        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today_total_transactions(self, request):
        today_param = request.query_params.get("today")
        if today_param:
            try:
                today = parse_date(today_param)
            except ValueError:
                today = localtime(timezone.now()).date()
        else:
            today = localtime(timezone.now()).date()

        transactions = self.get_queryset().filter(date=today)
        total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        })

    @action(detail=False, methods=['get'])
    def yesterday_total_transactions(self, request):
        yesterday = (localtime(timezone.now()) - timedelta(days=1)).date()
        transactions = self.get_queryset().filter(date=yesterday)
        total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        local_today = localtime(timezone.now()).date()
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        filters = {}

        if date_from and date_to:
            filters["date__range"] = [date_from, date_to]
        elif date_from:
            filters["date__gte"] = date_from
        elif date_to:
            filters["date__lte"] = date_to

        transactions = self.queryset
        total_income = transactions.filter(transaction_type='income', **filters).aggregate(Sum('amount'))['amount__sum'] if filters else self.queryset.filter(transaction_type='income',
            date__lte=local_today).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='expense', **filters).aggregate(Sum('amount'))['amount__sum'] if filters else self.queryset.filter(transaction_type='expense', 
            date__lte=local_today).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        })

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def todays_events(self, request):
        local_today = localtime(timezone.now()).date()
        events = self.queryset.filter(start_date__date=local_today)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
    
class PettyCashViewSet(viewsets.ModelViewSet):
    queryset = PettyCash.objects.all()
    serializer_class = PettyCashSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def todays_petty_cash(self, request):
        local_today = localtime(timezone.now()).date()
        petty_cash = self.queryset.filter(date=local_today)
        serializer = self.get_serializer(petty_cash, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_petty_cash(self, request):
        pending_petty_cash = self.queryset.filter(isApproved=False)
        serializer = self.get_serializer(pending_petty_cash, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total_petty_cash(self, request):
        approved_petty_cash = self.queryset.filter(isApproved=True)
        total_petty_cash = approved_petty_cash.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total_petty_cash": total_petty_cash})
    
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def todays_bills(self, request):
        local_today = localtime(timezone.now()).date()
        bills = self.queryset.filter(due_date=local_today)
        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_bills(self, request):
        pending_bills = self.queryset.filter(is_paid=False)
        serializer = self.get_serializer(pending_bills, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total_paid_bills(self, request):
        paid_bills = self.queryset.filter(is_paid=True)
        total_paid_bills = paid_bills.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total_paid_bills": total_paid_bills})
    
    @action(detail=False, methods=['get'])
    def total_unpaid_bills(self, request):
        unpaid_bills = self.queryset.filter(is_paid=False)
        total_unpaid_bills = unpaid_bills.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total_unpaid_bills": total_unpaid_bills})
    
    @action(detail=False, methods=['get'])
    def total_bills(self, request):
        total_bills = self.queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total_bills": total_bills})
    
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def todays_sales(self, request):
        local_today = localtime(timezone.now()).date()
        sales = self.queryset.filter(sale_date=local_today)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total_sales(self, request):
        total_sales = self.queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total_sales": total_sales})