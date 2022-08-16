from django.shortcuts import render
from .models import Deal, Client
from django.views import generic
from datetime import datetime
from  .return_top_customer import return_top_customer_with_items

def start_page(request):
    return render(request, 'proc_deals/start.html', {'start': ''})

class ResultsView(generic.ListView):
    model = Client
    template_name = 'proc_deals/result.html'


def result(request):

    Deal.objects.all().delete()
    Client.objects.all().delete()

    deals_file_csv = request.FILES['file_csv']



    for line in deals_file_csv:
        deal = Deal()
        deal.create_deals_of_line(line)

    top_customer = return_top_customer_with_items()

    for customer in top_customer:
        client = Client()
        client.username = customer['customer']
        client.gems = customer['items']
        client.spent_money = customer['total_sum']
        client.save()

    return render(request, 'proc_deals/result.html', {'clients': Client.objects.all()})



