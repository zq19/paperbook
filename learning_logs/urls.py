"""定义learning_logs的URL模式"""

from django.conf.urls import url,re_path

from . import views

urlpatterns = [
    #主页
    re_path(r'^$',views.index,name = 'index'), # name为此条url的名字
    # 显示所有主题，主题页
    re_path(r'^topics/$',views.topics,name = 'topics'), # 同上
    # 特定主题的详细页面
    re_path('^topics/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    # 用于用户添加新主题的网页
    re_path('^new_topic/$',views.new_topic,name='new_topic'),
    # 用于用户编写新条目的页面
    re_path('^new_entry/(?P<topic_id>\d+)$',views.new_entry,name='new_entry'),
    # 用于编辑条目的页面
    re_path('^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry'),
    re_path('^delete_entry/(?P<entry_id>\d+)/$',views.delete_entry,name='delete_entry'),
    re_path('^delete_topic/(?P<topic_id>\d+)/$',views.delete_topic,name='delete_topic'),
    re_path('^topics/my_topic/$',views.my_topic,name='my_topic'),
]