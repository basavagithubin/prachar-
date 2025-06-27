from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Shared choices for follow-up status
FOLLOW_UP_STATUS_CHOICES = [
    ('Coming', 'Coming'),
    ('Out of Station', 'Out of Station'),
    ('Busy', 'Busy'),
    ('Not Feeling Well', 'Not Feeling Well'),
    ('Not Reciving calls', 'Not Reciving calls'),
    ('Not Interested', 'Not Interested'),
    ('Trying to avoide', 'Trying to avoide'),
    ('Other', 'Other'),
]

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Candidate(models.Model):
    LEVEL_CHOICES = [
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
        ('L4', 'L4'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mother_tongue = models.CharField(max_length=100, blank=True, null=True)
    assigned_volunteer = models.ForeignKey('Volunteer', null=True, blank=True, on_delete=models.SET_NULL)

    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="Select the candidate's skill or engagement level (L1–L4)."
    )

    attended = models.BooleanField(default=False)
    followed_up = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    follow_up_status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=FOLLOW_UP_STATUS_CHOICES
    )
    follow_up_status_date = models.DateField(blank=True, null=True)

    registration_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def should_show_followup_status_today(self):
        return self.follow_up_status_date == now().date()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class AttendanceResetTracker(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    last_reset_date = models.DateField()

    def __str__(self):
        return f"Last Reset: {self.last_reset_date}"

    class Meta:
        verbose_name = "Attendance Reset Tracker"

class Comment(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='comments')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.volunteer.username} on {self.candidate.name}"

    class Meta:
        ordering = ['-timestamp']

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Assignment(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.username} → {self.candidate.name}"

    class Meta:
        unique_together = ('volunteer', 'candidate')
        ordering = ['-assigned_at']

class EmailLog(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='email_logs')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.candidate.name} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-sent_at']

class SMSLog(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='sms_logs')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS to {self.candidate.name} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-sent_at']
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent')
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # ✅ New field to track time of marking attendance
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.candidate.name} - {self.date} - {self.status}"

    class Meta:
        unique_together = ('candidate', 'date')
        ordering = ['-date', '-timestamp']  # ✅ Sort by both date and time


class FollowUpSession(models.Model):
    date = models.DateField()
    speaker_name = models.CharField(max_length=255, blank=True, null=True)
    followed_up = models.ManyToManyField(Candidate, related_name='followed_up_sessions', blank=True)
    attended = models.ManyToManyField(Candidate, related_name='attended_sessions', blank=True)
    new = models.ManyToManyField(Candidate, related_name='new_sessions', blank=True)
    not_attended = models.ManyToManyField(Candidate, related_name='not_attended_sessions', blank=True)

    def __str__(self):
        return f"Follow-up Session - {self.date}"
    
class CandidateComment(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment for {self.candidate.name}"

