from django.shortcuts import render
from aids.models import SchoolInfo


def page_not_found(request):
    infor = SchoolInfo.all()
    context = {'tittle': 'The page is not found', 'info': infor}
    return render(request, 'error.html', context)


def error(request):
    infor = SchoolInfo.all()
    context = {'tittle': 'The page is been worked on', 'info': infor}
    return render(request, 'error.html', context)


def permission_denied(request):
    infor = SchoolInfo.all()
    context = {'tittle': 'Permission Denied', 'info': infor}
    return render(request, 'error.html', context)


def bad_request(request):
    infor = SchoolInfo.all()
    context = {'tittle': 'Bad Request', 'info': infor}
    return render(request, 'error.html', context)

# handler404 = 'sch.views.page_not_found'
# handler500 = 'sch.views.error'
# handler403 = 'sch.views.permission_denied'
# handler400 = 'sch.views.bad_request'
