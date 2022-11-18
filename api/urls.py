from django.urls import path,include

from api.views import rotatePDF

urlpatterns=[
    path('rotate/',view=rotatePDF,name='rotate pdf pages')
]