from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", home,name= "home"),
    path("notes", notes,name= "notes"),
    path("delete_note/<int:pk>", delete_note,name= "delete_note"),
    path("notes_detail/<int:pk>", NotesDetailView.as_view(),name= "notes_detail"),
    path("homework", homework,name= "homework"),
    path("update_homework/<int:pk>", update_homework,name= "update_homework"),
    path("delete_homework/<int:pk>", delete_homework,name= "delete_homework"),
    path("youtube", youtube,name= "youtube"),
    path("todo", todo,name= "todo"),
    path("update_todo/<int:pk>", update_todo,name= "update_todo"),
    path("delete_todo/<int:pk>", delete_todo,name= "delete_todo"),
    path("books", books,name= "books"),
    path("dictionary", dictionary,name= "dictionary"),
    path("wiki", wiki,name= "wiki"),
    path("conversion", conversion,name= "conversion"),
    path("register/", register,name= "register"),
    path("login/", auth_views.LoginView.as_view(template_name='dashboard/login.html'), name="login"),
    path("profile/", profile, name="profile"),
    path("logout", logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)