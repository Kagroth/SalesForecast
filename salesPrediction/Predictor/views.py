from django.shortcuts import render

# Create your views here.

from time import sleep
from random import randrange
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .neuralnetwork import predict
import json

# glowna strona aplikacji
def index(request):
    return render(request, 'Predictor/index.html')
    #return HttpResponse("Wtf")

def predictSales(request):
    #kod dotyczący predykcji sprzedazy
    sleep(1)
    monthsList = ['Styczen', 'Luty', 'Marzec', 'Kwiecien', 'Maj',
                  'Czerwiec', 'Lipiec', 'Sierpien', 'Wrzesien',
                  'Pazdziernik', 'Listopad', 'Grudzien']
    salesCount = {}
    for month in monthsList:
        salesCount[month] = randrange(1, 150)

    if request.method == 'POST':
        dataDict = json.loads(request.body)
        print(dataDict)
        print(type(dataDict))

    for monthNumber in range(12):
        print("Przed predykcja: ", dataDict)
        nextMonthData = predict(salesData=dataDict)
        for month in nextMonthData:
            dataDict.pop(month)
            dataDict[month] = nextMonthData[month]
            break
        print("Po predykcji: ", dataDict)

    return JsonResponse(dataDict)
