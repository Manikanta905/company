import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import JobListing, TeamMember
from .forms import JobApplicationForm, ContactForm

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper — send email notification for a new job application
# ---------------------------------------------------------------------------
def _send_application_email(application):
    """
    Sends a full-detail notification email to mktechsolution2026@gmail.com
    every time a candidate submits a job application.
    Includes every field: job info, applicant info, cover letter,
    job description, responsibilities, requirements, salary, deadline, timestamps.
    """
    job     = application.job
    subject = f"[New Application #{application.pk}] {job.title} — {application.full_name}"

    # ------------------------------------------------------------------
    # Plain-text fallback — contains ALL data
    # ------------------------------------------------------------------
    separator = "=" * 60
    text_body = f"""
{separator}
  MK TECH SOLUTIONS — NEW JOB APPLICATION RECEIVED
  Application #{application.pk}
{separator}

QUICK SUMMARY
  {application.full_name} applied for: {job.title}
  Submitted: {application.applied_on.strftime("%A, %B %d, %Y at %I:%M %p")} UTC

{separator}
  SECTION 1 — POSITION DETAILS
{separator}
  Job Title     : {job.title}
  Department    : {job.department}
  Location      : {job.location}
  Job Type      : {job.get_job_type_display()}
  Salary Range  : {job.salary_range if job.salary_range else 'Not specified'}
  Posted On     : {job.posted_on.strftime("%B %d, %Y")}
  Deadline      : {job.deadline.strftime("%B %d, %Y") if job.deadline else 'No deadline set'}
  Status        : {'Active' if job.is_active else 'Closed'}

{separator}
  SECTION 2 — APPLICANT DETAILS
{separator}
  Full Name     : {application.full_name}
  Email Address : {application.email}
  Phone Number  : {application.phone}
  Resume / CV   : {application.resume_link if application.resume_link else 'Not provided'}
  Applied On    : {application.applied_on.strftime("%A, %B %d, %Y at %I:%M %p")} UTC

{separator}
  SECTION 3 — COVER LETTER
{separator}
{application.cover_letter}

{separator}
  SECTION 4 — FULL JOB DESCRIPTION
{separator}
{job.description}

{separator}
  SECTION 5 — RESPONSIBILITIES
{separator}
{job.responsibilities if job.responsibilities else 'Not specified'}

{separator}
  SECTION 6 — REQUIREMENTS
{separator}
{job.requirements}

{separator}
  SECTION 7 — SUBMISSION INFO
{separator}
  Application ID : #{application.pk}
  Submitted      : {application.applied_on.strftime("%A, %B %d, %Y at %I:%M %p")} UTC
  Source         : MK Tech Solutions Careers Portal
  Notify Email   : mktechsolution2026@gmail.com

Admin Panel:
  http://127.0.0.1:8000/admin/website/jobapplication/{application.pk}/change/

{separator}
Reply to this email to contact {application.full_name} directly at {application.email}.
{separator}
"""

    # ------------------------------------------------------------------
    # HTML body — fully styled, contains ALL data
    # ------------------------------------------------------------------
    html_body = render_to_string('emails/application_notification.html', {
        'application': application,
        'job': job,
    })

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.COMPANY_EMAIL],          # mktechsolution2026@gmail.com
        reply_to=[application.email],          # reply goes straight to applicant
    )
    msg.attach_alternative(html_body, 'text/html')

    try:
        msg.send(fail_silently=False)
        logger.info(
            "Application email sent to %s for applicant %s (Job: %s)",
            settings.COMPANY_EMAIL, application.full_name, application.job.title
        )
    except Exception as e:
        # Logs to console/server — won't crash the user's form submission
        logger.error(
            "FAILED to send application email to %s — %s: %s",
            settings.COMPANY_EMAIL, type(e).__name__, e
        )


# ---------------------------------------------------------------------------
# Helper — send email notification for a contact form message
# ---------------------------------------------------------------------------
def _send_contact_email(contact_msg):
    subject = f"New Contact Message: {contact_msg.subject}"

    text_body = (
        f"New contact form submission on MK Tech Solutions website.\n\n"
        f"Name    : {contact_msg.name}\n"
        f"Email   : {contact_msg.email}\n"
        f"Subject : {contact_msg.subject}\n\n"
        f"--- Message ---\n"
        f"{contact_msg.message}\n\n"
        f"Reply directly to the sender: {contact_msg.email}\n"
    )

    html_body = render_to_string('emails/contact_notification.html', {
        'msg': contact_msg,
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.COMPANY_EMAIL],
        reply_to=[contact_msg.email],
    )
    email.attach_alternative(html_body, 'text/html')

    try:
        email.send(fail_silently=False)
        logger.info(
            "Contact email sent to %s from %s",
            settings.COMPANY_EMAIL, contact_msg.email
        )
    except Exception as e:
        logger.error(
            "FAILED to send contact email to %s — %s: %s",
            settings.COMPANY_EMAIL, type(e).__name__, e
        )


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def home(request):
    active_jobs = JobListing.objects.filter(is_active=True)[:3]
    return render(request, 'website/home.html', {
        'active_jobs': active_jobs,
        'page': 'home',
    })


def about(request):
    team_members = TeamMember.objects.all()
    return render(request, 'website/about.html', {
        'team_members': team_members,
        'page': 'about',
    })


def jobs(request):
    department      = request.GET.get('department', '')
    job_type        = request.GET.get('job_type', '')
    all_jobs        = JobListing.objects.filter(is_active=True)

    if department:
        all_jobs = all_jobs.filter(department__icontains=department)
    if job_type:
        all_jobs = all_jobs.filter(job_type=job_type)

    departments = (
        JobListing.objects
        .filter(is_active=True)
        .values_list('department', flat=True)
        .distinct()
    )

    return render(request, 'website/jobs.html', {
        'jobs': all_jobs,
        'departments': departments,
        'job_type_choices': JobListing.JOB_TYPE_CHOICES,
        'selected_department': department,
        'selected_job_type': job_type,
        'page': 'jobs',
    })


def job_detail(request, pk):
    job = get_object_or_404(JobListing, pk=pk, is_active=True)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application      = form.save(commit=False)
            application.job  = job
            application.save()

            # Fire email to company inbox
            _send_application_email(application)

            # Redirect to dedicated success page
            return redirect('application_success')
    else:
        form = JobApplicationForm()

    return render(request, 'website/job_detail.html', {
        'job': job,
        'form': form,
        'page': 'jobs',
    })


def application_success(request):
    """Dedicated thank-you page shown after a job application is submitted."""
    return render(request, 'website/application_success.html', {'page': 'jobs'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()

            # Fire email to company inbox
            _send_contact_email(contact_msg)

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'website/contact.html', {
        'form': form,
        'page': 'contact',
    })


def contact_success(request):
    """Dedicated thank-you page shown after a contact form is submitted."""
    return render(request, 'website/contact_success.html', {'page': 'contact'})
