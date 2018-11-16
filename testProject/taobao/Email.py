from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse



def send(request):
    if request.method == "GET":

        for i in range(0, 1000):
            send_mail(i,
                      '这是武器',
                      settings.EMAIL_FROM,
                      ['1025343964@qq.com'],
                      fail_silently=False)
    return HttpResponse('ok')

