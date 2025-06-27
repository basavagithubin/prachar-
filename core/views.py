from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mass_mail
from datetime import date

from .models import (
    Candidate, Comment, Volunteer, Attendance, FollowUpSession,
    EmailLog, AttendanceResetTracker
)
from .forms import CandidateForm, CommentForm, LoginForm, VolunteerForm
from .utils import send_bulk_email, send_bulk_sms
from .choices import FOLLOW_UP_STATUS_CHOICES
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages

from .models import Candidate, Volunteer, Attendance, AttendanceResetTracker, FollowUpSession, FOLLOW_UP_STATUS_CHOICES
from .models import CandidateComment

from .models import Candidate, Volunteer, Comment, Attendance, FollowUpSession, EmailLog, SMSLog


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from datetime import date
from .models import (
    Candidate, Volunteer, Attendance, FollowUpSession, 
    AttendanceResetTracker, CandidateComment
)
from .choices import FOLLOW_UP_STATUS_CHOICES



from django.core.paginator import Paginator
from datetime import date

@login_required
def dashboard(request):
    today = timezone.now().date()

    # Reset attendance, follow-up, and status only once per day
    tracker, created = AttendanceResetTracker.objects.get_or_create(id=1, defaults={'last_reset_date': today})
    if tracker.last_reset_date != today:
        Candidate.objects.update(
            attended=False,
            followed_up=False,
            follow_up_status='',
            follow_up_status_date=None
        )
        FollowUpSession.objects.filter(date=today).delete()
        Attendance.objects.filter(date=today).delete()
        tracker.last_reset_date = today
        tracker.save()

    query = request.GET.get('search', '')
    candidates = Candidate.objects.filter(deleted=False).select_related('assigned_volunteer')

    if query:
        candidates = candidates.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(assigned_volunteer__name__icontains=query)
        )

    # Apply pagination
    paginator = Paginator(candidates, 10)  # Show 10 candidates per page
    page_number = request.GET.get('page')
    candidates_page = paginator.get_page(page_number)

    volunteers = Volunteer.objects.all()

    if request.method == 'POST':
        if 'volunteer_id' in request.POST:
            candidate = get_object_or_404(Candidate, id=request.POST['candidate_id'])
            volunteer = get_object_or_404(Volunteer, id=request.POST['volunteer_id'])
            candidate.assigned_volunteer = volunteer
            candidate.save()
            messages.success(request, f"{candidate.name} assigned to {volunteer.name}.")

        elif 'attendance_candidate_id' in request.POST:
            candidate = get_object_or_404(Candidate, id=request.POST['attendance_candidate_id'])
            Attendance.objects.get_or_create(candidate=candidate, date=today)
            candidate.attended = True
            candidate.save()
            messages.success(request, f"Marked attendance for {candidate.name}.")

        elif 'follow_up_candidate_id' in request.POST:
            candidate = get_object_or_404(Candidate, id=request.POST['follow_up_candidate_id'])
            candidate.followed_up = True
            candidate.save()
            messages.success(request, f"Marked follow-up for {candidate.name}.")

        elif 'follow_up_status_candidate_id' in request.POST:
            candidate = get_object_or_404(Candidate, id=request.POST['follow_up_status_candidate_id'])
            status = request.POST.get('follow_up_status', '').strip()
            date_str = request.POST.get('follow_up_status_date', '')
            try:
                session_date = date.fromisoformat(date_str) if date_str else today
            except ValueError:
                session_date = today
            candidate.follow_up_status = status
            candidate.follow_up_status_date = session_date
            candidate.save()
            Comment.objects.create(
                candidate=candidate,
                volunteer=request.user,
                content=f"Status updated to '{status}' for follow-up on {session_date.strftime('%d %b %Y')}."
            )

            # CandidateComment.objects.create(
            #     candidate=candidate,
            #     comment=f"Status updated to '{status}' for follow-up on {session_date.strftime('%d %b %Y')}."
            # )
            messages.success(request, f"Updated follow-up status for {candidate.name}.")

        elif 'level_candidate_id' in request.POST:
            candidate_id = request.POST.get('level_candidate_id')
            level = request.POST.get('level')
            if candidate_id and level:
                try:
                    candidate = Candidate.objects.get(id=candidate_id)
                    candidate.level = level
                    candidate.save()
                    messages.success(request, f"Level updated for {candidate.name}.")
                except Candidate.DoesNotExist:
                    messages.error(request, "Candidate not found.")

        elif 'delete_candidate_id' in request.POST:
            candidate = get_object_or_404(Candidate, id=request.POST['delete_candidate_id'])
            candidate.deleted = True
            candidate.save()
            messages.warning(request, f"{candidate.name} marked as deleted.")

        return redirect('dashboard')

    context = {
        'candidates': candidates_page,  # use paginated queryset
        'volunteers': volunteers,
        'today': today,
        'follow_up_status_choices': FOLLOW_UP_STATUS_CHOICES,
        'query': query,
    }
    return render(request, 'core/dashboard.html', context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CandidateComment  # Adjust if your model name is different
from collections import defaultdict
from django.utils.timezone import localdate

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CandidateComment
from collections import defaultdict
from django.shortcuts import render
from .models import CandidateComment

# @login_required
# def comments_view(request):
#     comments = CandidateComment.objects.select_related('candidate__assigned_volunteer').order_by('-created_at')

#     grouped_comments = defaultdict(list)
#     for comment in comments:
#         comment_date = comment.created_at.strftime('%d %b %Y')
#         grouped_comments[comment_date].append(comment)

#     return render(request, 'core/comments.html', {'grouped_comments': dict(grouped_comments)})




@login_required
def register_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.registered_by = request.user
            candidate.registration_date = timezone.now().date()
            candidate.save()
            messages.success(request, "Candidate registered successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateForm()
    return render(request, 'core/candidate_register.html', {'form': form})

@login_required
def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate updated successfully.")
            return redirect('candidate_detail', candidate_id=candidate.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'core/edit_candidate.html', {'form': form, 'candidate': candidate})

@login_required
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id, deleted=False)
    return render(request, 'core/candidate_detail.html', {'candidate': candidate})

@login_required
def comment_section(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    comments = Comment.objects.filter(candidate=candidate).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.candidate = candidate
            comment.volunteer = request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('comment_section', candidate_id=candidate_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CommentForm()
    return render(request, 'core/comment_section.html', {'form': form, 'comments': comments, 'candidate': candidate})

@login_required
def compose_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        candidates = Candidate.objects.filter(email__isnull=False).exclude(email='')
        emails = [c.email for c in candidates]

        if not emails:
            messages.error(request, "No candidates with valid email addresses.")
        else:
            send_bulk_email(subject, body, emails)
            for c in candidates:
                EmailLog.objects.create(candidate=c, subject=subject, message=body)
            messages.success(request, f"Email sent to {len(emails)} candidates.")
        return redirect('compose_email')
    return render(request, 'core/compose_email.html')

@login_required
def compose_sms(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        candidates = Candidate.objects.filter(phone__isnull=False).exclude(phone='')
        phone_numbers = [c.phone for c in candidates]
        if not phone_numbers:
            messages.error(request, "No candidates with valid phone numbers.")
        else:
            send_bulk_sms(message, phone_numbers)
            messages.success(request, "SMS sent successfully to all candidates.")
        return redirect('compose_sms')
    return render(request, 'core/compose_sms.html')

from django.shortcuts import render
from collections import defaultdict
from .models import Attendance
from collections import defaultdict
from django.shortcuts import render
from .models import Attendance

def attendance_list(request):
    # Fetch attendance records with candidate info and timestamp
    attendance_records = Attendance.objects.select_related('candidate').order_by('-date', '-timestamp')

    grouped_attendance = defaultdict(list)
    for record in attendance_records:
        # Safe fallback in case timestamp is accidentally null (unlikely with auto_now_add)
        if not hasattr(record, 'timestamp') or record.timestamp is None:
            continue
        grouped_attendance[record.date].append(record)

    context = {
        'grouped_attendance': dict(grouped_attendance),
    }
    return render(request, 'core/attendance_list.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import FollowUpSession, Candidate

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import FollowUpSession, Candidate
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import FollowUpSession, Candidate


from django.views.decorators.http import require_POST


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import Candidate, FollowUpSession



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import Candidate, FollowUpSession

@login_required
def follow_up_report(request):
    today = date.today()
    current_session, _ = FollowUpSession.objects.get_or_create(date=today)

    # ✅ Handle reset historical sessions
    if request.method == 'POST' and request.POST.get('reset_history') == '1':
        FollowUpSession.objects.exclude(date=today).delete()
        messages.success(request, "Historical sessions cleared successfully.")
        return redirect('follow_up_report')

    # ✅ Handle speaker name input
    if request.method == 'POST' and 'speaker_name' in request.POST:
        speaker_name = request.POST.get('speaker_name')
        if speaker_name:
            current_session.speaker_name = speaker_name
            current_session.save()
            # ✅ Refresh session so the updated name reflects in summary
            current_session.refresh_from_db()
            messages.success(request, "Speaker name updated successfully.")
            return redirect('follow_up_report')

    # ✅ Update session candidate groups
    current_session.followed_up.set(Candidate.objects.filter(followed_up=True, updated_at__date=today))
    current_session.attended.set(Candidate.objects.filter(attended=True, updated_at__date=today))
    current_session.new.set(Candidate.objects.filter(registration_date=today))
    current_session.not_attended.set(Candidate.objects.filter(attended=False, updated_at__date=today))

    current_session.refresh_from_db()  # ensure we use latest values

    status_display_count = {
        'Followed Up': current_session.followed_up.count(),
        'Attended': current_session.attended.count(),
        'New': current_session.new.count(),
        'Not Attended': current_session.not_attended.count()
    }

    status_candidate_map = {
        'Followed Up': current_session.followed_up.all(),
        'Attended': current_session.attended.all(),
        'New': current_session.new.all(),
        'Not Attended': current_session.not_attended.all()
    }

    current_session_candidates = {
        'followed_up': current_session.followed_up.all(),
        'attended': current_session.attended.all(),
        'new': current_session.new.all(),
        'not_attended': current_session.not_attended.all()
    }

    sessions = FollowUpSession.objects.exclude(date=today).order_by('-date')
    for session in sessions:
        session.candidate_map = {
            'followed_up': session.followed_up.all(),
            'attended': session.attended.all(),
            'new': session.new.all(),
            'not_attended': session.not_attended.all()
        }

    context = {
        'today': today,
        'status_display_count': status_display_count,
        'status_candidate_map': status_candidate_map,
        'current_session': current_session,
        'current_session_candidates': current_session_candidates,
        'session_labels': [('Followed Up', 'followed_up'), ('Attended', 'attended'), ('New', 'new'), ('Not Attended', 'not_attended')],
        'sessions': sessions,
        'report_keys': ['followed_up', 'attended', 'new', 'not_attended'],
    }

    return render(request, 'core/follow_up_report.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def deleted_candidates(request):
    deleted = Candidate.objects.filter(deleted=True)
    return render(request, 'core/deleted_candidates.html', {'deleted_candidates': deleted})


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Volunteer
from .forms import VolunteerForm

@login_required
def manage_volunteers(request):
    volunteers = Volunteer.objects.all()
    
    if request.method == 'POST' and 'add_volunteer' in request.POST:
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer added successfully!")
            return redirect('manage_volunteers')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VolunteerForm()

    return render(request, 'core/volunteer_management.html', {
        'volunteers': volunteers,
        'form': form,
    })


@login_required
def edit_volunteer(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)

    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer updated successfully.")
            return redirect('manage_volunteers')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VolunteerForm(instance=volunteer)

    return render(request, 'core/edit_volunteer.html', {'form': form, 'volunteer': volunteer})


@login_required
def delete_volunteer(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)

    if request.method == 'POST':
        volunteer.delete()
        messages.success(request, "Volunteer deleted successfully.")
        return redirect('manage_volunteers')

    return render(request, 'core/delete_volunteer_confirm.html', {'volunteer': volunteer})


@login_required
def volunteer_view_candidates(request):
    candidates = Candidate.objects.filter(assigned_volunteer=request.user)
    return render(request, 'core/volunteer_candidates.html', {'candidates': candidates})


@login_required
def volunteer_list(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'core/volunteer_list.html', {'volunteers': volunteers})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect

@require_http_methods(["GET", "POST"])
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    # return render(request, 'core/logout_confirm.html')
    return render(request, 'core/login.html')


class CustomLoginView(LoginView):
    template_name = 'core/login.html'

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def logout_confirm(request):
    return render(request, 'core/logout_confirm.html')
from django.http import JsonResponse

@login_required
def assign_volunteer(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    volunteer_id = request.POST.get('volunteer_id')
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    candidate.assigned_volunteer = volunteer
    candidate.save()
    return JsonResponse({'success': True})

@login_required
def mark_attendance(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.attended = True
    candidate.save()
    return JsonResponse({'success': True})

@login_required
def mark_followup(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.followed_up = True
    candidate.save()
    return JsonResponse({'success': True})

@login_required
def update_status(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.follow_up_status = request.POST.get('follow_up_status')
    candidate.follow_up_status_date = request.POST.get('follow_up_status_date')
    candidate.save()
    return JsonResponse({'success': True})

@login_required
def delete_candidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.deleted = True
    candidate.save()
    return JsonResponse({'success': True})
from django.http import JsonResponse
from .models import Candidate



from datetime import datetime

@login_required
def candidates_by_status(request):
    status = request.GET.get('status')
    date_str = request.GET.get('date')

    candidates = Candidate.objects.filter(follow_up_status=status)

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            candidates = candidates.filter(follow_up_status_date=date_obj)  # Or use updated_at__date if that's what you prefer
        except ValueError:
            pass

    candidates = candidates.select_related('assigned_volunteer')

    data = [{
        'name': c.name,
        'phone': c.phone,
        'email': c.email,
        'volunteer': c.assigned_volunteer.name if c.assigned_volunteer else None
    } for c in candidates]

    return JsonResponse(data, safe=False)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


import openpyxl
from django.http import HttpResponse
from .models import Candidate

def export_candidates_excel(request):
    # Create workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Candidates"

    # Add header row
    headers = [
        'Name', 'Email', 'Phone', 'Registration Date', 'Mother Tongue',
        'Assigned Volunteer', 'Attended', 'Followed-Up', 'Follow-Up Status',
        'Follow-Up Status Date', 'Level'
    ]
    ws.append(headers)

    # Add data rows
    for c in Candidate.objects.all():
        ws.append([
            c.name,
            c.email,
            c.phone,
            c.registration_date.strftime('%Y-%m-%d') if c.registration_date else '',
            c.mother_tongue,
            c.assigned_volunteer.name if c.assigned_volunteer else 'Not Assigned',
            'Yes' if c.attended else 'No',
            'Yes' if c.followed_up else 'No',
            c.get_follow_up_status_display() if c.follow_up_status else '',
            c.follow_up_status_date.strftime('%Y-%m-%d') if c.follow_up_status_date else '',
            c.level
        ])

    # Set HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=foe_candidates.xlsx'
    wb.save(response)

    return response


from collections import defaultdict
from django.shortcuts import render
from .models import Comment

# @login_required
# def comments_view(request):
#     all_comments = Comment.objects.select_related('candidate', 'candidate__assigned_volunteer').order_by('-created_at')

#     grouped_comments = defaultdict(list)
#     status_counts_by_date = defaultdict(lambda: {'Interested': 0, 'Not Interested': 0, 'Follow-up Later': 0, 'Other': 0})

#     for comment in all_comments:
#         date_str = comment.created_at.strftime("%d %b %Y")
#         grouped_comments[date_str].append(comment)

#         status = (comment.candidate.follow_up_status or "").strip()
#         if status in ['Interested', 'Not Interested', 'Follow-up Later']:
#             status_counts_by_date[date_str][status] += 1
#         else:
#             status_counts_by_date[date_str]['Other'] += 1

#     context = {
#         'grouped_comments': dict(grouped_comments),
#         'status_counts': dict(status_counts_by_date),
#     }
#     return render(request, 'core/comments.html', context)


from collections import defaultdict
from django.shortcuts import render
from .models import Comment


from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Comment  # ensure this is imported

@login_required
def comments_view(request):
    all_comments = Comment.objects.select_related('candidate', 'candidate__assigned_volunteer').order_by('-timestamp')

    # Group comments by date
    grouped_comments = defaultdict(list)
    for comment in all_comments:
        comment_date = comment.timestamp.date()
        grouped_comments[comment_date].append(comment)

    return render(request, 'core/comments.html', {
        'grouped_comments': dict(grouped_comments),
    })

# @login_required
# def comments_view(request):
#     all_comments = Comment.objects.select_related('candidate', 'candidate__assigned_volunteer').order_by('-timestamp')

#     # Group by date
#     grouped_comments = defaultdict(list)
#     for comment in all_comments:
#         comment_date = comment.timestamp.date()
#         grouped_comments[comment_date].append(comment)

#     return render(request, 'core/comments.html', {
#         'grouped_comments': dict(grouped_comments),
#     })


