from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view

from sdk.key_generation import generate_random_key
from sdk.storage import create_storage
from sdk.url_processor import process_url, InvalidURLException

storage = create_storage()


@api_view(['GET'])
def go_to(request, key, format=None):
    url = _retrieve_url_by_key(key)
    if not url:
        return JsonResponse(status=404, data={
            'error': 'key not found'
        })

    return HttpResponseRedirect(redirect_to=url)


@api_view(['POST'])
def shorten(request, format=None):
    url = request.data.get('url')
    if not url:
        return JsonResponse(status=400, data={
            'error': 'missing url parameter'
        })

    try:
        url = _process_url(url)
    except InvalidURLException as e:
        return JsonResponse(status=400, data={
            'error': 'invalid URL',
            'details': e.message
        })

    key = _store_url_and_get_key(url)
    return JsonResponse(status=200, data={
        'key': key
    })


def _retrieve_url_by_key(key):
    return storage.get(key)


def _store_pair(key, url):
    return storage.set(key, url)


def _process_url(url):
    return process_url(url)


def _store_url_and_get_key(url):
    while True:
        key = _generate_key()
        if _store_pair(key, url):
            break

    return key


def _generate_key():
    return generate_random_key()