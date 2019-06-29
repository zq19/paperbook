# Create your views here.

from django.shortcuts import render,redirect,get_object_or_404
from .models import Topic,Entry
from django.urls import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

#在这里创建视图


def index(request):
    """学习笔记的主页"""

    return render(request,'learning_logs/index.html')


def check_topic_owner(topic, request):
    """判断主题的拥有者"""
    if topic.owner != request.user:
        raise Http404


def topics(request):
    """显示所有主题"""
    topics = Topic.objects.filter(public=True).order_by('date_added')
    return render(request,'learning_logs/topics.html',{'topics':topics})


def topic(request,topic_id):
    """单击单个主题显示所有条目"""
    topic = get_object_or_404(Topic,id=topic_id)
    # 检测请求主题是否私密，如果私密，判断是否请求者是拥有者
    if topic.public == False:
        check_topic_owner(topic,request)
    entries = topic.entry_set.order_by('-date_added')
    return render(request,'learning_logs/topic.html',{'topic':topic,'entries':entries})


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # post提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return redirect('learning_logs:topics')

    return render(request,'learning_logs/new_topic.html',{'form':form})


@login_required
def new_entry(request,topic_id):
    """添加新条目"""
    topic = get_object_or_404(Topic,id=topic_id)
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # 用户提交了表单数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect(reverse('learning_logs:topic',args=[topic_id]))
    return render(request,'learning_logs/new_entry.html',{'topic':topic,'form':form})


@login_required
def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = get_object_or_404(Entry,id=entry_id)
    topic = entry.topic
    check_topic_owner(topic,request)
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # post提交的数据，对数据进行处理
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('learning_logs:topic',args=[topic.id]))
    return render(request,'learning_logs/edit_entry.html',{'entry':entry,'topic':topic,'form':form})


@login_required
def delete_entry(request,entry_id):
    """删除条目"""
    entry = get_object_or_404(Entry,id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)
    if request.method == 'POST':
        data = request.POST.get('choice')
        if data == '1':
            entry.delete()
            return redirect(reverse('learning_logs:topic',args=[topic.id]))
        else:
            return redirect(reverse('learning_logs:topic',args=[topic.id]))
    return render(request,'learning_logs/delete_entry.html',{'entry':entry})


@login_required
def delete_topic(request,topic_id):
    """删除主题"""
    topic = get_object_or_404(Topic,id=topic_id)
    check_topic_owner(topic, request)
    if request.method == 'POST':
        data = request.POST.get('choice')
        if data == '1':
            topic.delete()
            return redirect('learning_logs:topics')
        else:
            return redirect('learning_logs:topics')
    return render(request,'learning_logs/delete_topic.html',{'topic':topic})

@login_required
def my_topic(request):
    """个人主题中心"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    return render(request,'learning_logs/my_topic.html',{'topics':topics})
