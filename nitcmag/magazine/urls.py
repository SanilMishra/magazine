from django.contrib import admin
from django.urls import path
from . import views

app_name = "magazine"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('admin_module/',views.admin_module,name="admin_module"),
    path('admin_module/view_assigned_articles/',views.view_assigned_articles,name="view_assigned_articles"),
    path('admin_module/send_for_review/',views.send_for_review,name="send_for_review"),
    path('admin_module/view_pending_articles/',views.view_pending_articles,name="view_pending_articles"),
    path('admin_module/view_reviewed_articles/',views.view_reviewed_articles,name="view_reviewed_articles"),
    path('reviewer_module/',views.reviewer_module,name="reviewer_module"),
    path('reviewer_module/reviewed_articles_reviewer/',views.reviewed_articles_reviewer,name="reviewed_article_reviewer"),
    path('reviewer_module/pending_articles_reviewer',views.pending_articles_reviewer,name="pending_articles_reviewer"),
    path('view_magazine/',views.view_magazine,name="view_magazine")
]