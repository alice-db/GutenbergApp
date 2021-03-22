import requests
from rest_framework.views import APIView
from rest_framework.response import Response

import json
import os

from mygutenberg import util
from django.conf import settings

from django.http import Http404
from django.http import JsonResponse
