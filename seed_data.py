"""
Run with:  py manage.py shell < seed_data.py
Seeds sample job listings and a superuser (admin / admin1234)
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mktechsolutions.settings')
django.setup()

from django.contrib.auth import get_user_model
from website.models import JobListing, TeamMember

User = get_user_model()

# ---- Superuser ----
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mktechsolutions.com', 'admin1234')
    print("Superuser created  →  username: admin  /  password: admin1234")
else:
    print("Superuser already exists.")

# ---- Job Listings ----
jobs = [
    {
        'title': 'Full-Stack Django Developer',
        'department': 'Engineering',
        'location': 'Remote / Tech City, TX',
        'job_type': 'full_time',
        'salary_range': '$80,000 – $110,000',
        'description': (
            'We are looking for an experienced Full-Stack Developer who is '
            'comfortable with both Python/Django on the backend and modern '
            'JavaScript frameworks on the frontend. You will be responsible '
            'for building and maintaining high-quality web applications for '
            'our clients across various industries.'
        ),
        'requirements': (
            '• 3+ years of experience with Django and Python\n'
            '• Proficiency in JavaScript (React or Vue preferred)\n'
            '• Experience with PostgreSQL or similar relational databases\n'
            '• Familiarity with Docker and CI/CD pipelines\n'
            '• Strong understanding of REST API design\n'
            '• Excellent written and verbal communication skills'
        ),
        'responsibilities': (
            '• Design and implement new features end-to-end\n'
            '• Write clean, well-tested, and documented code\n'
            '• Collaborate with product managers and designers\n'
            '• Participate in code reviews and mentor junior developers\n'
            '• Contribute to architectural decisions'
        ),
    },
    {
        'title': 'Cloud Infrastructure Engineer',
        'department': 'Cloud & DevOps',
        'location': 'Tech City, TX (Hybrid)',
        'job_type': 'full_time',
        'salary_range': '$90,000 – $130,000',
        'description': (
            'Join our Cloud team to design, build, and manage scalable cloud '
            'infrastructure on AWS. You will work closely with engineering '
            'teams to automate deployments, optimise costs, and ensure the '
            'reliability and security of our client environments.'
        ),
        'requirements': (
            '• 4+ years of cloud infrastructure experience (AWS preferred)\n'
            '• Strong skills in Terraform or CloudFormation\n'
            '• Kubernetes / EKS experience\n'
            '• Proficiency with Linux and shell scripting\n'
            '• AWS certifications (Solutions Architect or DevOps Engineer) a plus'
        ),
        'responsibilities': (
            '• Design and maintain cloud architecture\n'
            '• Build automated deployment pipelines (CI/CD)\n'
            '• Monitor and respond to infrastructure incidents\n'
            '• Implement cost-optimisation strategies\n'
            '• Document infrastructure standards and procedures'
        ),
    },
    {
        'title': 'UI/UX Designer',
        'department': 'Design',
        'location': 'Remote',
        'job_type': 'full_time',
        'salary_range': '$65,000 – $90,000',
        'description': (
            'We are hiring a creative UI/UX Designer to craft beautiful, '
            'user-centred digital experiences. You will work alongside '
            'product and engineering teams to take products from concept to '
            'polished, accessible interfaces.'
        ),
        'requirements': (
            '• 2+ years of UI/UX design experience\n'
            '• Portfolio demonstrating strong design thinking\n'
            '• Proficiency in Figma (or similar)\n'
            '• Understanding of accessibility standards (WCAG 2.1)\n'
            '• Ability to translate user research into design decisions'
        ),
        'responsibilities': (
            '• Create wireframes, prototypes, and high-fidelity designs\n'
            '• Conduct usability testing and incorporate feedback\n'
            '• Collaborate closely with frontend developers\n'
            '• Maintain and evolve our design system\n'
            '• Ensure all designs meet accessibility guidelines'
        ),
    },
    {
        'title': 'Junior Software Engineer (Internship)',
        'department': 'Engineering',
        'location': 'Tech City, TX',
        'job_type': 'internship',
        'salary_range': '$20 – $25 / hour',
        'description': (
            'Kick-start your software engineering career with a hands-on '
            'internship at MK Tech Solutions. You will be embedded in a '
            'real project team and contribute to features that go to '
            'production, all while being mentored by senior engineers.'
        ),
        'requirements': (
            '• Currently pursuing a degree in Computer Science or related field\n'
            '• Familiarity with Python or JavaScript\n'
            '• Basic understanding of version control (Git)\n'
            '• Eagerness to learn and a proactive attitude'
        ),
        'responsibilities': (
            '• Work on assigned features under senior engineer guidance\n'
            '• Participate in daily stand-ups and sprint planning\n'
            '• Write and maintain unit tests\n'
            '• Document your work clearly'
        ),
    },
    {
        'title': 'Cybersecurity Analyst',
        'department': 'Security',
        'location': 'Remote',
        'job_type': 'full_time',
        'salary_range': '$85,000 – $115,000',
        'description': (
            'Protect our clients and internal systems from evolving threats. '
            'As a Cybersecurity Analyst you will perform security assessments, '
            'respond to incidents, and help build a stronger security culture '
            'across the organisation.'
        ),
        'requirements': (
            '• 3+ years of experience in cybersecurity or information security\n'
            '• Knowledge of OWASP Top 10 and common attack vectors\n'
            '• Experience with SIEM tools (Splunk, ELK, etc.)\n'
            '• Security certifications (CEH, CISSP, CompTIA Security+) preferred\n'
            '• Strong analytical and problem-solving skills'
        ),
        'responsibilities': (
            '• Conduct regular security audits and vulnerability assessments\n'
            '• Monitor security alerts and respond to incidents\n'
            '• Develop and maintain security policies and procedures\n'
            '• Provide security training to staff\n'
            '• Stay current with threat intelligence'
        ),
    },
]

created = 0
for job_data in jobs:
    obj, made = JobListing.objects.get_or_create(title=job_data['title'], defaults=job_data)
    if made:
        created += 1

print(f"{created} job listing(s) created ({len(jobs) - created} already existed).")

# ---- Team Members ----
team = [
    {'name': 'Marcus Kim', 'role': 'CEO & Co-Founder', 'order': 1,
     'bio': 'Marcus leads MK Tech Solutions with 15+ years of enterprise software experience.'},
    {'name': 'Aisha Patel', 'role': 'CTO & Co-Founder', 'order': 2,
     'bio': 'Aisha architects the technical vision and oversees our engineering teams.'},
    {'name': 'Jordan Rivera', 'role': 'Head of Engineering', 'order': 3,
     'bio': 'Jordan keeps our dev teams running smoothly and shipping quality code.'},
    {'name': 'Priya Singh', 'role': 'Head of Design', 'order': 4,
     'bio': 'Priya drives user experience excellence across all our client products.'},
]

t_created = 0
for member in team:
    obj, made = TeamMember.objects.get_or_create(name=member['name'], defaults=member)
    if made:
        t_created += 1

print(f"{t_created} team member(s) created.")
print("\n✅ Seed complete! Run the server with:  py manage.py runserver")
