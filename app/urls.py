from django.urls import path
import views

urlpatterns = [
    path('images/get-all', views.get_all__image, name="all-images"),
    path('images/get', views.get__image, name="get-images"),
    path('images/add', views.add__image, name="add-images"),
    path('images/delete', views.delete__image, name="delete-images"),
    path('images/update', views.update__image, name="update-images"),

    path('result/get-all', views.get_all__result, name="all-results"),
    path('result/get', views.get__result, name="get-results"),
    path('result/add', views.add__result, name="add-results"),
    path('result/delete', views.delete__result, name="delete-results"),

]
