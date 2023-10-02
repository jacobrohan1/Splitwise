from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Expense, ExpenseParticipant
from .serializers import UserSerializer, ExpenseSerializer, ExpenseParticipantSerializer
from django.db.models import Sum

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

@api_view(['GET'])
def user_expenses(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    expenses = Expense.objects.filter(participants=user)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def show_balances(request):
    users = User.objects.all()
    users_data = []

    for user in users:
        # Calculate the balance for each user
        user_balance = ExpenseParticipant.objects.filter(participant=user).aggregate(Sum('share'))['share__sum'] or 0
        print(f"User: {user}, Balance: {user_balance}")
        # Create a dictionary with user data and balance
        user_data = {
            "id": user.id,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "mobile_number": user.mobile_number,
            "balance": user_balance  # Assign the calculated balance
        }
        users_data.append(user_data)

    return Response(users_data)


from decimal import Decimal  # Import Decimal

@api_view(['POST'])
def split_expense(request):
    data = request.data
    payer_id = data.get('payer')
    description = data.get('description')
    amount = data.get('amount')
    expense_type = data.get('expense_type')
    participants = data.get('participants')
    shares = data.get('shares')

    try:
        payer = User.objects.get(user_id=payer_id)
    except User.DoesNotExist:
        return Response({"error": "Payer does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    if expense_type == 'EQUAL':
        if abs(sum(shares) - amount) >= 0.01:
            return Response({"error": "Invalid expense distribution"}, status=status.HTTP_400_BAD_REQUEST)
    elif expense_type == 'EXACT':
        if abs(sum(shares) - amount) >= 0.01:
            return Response({"error": "Invalid expense distribution"}, status=status.HTTP_400_BAD_REQUEST)
    elif expense_type == 'PERCENT':
        if abs(sum(shares) - 100.0) >= 0.01:
            return Response({"error": "Invalid expense distribution"}, status=status.HTTP_400_BAD_REQUEST)
    
    expense = Expense.objects.create(payer=payer, description=description, amount=amount, expense_type=expense_type)
    
    for participant_id, share in zip(participants, shares):
        try:
            participant = User.objects.get(user_id=participant_id)
        except User.DoesNotExist:
            expense.delete()
            return Response({"error": "Participant does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        share_decimal = Decimal(share)  # Convert share to Decimal
        payer.balance += share_decimal  # Update payer's balance
        payer.save()  # Save the updated payer balance

        # For participants other than the payer, deduct their shares
        if participant != payer:
            participant.balance -= share_decimal  # Update participant's balance
            participant.save()  # Save the updated participant balance

        ExpenseParticipant.objects.create(expense=expense, participant=participant, share=share_decimal)
    
    return Response({"message": "Expense added successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def check_user_balance(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    user_balance = user.balance  # Assuming you have a 'balance' field in your User model

    return Response({"user_id": user.user_id, "balance": user_balance})