from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .forms import *
from .models import *
import json
# Create your views here.

def index(request):
    return render(request,"pages/main_page.html")

@login_required
def my_groups(request):
    groups = request.user.joined_groups.all()

    context = {
        "groups":groups
    }
    return render(request,"pages/group_list.html",context)

@login_required
def group_detail(request,id):
    group = get_object_or_404(ChatGroup,id=id)
    context = {
        "group" :group
    }

    return render(request,"pages/group_detail.html",context)
@login_required
def delete_group(request,id):
    return HttpResponse("delete_group")

@login_required
def group_settings(request,id):
    group = get_object_or_404(ChatGroup,id=id)
    context = {
        "group":group
    }
    return render(request,"pages/group_settings.html",context)

@login_required
def register(request):
    if request.method == "POST" :
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request,user)
            return redirect("chat:my_groups")
    else:
        form = RegisterForm()

    return render(request,"registration/register.html",{"form":form})


@login_required
@require_POST
def change_group_name(request):
    data = json.loads(request.body)
    unique_code = data.get("unique_code",None)
    name = data.get("name",None)
    if unique_code :
        if name :
            group = ChatGroup.objects.get(unique_code=unique_code)
            group.name = name
            group.save()
            context = {
                "status":"ok"
            }
            return JsonResponse(context,status=201)
        else:
            return JsonResponse({"status":"name is empty"},status=400)
    else:
        return JsonResponse({"status":"group dose not exist"},status=404)

def change_group_code(request):
    data = json.loads(request.body)
    unique_code = data.get("unique_code", None)
    if unique_code:
            group = ChatGroup.objects.get(unique_code=unique_code)
            group.unique_code = set_unique()
            group.save()
            context = {
                "status": "ok",
                "url" : f"{request.get_host()}/chat/group/{group.id}",
            }
            return JsonResponse(context, status=201)

    else:
        return JsonResponse({"status": "group dose not exist"}, status=404)

@require_POST
def make_group(request) :
    data = json.loads(request.body)
    name = data.get("name")
    if name :
        group = ChatGroup.objects.create(name=name,creator=request.user)
        Member.objects.create(chat=group,user=request.user)
        context = {
            "status": "ok",
            "url": f"/chat/group/{group.id}",
        }
        return JsonResponse(context,status=201)
    else:
        return JsonResponse({"status":"groups must have a group name"},status=400)