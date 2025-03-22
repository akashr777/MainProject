from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class login_model(models.Model):
    username=models.CharField(max_length=100,null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    type=models.CharField(max_length=100,null=True,blank=True)


class user_table(models.Model):
    LOGINID = models.ForeignKey(login_model, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    profileimage=models.FileField(upload_to='profileimage/',null=True,blank=True)


from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class employee_table(models.Model):
    LOGINID = models.ForeignKey("login_model", on_delete=models.CASCADE, null=True, blank=True)  
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.BigIntegerField(null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)  
    availability_status = models.BooleanField(default=True)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)  
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)  
    date_of_joining = models.DateField(null=True, blank=True)
    profileimage = models.FileField(upload_to='profileimage/', null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.role.name if self.role else 'No Role'} ({self.department.name if self.department else 'No Department'})"





class campaign_request(models.Model):

    user = models.ForeignKey(login_model, on_delete=models.CASCADE, null=True, blank=True)
    CLIENT = models.ForeignKey(user_table, on_delete=models.CASCADE, null=True, blank=True)
    
    campaign_name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    primary_color = models.CharField(max_length=7, null=True, blank=True)  
    font_style = models.CharField(
        max_length=50, null=True, blank=True
      
    )
    theme = models.CharField(
        max_length=50, null=True, blank=True
      
    )
    additional_text = models.TextField(blank=True, null=True)
    campaign_text = models.TextField(blank=True, null=True)

    creative_requirements = models.CharField(max_length=400, null=True, blank=True) 
    ad_effects = models.CharField(max_length=400, null=True, blank=True)   
    ad_placement = models.CharField(max_length=400, null=True, blank=True)   
    
    estimated_budget = models.CharField(max_length=100, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True) 



class CampaignFile(models.Model):
    campaign = models.ForeignKey(campaign_request, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='clientreqfile/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class notification_table(models.Model):
    CLIENT = models.ForeignKey(user_table, on_delete=models.CASCADE, null=True, blank=True)
    not_date=models.DateField(auto_now=True, null=True, blank=True)
    description=models.CharField(max_length=100, null=True, blank=True)
    STATUS_CHOICES = [
        ("unread", "Unread"),
        ("read", "Read"),
    ]
    status=models.CharField(max_length=20 , null=True, blank=True,default="unread")
    
    
    def __str__(self):
        return f"Notification for {self.CLIENT} - {self.status}"

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
         ('Review', 'Review'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255,null=True,blank=True)

    campaign = models.ForeignKey(campaign_request, on_delete=models.CASCADE,related_name="tasks")
    assigned_to = models.ForeignKey(employee_table, on_delete=models.CASCADE,related_name="tasks")
    task_description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    created_at = models.DateTimeField(auto_now_add=True)
    creative_file = models.FileField(upload_to="creatives/", null=True, blank=True)  # Employee Uploads Creative
    reviewed_by_cd = models.BooleanField(default=False)  # Creative Director Approval
    feedback = models.TextField(blank=True, null=True)  # Feedback if rejected

    def __str__(self):
        return f"Task for {self.assigned_to.full_name} ({self.status})"


from django.db import models
from django.contrib.auth.models import User  # Assuming user authentication
from .models import Task,employee_table

class CreativeUpload(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="creatives")
    file = models.FileField(upload_to="creatives/")
    uploaded_by = models.ForeignKey(employee_table, on_delete=models.CASCADE,null=True,blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.task.title} - {self.uploaded_by.full_name}"



class FinalCreative(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="final_creatives")
    file = models.FileField(upload_to="final_creatives/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(employee_table, on_delete=models.SET_NULL, null=True,blank=True)
    sent_to_client = models.BooleanField(default=False)
    approved_by_client = models.BooleanField(default=False)  # New Field
    rejection_reason = models.TextField(blank=True, null=True)  # Stores rejection reason

    def __str__(self):
        return f"Final Creative for {self.task.title} - {self.reviewed_by.username if self.reviewed_by else 'Unknown'}"

    def send_to_client(self):
        """Mark this final creative as sent."""
        self.sent_to_client = True
        self.save()
        self.task.status = "Completed"
        self.task.save()

    def reject_by_client(self, reason):
        """Handle client rejection."""
        self.approved_by_client = False
        self.rejection_reason = reason
        self.sent_to_client = False  # Reset to allow resubmission
        self.save()

        # Change task status back to review for revision
        self.task.status = "Review"
        self.task.save()



class CreativeFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="creative_files")
    file = models.FileField(upload_to="creatives/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class TaskReview(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="review")
    reviewed_by = models.ForeignKey("employee_table", on_delete=models.CASCADE, related_name="reviews")
    feedback = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now=True)



# class Task(models.Model):
#     PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
#     STATUS_CHOICES = [('To-Do', 'To-Do'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]

#     campaign = models.ForeignKey(campaign_request, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  
#     assigned_to = models.ManyToManyField(employee_table, related_name="tasks", null=True, blank=True) 
#     task_name = models.CharField(max_length=255, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='To-Do')
#     deadline = models.DateField(null=True, blank=True)
#     progress = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

#     def __str__(self):
#         return f"{self.task_name} - {self.assigned_to.full_name} ({self.department.name})"




# class TaskComment(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
#     employee = models.ForeignKey(employee_table, on_delete=models.CASCADE)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds timestamp

#     def __str__(self):
#         return f"{self.user.username} - {self.task.task_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"





# class AdCreative(models.Model):
#     CREATIVE_TYPE_CHOICES = [
#         ('Text', 'Text'),
#         ('Image', 'Image'),
#         ('Video', 'Video'),
#     ]
    
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('In Review', 'In Review'),
#         ('Finalized', 'Finalized'),
#         ('Submitted', 'Submitted'),
#         ('Approved', 'Approved'),
#         ('Rejected', 'Rejected'),
#     ]
#     tasks=models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
#     campaign = models.ForeignKey(campaign_request, on_delete=models.CASCADE, related_name="creatives" ,blank=True, null=True)
#     employee = models.ForeignKey(employee_table, on_delete=models.CASCADE, blank=True, null=True)
#     creative_type = models.CharField(max_length=10, choices=CREATIVE_TYPE_CHOICES, blank=True, null=True)
#     file = models.FileField(upload_to="ad_creatives/", blank=True, null=True)
#     text_content = models.TextField(blank=True, null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     approval_date = models.DateTimeField(blank=True, null=True)  # Date when it was approved/rejected
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Track creative status
#     is_final_submission = models.BooleanField(default=False)  # Flag to indicate if the creative is ready for client submission
    





# class FinalAdCreative(models.Model):
#     campaign = models.ForeignKey(campaign_request, on_delete=models.CASCADE, related_name="final_creative")
#     file = models.FileField(upload_to="final_ad_creatives/", blank=True, null=True)
#     text_content = models.TextField(blank=True, null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(
#         max_length=20, choices=[
#             ('Pending', 'Pending'),
#             ('Submitted', 'Submitted'),
#             ('Approved', 'Approved'),
#             ('Rejected', 'Rejected'),
#         ], default='Pending'
#     )




# class FinalAdSubmission(models.Model):
#     ad_creative = models.ForeignKey('AdCreative', on_delete=models.CASCADE)
#     submitted_by = models.ForeignKey('employee_table', on_delete=models.CASCADE)
#     client = models.ForeignKey('user_table', on_delete=models.CASCADE)
#     submission_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])


# class AdProject(models.Model):
#     CLIENT = models.ForeignKey(user_table, on_delete=models.CASCADE, null=True, blank=True)
#     title = models.CharField(max_length=255,null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     completed = models.BooleanField(default=False, null=True, blank=True)



# from django.db import models

# class AdSpace(models.Model):
#     """Defines available ad spaces on the customized browser"""
#     POSITION_CHOICES = [
#         ('header', 'Header Banner'),
#         ('sidebar', 'Sidebar Ad'),
#         ('footer', 'Footer Banner'),
#         ('popup', 'Popup Ad'),
#     ]

#     name = models.CharField(max_length=255, unique=True)
#     position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='header')
#     width = models.IntegerField(help_text="Width in pixels")
#     height = models.IntegerField(help_text="Height in pixels")
#     is_available = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.name} ({self.position})"

# class TimeSlot(models.Model):
#     """Stores available time slots for running ads"""
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     is_booked = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.start_time} - {self.end_time}"

# class AdAssignment(models.Model):
#     ad_creative = models.ForeignKey(FinalAdCreative, on_delete=models.CASCADE)
#     ad_space = models.ForeignKey(AdSpace, on_delete=models.CASCADE)
#     time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
#     assigned_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.ad_creative} -> {self.ad_space} @ {self.time_slot}"



# from django.db import models
# from django.contrib.auth.models import User

# class Campaign(models.Model):
#     STATUS_CHOICES = [
#         ('pending_budget', 'Pending Budget Approval'),
#         ('approved', 'Approved'),
#         ('running', 'Running'),
#         ('completed', 'Completed'),
#         ('rejected', 'Rejected'),
#     ]

#     client = models.ForeignKey(user_table, on_delete=models.CASCADE, related_name="campaigns")
#     campaign_request = models.OneToOneField(campaign_request, on_delete=models.CASCADE)  # Link to the request
#     campaign_name = models.CharField(max_length=255)
#     budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_budget')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.campaign_name
