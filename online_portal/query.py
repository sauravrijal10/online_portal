import json
from payment.models import Payment
from customer.models import Customer

from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Count
from django.db.models.functions import ExtractMonth


def query_view(request):
    query1 = Payment.objects.filter(payment_status='COMPLETED').values('id', 'amount', 'payment_status', 'invoice_id')
    count1 = query1.count()
    query2 = Payment.objects.filter(payment_status='INCOMPLETE').values('id', 'amount', 'payment_status', 'invoice_id')
    count2 = query2.count()
    query3 = Customer.objects.filter(file=None).values('id', 'name', 'passport_number', 'applied_country', 'contact', 'status', 'branch', 'invoice')
    count3 = query3.count()
    query4 = Customer.objects.values('status').annotate(count=Count('id'))
    query5 = Customer.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))

    response_data ={
        'Payment_Completed':list(query1),
        'Payment_Complete_Count': count1,
        'Payment_Incomplete':list(query2),
        'Payment_Incomplete_Count': count2,
        'File_Null':list(query3),
        'File_Null_Count': count3,
        'Group_By_Status':list(query4),
        'Group_By_Month':list(query5)
    }
    return JsonResponse(response_data, safe=False)
