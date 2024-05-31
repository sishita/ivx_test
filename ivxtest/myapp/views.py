from django.contrib import messages
from django.shortcuts import render, redirect

from myapp.api import ApiClient, ApiResult
from myapp.models import AiAnalysisLog


def index(request):
    return render(request, 'myapp/index.html')


# Create your views here.
def analysis(request):
    if 'image_path' not in request.POST or request.POST['image_path'] == '':
        messages.warning(request, 'image_pathを指定してください。')
        return render(request, 'myapp/index.html')
    if len(request.POST['image_path']) > 255:
        messages.warning(request, 'image_pathは255文字以内で指定してください。')
        return render(request, 'myapp/index.html')

    image_path = request.POST['image_path']
    result = ApiClient().post(image_path)
    AiAnalysisLog.objects.create_log(result)
    match result:
        case ApiResult():
            return redirect('/')
        case _:
            messages.warning(request, 'APIリクエストでエラーが発生しました。')
            return redirect('/')
