import http

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import ClientRequest, Log, ModelResult


# Create your views here.


def process__image(image, method, var):
    pass


############  Input Image  ############

@require_http_methods(["GET"])
def get__image(request, pk):
    target_image = ClientRequest.objects.filter(client_request__user=request.user, pk=pk).filter()
    return render(request, "main.html", {"target_image": target_image}, status=http.HTTPStatus.OK)


@require_http_methods(["GET"])
def get_all__image(request):
    all_images = ClientRequest.objects.filter(client_request__user=request.user)
    return render(request, "main.html", {"all_images": all_images}, status=http.HTTPStatus.OK)


@require_http_methods(["POST"])
def add__image(request):
    try:
        ClientRequest.objects.create(request.POST)
        return render(request, "content.html", status=http.HTTPStatus.CREATED)
    except:
        return render(request, "main.html", {"msg": "Wrong DATA"}, status=http.HTTPStatus.NOT_FOUND)


@require_http_methods(["DELETE"])
def delete__image(request):
    target_image = ClientRequest.objects.filter(pk=request.POST["resultId"]).first()
    if target_image:
        target_image.delete()
        return render(request, "main.html", {"target_image": target_image}, status=http.HTTPStatus.OK)
    return render(request, "main.html", {"msg": "Wrong ID"}, status=http.HTTPStatus.NOT_FOUND)


@require_http_methods(["UPDATE"])
def update__image(request):
    target_image = ClientRequest.objects.filter(pk=request.POST["resultId"]).first()
    if target_image:
        target_image.user = request.POST["user"]
        target_image.image = request.POST["image"]
        target_image.name = request.POST["name"]
        target_image.description = request.POST["description"]
        target_image.method = request.POST["method"]
        target_image.save()
        return render(request, "main.html", {"target_image": target_image}, status=http.HTTPStatus.OK)
    return render(request, "main.html", {"msg": "Wrong ID"}, status=http.HTTPStatus.NOT_FOUND)


############  Result Image  ############


@require_http_methods(["GET"])
def get_all__result(request):
    all_result = ModelResult.objects.filter(client_request__user=request.user)
    if all_result:
        return render(request, "main.html", {"all_result": all_result}, status=http.HTTPStatus.OK)
    return render(request, "main.html", {"msg": "No Result"}, status=http.HTTPStatus.NOT_FOUND)


@require_http_methods(["GET"])
def get__result(request, pk):
    target_result = ModelResult.objects.filter(client_request__user=request.user, pk=pk).filter()
    if target_result:
        return render(request, "main.html", {"target_result": target_result}, status=http.HTTPStatus.OK)
    return render(request, "main.html", {"msg": "Wrong ID"}, status=http.HTTPStatus.NOT_FOUND)


@require_http_methods(["POST"])
def add__result(request):
    result = ModelResult.objects.create(request.POST)
    result.save()
    return render(request, "main.html", {"msg": "Created"}, status=http.HTTPStatus.OK)


@require_http_methods(["DELETE"])
def delete__result(request):
    target_result = ModelResult.objects.filter(pk=request.POST["resultId"]).first()
    if target_result:
        target_result.delete()
        return render(request, "main.html", {"target_result": target_result}, status=http.HTTPStatus.OK)
    return render(request, "main.html", {"msg": "Wrong ID"}, status=http.HTTPStatus.NOT_FOUND)
