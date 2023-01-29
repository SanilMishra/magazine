from django.contrib import admin
from django.urls import path
from . import views

app_name = "magazine"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('change_password/',views.change_password,name="change_password"),
    path('admin_module/',views.admin_module,name="admin_module"),
    path('admin_module/appoint_reviewer',views.appoint_reviewer,name="appoint_reviewer"),
    path('admin_module/remove_reviewer',views.remove_reviewer,name="remove_reviewer"),
    path('admin_module/view_unassigned_articles/',views.view_unassigned_articles,name="view_unassigned_articles"),
    path('admin_module/send_for_review/',views.send_for_review,name="send_for_review"),
    path('admin_module/view_pending_articles/',views.view_pending_articles,name="view_pending_articles"),
    path('admin_module/view_reviewed_articles/',views.view_reviewed_articles,name="view_reviewed_articles"),
    path('admin_module/view_reviewed_articles/<int:article_id>',views.display_article_admin,name="display_article_admin"),
    path('admin_module/admin_view_article/',views.admin_view_article,name="review_article"),
    path('reviewer_module/',views.reviewer_module,name="reviewer_module"),
    path('reviewer_module/reviewer_view_article/',views.reviewer_view_article,name="review_article"),
    path('reviewer_module/reviewed_articles_reviewer/',views.reviewed_articles_reviewer,name="reviewed_articles_reviewer"),
    path('reviewer_module/pending_articles_reviewer',views.pending_articles_reviewer,name="pending_articles_reviewer"),
    path('view_magazine/',views.view_magazine,name="view_magazine"),
    path('create_article/',views.create_article,name="create_article"),
    # path('view_magazine/viewer_article/',views.published_article,name="view_magazine")
    
]