from django.urls import reverse

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from .models import Input, Output
from app.tasks import summation


def call_celery(target, min, max, request):
    print("in call_celery: ", target, min, max)
    summation.delay(target, min, max)


@csrf_exempt
def index(request):
    if request.method == 'POST':
        if request.FILES:
            if int(request.POST.get("min", None)) >= 50 and int(request.POST.get("max", None)) <= 500:
                obj = Input.objects.create(image=request.FILES.get("image"), variable_1=int(request.POST.get("min")),
                                           variable_2=int(request.POST.get("max")))

                call_celery(obj.id, int(request.POST.get("min")), int(request.POST.get("max")), request)

                return redirect(reverse('result', kwargs={'id': obj.id}))
        else:
            return HttpResponse(request.FILES)
    if request.method == 'GET':
        return render(request, 'app.html')


def result(request, id):
    try:
        obj = Output.objects.filter(input_ids_id=id)[0]
        if not obj:
            return render(request, 'result.html', {'results': 0, "wrong": True})
        target = Output.objects.filter(input_ids_id=id).delete()
        return render(request, 'result.html', {'results': obj})
    except:
        return render(request, 'result.html', {'results': 0, "wrong": True})


def get_images(request, id):
    print("here")
    try:
        obj = Output.objects.filter(input_ids_id=id)[0]
        if obj:
            print(type(obj), obj)
            render(request, 'result.html', {'results': obj})
        return False
        # return render(request, 'app.html', {'input': inputq})
    except:
        return False
