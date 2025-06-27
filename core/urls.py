from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView
from django.shortcuts import redirect

urlpatterns = [
    # 🏠 Root - Redirect to Dashboard
    path('', lambda request: redirect('dashboard'), name='home'),

    # 🔐 Authentication
    path('login/', CustomLoginView.as_view(), name='login'),       # Custom Login View
    path('logout/', LogoutView.as_view(), name='logout'),          # Logout
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),

    # 🏠 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 👤 Candidate Management
    path('register/', views.register_candidate, name='register_candidate'),
    path('candidate/<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
    path('candidate/<int:candidate_id>/edit/', views.edit_candidate, name='edit_candidate'),
    path('deleted-candidates/', views.deleted_candidates, name='deleted_candidates'),

    # 💬 Comments
    path('comments/', views.comments_view, name='comments'),
    path('candidates/<int:candidate_id>/comments/', views.comment_section, name='comment_section'),

    # 🧑‍🤝‍🧑 Volunteer Management
    path('volunteers/', views.manage_volunteers, name='manage_volunteers'),
    path('volunteer/<int:id>/edit/', views.edit_volunteer, name='edit_volunteer'),
    path('volunteer/<int:id>/delete/', views.delete_volunteer, name='delete_volunteer'),
    path('volunteer-list/', views.volunteer_list, name='volunteer_list'),
    path('volunteer-candidates/', views.volunteer_view_candidates, name='volunteer_candidates'),

    # 📅 Attendance & Follow-Up
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('follow_up_report/', views.follow_up_report, name='follow_up_report'),
    path('follow-up/candidates/', views.candidates_by_status, name='get_candidates_by_status'),

    # 📤 Communication
    path('compose-email/', views.compose_email, name='compose_email'),
    path('compose-sms/', views.compose_sms, name='compose_sms'),

    path('export-excel/', views.export_candidates_excel, name='export_candidates_excel'),

]

# from django.urls import path
# from . import views
# from .views import CustomLoginView
# from django.contrib.auth.views import LogoutView
# from django.contrib.auth.views import LoginView

# urlpatterns = [
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('register/', views.register_candidate, name='register_candidate'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('logout/confirm/', views.logout_confirm, name='logout_confirm'),
#     path('volunteers/', views.manage_volunteers, name='manage_volunteers'),  # ✅ Correct name
#     path('candidates/<int:candidate_id>/comments/', views.comment_section, name='comment_section'),
#     path('volunteer-candidates/', views.volunteer_view_candidates, name='volunteer_candidates'),
#     path('volunteer-list/', views.volunteer_list, name='volunteer_list'),
#     path('attendance/', views.attendance_list, name='attendance_list'),
#     path('deleted-candidates/', views.deleted_candidates, name='deleted_candidates'),
#     path('follow_up_report/', views.follow_up_report, name='follow_up_report'),
#     path('volunteer/<int:id>/edit/', views.edit_volunteer, name='edit_volunteer'),
#     path('volunteer/<int:id>/delete/', views.delete_volunteer, name='delete_volunteer'),
#     path('compose-email/', views.compose_email, name='compose_email'),
#     path('compose-sms/', views.compose_sms, name='compose_sms'),
#     path('candidate/<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
#     path('candidate/<int:candidate_id>/edit/', views.edit_candidate, name='edit_candidate'),
#     path("accounts/logout/", LogoutView.as_view(), name="logout"),
#     path('follow-up/candidates/', views.candidates_by_status, name='get_candidates_by_status'),
#      path('comments/', views.comments_view, name='comments'),
#      path('login/', LoginView.as_view(), name='login'),


 
# ]