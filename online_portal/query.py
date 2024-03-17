import json
from payment.models import Payment
from customer.models import Customer

from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Count
from django.db.models.functions import ExtractMonth

from django.contrib.auth.decorators import login_required

from django.db.models import F


@login_required
def query_view(request):
    user = request.user
    print(user)
    if user.is_superuser or user.is_admin:
        query1 = Payment.objects.filter(payment_status='COMPLETED').values('id', 'amount', 'payment_status', 'invoice_id')
        count1 = query1.count()
        query2 = Payment.objects.filter(payment_status='INCOMPLETE').values('id', 'amount', 'payment_status', 'invoice_id')
        count2 = query2.count()
        query3 = Customer.objects.filter(file=None).values('id', 'name', 'passport_number', 'applied_country', 'contact', 'status', 'branch', 'invoice')
        count3 = query3.count()
        query4 = Customer.objects.values('status').annotate(count=Count('id'))
        query5 = Customer.objects.filter(file__isnull=False).annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))
    else:
        user_branch = user.branch
        query1 = Payment.objects.filter(payment_status='COMPLETED', payment_creator__branch=user_branch).values('id', 'amount', 'payment_status', 'invoice_id')
        count1 = query1.count()
        query2 = Payment.objects.filter(payment_status='INCOMPLETE', payment_creator__branch=user_branch).values('id', 'amount', 'payment_status', 'invoice_id')
        count2 = query2.count()
        query3 = Customer.objects.filter(file=None, branch=user_branch).values('id', 'name', 'passport_number', 'applied_country', 'contact', 'status', 'branch', 'invoice')
        count3 = query3.count()
        query4 = Customer.objects.filter(branch=user_branch).values('status').annotate(count=Count('id'))
        query5 = Customer.objects.filter(file__isnull=False, branch=user_branch).annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))

    response_data ={
        'Payment_Completed':list(query1),
        'Payment_Complete_Count': count1,
        'Payment_Incomplete':list(query2),
        'Payment_Incomplete_Count': count2,
        'File_Null':list(query3),
        'File_Null_Count': count3,
        'Group_By_Status':list(query4),
        'Group_By_Month_file':list(query5)
    }
    return JsonResponse(response_data, safe=False)

def group_by_branch(request):
    query1 = Payment.objects.filter(payment_status='COMPLETED').values('payment_creator__branch').annotate(
    total_payments=Count('id'),
    # total_amount=Sum('amount')
    ).values('payment_creator__branch', 'total_payments','id', 'amount', 'invoice_id')
    query2 = Payment.objects.filter(payment_status='INCOMPLETE').values('payment_creator__branch').annotate(
    total_payments=Count('id'),
    # total_amount=Sum('amount')
    ).values('payment_creator__branch', 'total_payments','id', 'amount', 'invoice_id')
    query3 = Customer.objects.filter(file=None).annotate(customer_branch=F('branch')).values('branch').annotate(count=Count('id')).values('branch', 'count')

    query4 = Customer.objects.values('status', 'branch').annotate(count=Count('id')).values('status', 'branch', 'count')

    query5 = Customer.objects.filter(file__isnull=False).annotate(customer_branch=F('branch')).annotate(month=ExtractMonth('created_at')).values('branch','month').annotate(count=Count('id'))
    response_data ={
        'Payment_Completed':list(query1),
        'Payment_Incomplete':list(query2),
        'File_Null':list(query3),
        # 'File_Null_Count': count3,
        'Group_By_Status':list(query4),
        'Group_By_Month_file':list(query5)
    }
    return JsonResponse(response_data, safe=False)