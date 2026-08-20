"""
Quick email test — run this ONCE to confirm Gmail is working:
    py test_email.py

If it prints "Email sent successfully!" then job applications
will automatically land in mktechsolution2026@gmail.com.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mktechsolutions.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print(f"\n Sending test email to: {settings.COMPANY_EMAIL}")
print(f" Using Gmail account : {settings.EMAIL_HOST_USER}")
print(f" App Password set    : {'YES — looks good' if settings.EMAIL_HOST_PASSWORD != 'your_16char_app_password_here' else 'NO — still placeholder! See instructions below.'}\n")

if settings.EMAIL_HOST_PASSWORD == 'your_16char_app_password_here':
    print("=" * 60)
    print("  ACTION REQUIRED — Gmail App Password not set yet!")
    print("=" * 60)
    print("""
  Follow these 3 steps:

  STEP 1 — Open this URL in your browser:
    https://myaccount.google.com/security
    → Make sure '2-Step Verification' is ON
      for mktechsolution2026@gmail.com

  STEP 2 — Open this URL:
    https://myaccount.google.com/apppasswords
    → Click 'Select app'  → choose 'Mail'
    → Click 'Select device' → choose 'Other'
    → Type 'Django' → click GENERATE
    → Copy the 16-character password shown

  STEP 3 — Open this file:
    mktechsolutions/mktechsolutions/settings.py

    Find this line:
      EMAIL_HOST_PASSWORD = 'your_16char_app_password_here'

    Replace it with your copied password, e.g.:
      EMAIL_HOST_PASSWORD = 'abcdwxyzefghijkl'

  Then run this script again:
    py test_email.py
""")
else:
    try:
        send_mail(
            subject='✅ MK Tech Solutions — Email Test',
            message=(
                'This is a test email from your MK Tech Solutions Django website.\n\n'
                'If you received this, your Gmail SMTP is working correctly.\n'
                'Job application emails will now be delivered to this inbox.\n\n'
                '— MK Tech Solutions System'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.COMPANY_EMAIL],
            fail_silently=False,
        )
        print("=" * 60)
        print("  Email sent successfully!")
        print("=" * 60)
        print(f"\n  Check your inbox at: {settings.COMPANY_EMAIL}")
        print("  Subject: ✅ MK Tech Solutions — Email Test\n")
        print("  Gmail SMTP is working. Every job application")
        print("  will now automatically send to this inbox.\n")

    except Exception as e:
        print("=" * 60)
        print("  Email FAILED to send!")
        print("=" * 60)
        print(f"\n  Error type : {type(e).__name__}")
        print(f"  Error      : {e}\n")
        print("  Common fixes:")
        print("  - Make sure 2-Step Verification is ON for your Gmail account")
        print("  - Make sure you used an APP PASSWORD, not your Gmail login password")
        print("  - Double-check you copied all 16 characters without spaces\n")
