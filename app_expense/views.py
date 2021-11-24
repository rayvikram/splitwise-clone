from django.db.models.aggregates import Sum
from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .models import Expense
from app_user.views import UserSerializer

class ExpenseSerializer(serializers.ModelSerializer):
    payee_email = serializers.SerializerMethodField()
    payer_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = '__all__'
    
    def get_payee_email(self, obj):
        return UserSerializer(obj.payee).data

    def get_payer_email(self, obj):
        return UserSerializer(obj.payer).data



class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
        
    def get_queryset(self):
        return Expense.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def friend(self, request, pk=None):
        context = Expense.objects.filter(
            created_by=request.user
            ).values('payer__email', 'payee__email').annotate(total_amount=Sum('amount'))
        return Response(context)

    @action(detail=False, methods=["get"])
    def group(self, request, pk=None):
        context = [{"group": 45}] #TODO
        return Response(context)

    @action(detail=False, methods=["get"])
    def overall(self, request, pk=None):
        context = [
            Expense.objects.filter(payer=request.user).aggregate(to_receive=Sum('amount')),
            Expense.objects.filter(payee=request.user).aggregate(to_pay=Sum('amount'))
                   ] 
        return Response(context)

    @action(detail=False, methods=["post"])
    def settleup(self, request, pk=None):
        data = request.data
        if not data.get('friend_email'):
            return Response({"message": "Please send friend email!"}, status=status.HTTP_400_BAD_REQUEST)
        friend = User.objects.filter(email=data.get('friend_email')).first()
        if not friend:
            return Response({"message": "Invalid friend!"}, status=status.HTTP_400_BAD_REQUEST)
        
        to_receive = Expense.objects.filter(payer=request.user, payee=friend).aggregate(to_receive=Sum('amount')).get('to_receive')
        to_pay = Expense.objects.filter(payee=request.user, payer=friend).aggregate(to_pay=Sum('amount')).get('to_pay')
        if to_receive > to_pay: #means friend paid me the difference amount
             Expense.objects.create(
                 payer=friend,
                 payee=request.user,
                 amount=to_receive - to_pay,
                 message="SETTLED UP",
                 expense_type="SETTLED_UP"
             )
             context = {
                 "message": f"Friend paid you and settled up rs {to_receive - to_pay}."
             }
        else: #means I paid him the difference amount
            Expense.objects.create(
                 payer=request.user,
                 payee=friend,
                 amount= to_pay-to_receive,
                 message="SETTLED UP",
                 expense_type="SETTLED_UP"
             )
            context = {
                 "message": f"You paid friend and settled up rs {to_pay-to_receive}."
            }
        return Response(context)
