from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import JobListing, JobApplication, ContactMessage, TeamMember

# -----------------------------------------------------------------------
# Site header branding
# -----------------------------------------------------------------------
admin.site.site_header  = "MK Tech Solutions — Admin"
admin.site.site_title   = "MK Tech Solutions"
admin.site.index_title  = "Website Management"


# -----------------------------------------------------------------------
# Job Listing — inline applications preview
# -----------------------------------------------------------------------
class JobApplicationInline(admin.TabularInline):
    model       = JobApplication
    extra       = 0
    readonly_fields = ('full_name', 'email', 'phone', 'resume_link', 'applied_on')
    fields      = ('full_name', 'email', 'phone', 'resume_link', 'applied_on')
    can_delete  = False
    show_change_link = True
    verbose_name_plural = "Applications received for this job"


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    # --- List view ---
    list_display  = (
        'title', 'department', 'location', 'job_type_badge',
        'salary_range', 'application_count', 'is_active', 'posted_on', 'deadline',
    )
    list_filter   = ('is_active', 'job_type', 'department')
    search_fields = ('title', 'department', 'description', 'location')
    list_editable = ('is_active',)
    date_hierarchy = 'posted_on'
    ordering      = ('-posted_on',)

    # --- Detail view ---
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'location', 'job_type', 'salary_range', 'is_active'),
        }),
        ('Job Details', {
            'fields': ('description', 'responsibilities', 'requirements'),
            'classes': ('wide',),
        }),
        ('Dates', {
            'fields': ('deadline',),
        }),
    )
    inlines   = [JobApplicationInline]

    # --- Custom columns ---
    @admin.display(description='Type')
    def job_type_badge(self, obj):
        colours = {
            'full_time':  ('#2563eb', '#eff6ff'),
            'part_time':  ('#7c3aed', '#f5f3ff'),
            'contract':   ('#c2410c', '#fff7ed'),
            'internship': ('#ca8a04', '#fefce8'),
            'remote':     ('#059669', '#ecfdf5'),
        }
        fg, bg = colours.get(obj.job_type, ('#1e293b', '#f1f5f9'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:50px;font-size:11px;font-weight:700;">{}</span>',
            bg, fg, obj.get_job_type_display(),
        )

    @admin.display(description='Applications')
    def application_count(self, obj):
        count = obj.applications.count()
        if count == 0:
            return format_html('<span style="color:#94a3b8;">0</span>')
        url = (
            reverse('admin:website_jobapplication_changelist')
            + f'?job__id__exact={obj.pk}'
        )
        return format_html(
            '<a href="{}" style="font-weight:700;color:#2563eb;">{} ✉</a>',
            url, count,
        )


# -----------------------------------------------------------------------
# Job Application
# -----------------------------------------------------------------------
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'email', 'phone', 'job_link', 'resume_btn', 'applied_on')
    list_filter   = ('job', 'job__department')
    search_fields = ('full_name', 'email', 'job__title')
    readonly_fields = ('applied_on',)
    ordering      = ('-applied_on',)

    fieldsets = (
        ('Applicant', {
            'fields': ('full_name', 'email', 'phone', 'resume_link'),
        }),
        ('Application', {
            'fields': ('job', 'cover_letter', 'applied_on'),
        }),
    )

    @admin.display(description='Job')
    def job_link(self, obj):
        url = reverse('admin:website_joblisting_change', args=[obj.job.pk])
        return format_html('<a href="{}">{}</a>', url, obj.job.title)

    @admin.display(description='Resume')
    def resume_btn(self, obj):
        if obj.resume_link:
            return format_html(
                '<a href="{}" target="_blank" '
                'style="background:#2563eb;color:#fff;padding:3px 10px;'
                'border-radius:6px;font-size:11px;font-weight:700;'
                'text-decoration:none;">View →</a>',
                obj.resume_link,
            )
        return format_html('<span style="color:#94a3b8;">—</span>')


# -----------------------------------------------------------------------
# Contact Message
# -----------------------------------------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'sent_on', 'read_status')
    list_filter   = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'sent_on')
    ordering      = ('-sent_on',)

    fieldsets = (
        ('Sender', {
            'fields': ('name', 'email'),
        }),
        ('Message', {
            'fields': ('subject', 'message', 'sent_on'),
        }),
        ('Status', {
            'fields': ('is_read',),
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    @admin.display(description='Status')
    def read_status(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="color:#059669;font-weight:700;">✔ Read</span>'
            )
        return format_html(
            '<span style="color:#dc2626;font-weight:700;">● Unread</span>'
        )

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected messages as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


# -----------------------------------------------------------------------
# Team Member
# -----------------------------------------------------------------------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'order', 'has_photo')
    list_editable = ('order',)
    search_fields = ('name', 'role')

    @admin.display(description='Photo', boolean=True)
    def has_photo(self, obj):
        return bool(obj.photo)
