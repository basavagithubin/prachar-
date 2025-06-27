from django.contrib import admin
from .models import Candidate, VolunteerProfile, Assignment, Comment, EmailLog, SMSLog, Volunteer
from .models import AttendanceResetTracker
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'assigned_volunteer']  # Removed 'attended'

admin.site.register(VolunteerProfile)
admin.site.register(Assignment)
admin.site.register(Comment)
admin.site.register(EmailLog)
admin.site.register(SMSLog)
admin.site.register(Volunteer)

admin.site.register(AttendanceResetTracker)

# core/admin.py

from django.contrib import admin
from .models import CandidateComment

@admin.register(CandidateComment)
class CandidateCommentAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('candidate__name', 'comment')
