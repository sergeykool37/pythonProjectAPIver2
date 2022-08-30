from .models import  Deal
from django.db.models import Sum, Count

def return_top_customer_with_items():

    rich_customer = Deal.objects.values('customer')\
        .annotate(total_sum=Sum('total'))\
        .order_by('-total_sum')[:5]

    items_rich_customer = Deal.objects.values('customer','item')\
        .filter(customer__in=rich_customer.values('customer'))\
        .distinct()

    items_rich_customer__gt_1 = items_rich_customer.values('item')\
        .annotate(count_customer=Count('customer', distinct=True))\
        .filter(count_customer__gt=1).values('item')

    items_rich_customer = items_rich_customer.filter(item__in=items_rich_customer__gt_1)

    ans = []
    record = {'customer': '',
              'items': '',
              'total_sum': 0}

    for customer in rich_customer:
        record['customer'] = customer['customer']
        record['total_sum'] = customer['total_sum']
        for item in items_rich_customer:
            if item['customer'] == record['customer']:
                if record['items'] == '':
                    record['items'] = item['item']
                else:
                    record['items'] = record['items'] + ', ' + item['item']
        if record['customer'] != '':
            ans.append(record)
            record = {'customer': '',
                      'items': '',
                      'total_sum': 0}
    return ans

