from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen, Request
from urllib.parse import quote      # 한글 인코딩
# from .apikey import * #if using on django , should using .apikey instead apikey
import json
from io import BytesIO
from PIL import Image       # 이미지

# 자기 api key 넣기
USER_API_KEY = '5dfaa778d1bf69df4e25612c3be6f0ca'

def api_genre(import_genres_url):
    url = import_genres_url
    queryParms = '?api_key=' + USER_API_KEY
    request = Request(url + queryParms + '&_type=json')
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    getJson = json.loads(response_body)['genres']
    return getJson

def api_request(request_url):
    queryParms = '?api_key=' + USER_API_KEY
    request = Request(request_url + queryParms + '&_type=json')
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    getJson = json.loads(response_body)
    return getJson

def api_search(search_word):
    url = 'https://api.themoviedb.org/3/search/multi?language=ko&page=1&include_adult=false'
    queryParms = '&api_key=' + USER_API_KEY + '&query=' + quote(search_word)
    request = Request(url + queryParms + '&_type=json')
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    # print(response_body)
    getJson = json.loads(response_body)['results']
    return getJson

# def api_movie(import_genres_url):
#     url = import_genres_url
#     queryParms = '?api_key=' + USER_API_KEY
#     request = Request(url + queryParms + '&_type=json')
#     request.get_method = lambda: 'GET'
#     response_body = urlopen(request).read()
#     getJson = json.loads(response_body)
#     getJson = [['id', getJson['id']],
#                 ['original_title', getJson['original_title']],
#                 ['popularity', getJson['popularity']],
#                 ['poster_path', getJson['poster_path']],
#                 ['release_date', getJson['release_date']],
#                 ['genres', getJson['genres']]]
#     return dict(getJson)
#
# def api_tv(import_genres_url):
#     url = import_genres_url
#     queryParms = '?api_key=' + USER_API_KEY
#     request = Request(url + queryParms + '&_type=json')
#     request.get_method = lambda: 'GET'
#     response_body = urlopen(request).read()
#     getJson = json.loads(response_body)
#     getJson = [['id', getJson['id']],
#                 ['original_name', getJson['original_name']],
#                 ['popularity', getJson['popularity']],
#                 ['poster_path', getJson['poster_path']],
#                 ['first_air_date', getJson['first_air_date']],
#                 ['last_air_date', getJson['last_air_date']],
#                 ['genres', getJson['genres']]]
#     return dict(getJson)

# def api_detail(search_url):
#     queryParms = '?api_key=' + USER_API_KEY
#     request = Request(search_url + queryParms + '&_type=json')
#     request.get_method = lambda: 'GET'
#     response_body = urlopen(request).read()
#     getJson = json.loads(response_body)
#     return getJson

# def api_img(import_img_url):
#     url = 'https://image.tmdb.org/t/p/w500'
#     request = Request(url + import_img_url)
#     request.get_method = lambda: 'GET'
#     response_body = urlopen(request).read()
#     response_img = Image.open(BytesIO(response_body))
#     # print(response_img)
#     return response_img
