import json
from payment.models import Payment
from payment.serializers import PaymentSerializer
from customer.models import Customer
from customer.serializers import CustomerSerializer

from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Count
from django.db.models.functions import ExtractMonth


def query_view(request):
    query1 = Payment.objects.filter(payment_status='COMPLETED')
    query2 = Payment.objects.filter(payment_status='INCOMPLETE')
    query3 = Customer.objects.filter(file=None)
    query4 = Customer.objects.values('status').annotate(count=Count('id'))
    query5 = Customer.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))


    serializer1 = PaymentSerializer(query1, many=True)
    serializer2 = PaymentSerializer(query2, many=True)
    serializer3 = CustomerSerializer(query3, many=True)
    serializer4 = CustomerSerializer(query4, many=True)
    # serialized_data_query1 = serialize('json', query1)
    # deserialized_data_query1 = json.loads(serialized_data_query1)

    response_data ={
        'Payment_Completed':serializer1.data,
        'Payment_Incomplete':serializer2.data,
        'File_Null':serializer3.data,
        'Group_By_Status':list(query4),
        'Group_By_Month':list(query5)
    }
    return JsonResponse(response_data, safe=False)
