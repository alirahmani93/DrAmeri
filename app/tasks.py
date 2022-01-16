from celery import shared_task
import asyncio

# from app.views import save_to_output
from app.detecting import DETECTING, save_to_output
from .models import Input, Output


@shared_task
def hello_task(name):
    return f"hello celery to {name}"


async def return_hello():
    await asyncio.sleep(1)
    return 'hello'


@shared_task(name="summation", serializer='json')
def summation(obj, min, max, ):
    a = Input.objects.get(id=obj)
    c_res, m_res, cm_res = DETECTING(f'{a.image}', int(min), int(max))
    save_to_output(a, c_res, m_res, cm_res)
    b = Output.objects.filter(input_ids_id=a.id)[0]
