from datetime import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views import View

from administrator.forms import CampaignRequestForm
# from administrator.models import login_model, user_table,campaign_request,employee_table,notification_table,Task,AdCreative,AdProject,FinalAdSubmission,
from administrator.models import login_model, user_table,campaign_request,employee_table,notification_table,CampaignFile,Department


class homepage(View):
    def get(self,request):
        return render(request,"Client/index.html")

class adminhome(View):
    def get(self,request):
        client_count=user_table.objects.count()
        emp_count=employee_table.objects.count()
        active_campaign=campaign_request.objects.filter(status="accepted").count()
        return render(request,"Administrators/base.html",{'client_count':client_count,'emp_count':emp_count,'active_campaign':active_campaign})

class clienthome(View):
    def get(self,request):
        client_name = request.session.get('client_name', 'Client')
        notification = notification_table.objects.filter(CLIENT__LOGINID__id=request.session.get('userid'))
        return render(request,"Client/Client_home.html",{'client_name':client_name,'notification':notification})
    
def get_notifications(request):
    notifications = notification_table.objects.filter(CLIENT__LOGINID__id=request.session['userid'], status='unread')
    print(notifications)
    return JsonResponse({"count": notifications.count(), "notifications": list(notifications.values("description"))})

@csrf_exempt
def mark_notifications_as_read(request):
    """ Mark all notifications as read for the logged-in user """
    if request.method == "POST":
        notification_table.objects.filter(CLIENT__LOGINID__id=request.session.get('userid'), status="unread").update(status="read")
        return JsonResponse({"status": "success"})

from django.shortcuts import render, redirect
from django.views import View
from django.utils.timezone import now
from .models import  login_model, employee_table
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from .models import login_model, employee_table, Task  # Import Task model
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from .models import login_model, employee_table, Task
class emphome(View):
    def get(self, request):
        if 'userid' not in request.session:  # Check if user is logged in
            return redirect('login')

        try:
            user = login_model.objects.get(id=request.session['userid'])  
            employee = employee_table.objects.get(LOGINID=user)  # Get employee record
            
            # Get the Creative Director role ID (hardcoded or from database)
            creative_director_role = Role.objects.get(name="Creative Director")
            your_creative_director_role_id = creative_director_role.id

            # Pass the ID to the template
            employee_name = employee.full_name
            employee_image = employee.profileimage.url if employee.profileimage else "/static/images/default-avatar.png"  
            tasks = Task.objects.filter(assigned_to=employee)
            pending_count = tasks.filter(status="To-Do").count()
            completed_count = tasks.filter(status="Completed").count()

            employee_role_id = employee.role.id if employee.role else None  
            print(f"Employee Role ID: {employee_role_id}")  # Debug print to confirm

        except employee_table.DoesNotExist:
            employee_name = "Employee Not Found"  
            employee_image = "/static/images/default-avatar.png"
            tasks = []  
            pending_count = completed_count = overdue_count = 0
            employee_role_id = None  
            your_creative_director_role_id = None  # Default for non-Creative Director

        return render(request, 'Employees/Emp_sidebar.html', {
            'employee_name': employee_name,
            'employee_image': employee_image,
            'tasks': tasks,  
            'pending_count': pending_count,  
            'completed_count': completed_count,  
            'employee_role_id': employee_role_id,  
            'your_creative_director_role_id': your_creative_director_role_id,  # Pass the value
        })



class about(View):
    def get(self,request):
        return render(request,"Client/about.html")
    

class mng_client(View):
    def get(self,request):
        a=user_table.objects.all()
        return render(request,"Administrators/Manage_client.html",{'a':a})
    
class delete_client(View):
    def get(self,request,id):
        a=user_table.objects.get(id=id).delete()
        return redirect('mng_client')


class registration(View):
    def get(self,request):
        return render(request,"Home/registration.html")

    def post(self, request):
        # Handle form submission
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company')
        password = request.POST.get('password')
        profileimage=request.FILES['image']

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "registration")
        # Create a user in the Usertable

        user = login_model.objects.create(
            username=email,
            password=password,  # Hash the password
            type='client',
        )

        client = user_table.objects.create(
            first_name=firstname,
            last_name=lastname,
            phone=phone,
            company_name=company_name,
            email=email,
            profileimage=profileimage,
            LOGINID=user
        )


        messages.success(request, 'Registration successful!')
        return redirect('login')  # Replace with the appropriate success page URL
    
           

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import login_model  # Ensure this is the correct import for your model

class login(View):
    def get(self, request):
        return render(request, "Home/login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username exists
        try:
            user = login_model.objects.get(username=username)
            
            # Check if the password matches
            if user.password == password:
                request.session['userid'] = user.id
                
                if user.type == 'admin':
                    return redirect('adminhome')
                elif user.type == 'client':
                    return redirect('clienthome')
                elif user.type == 'employee':
                    return redirect('emphome')
                else:
                    return render(request, 'Home/login.html',{'message':'Inavlid username or password'})
            else:
                    return render(request, 'Home/login.html',{'message':'Inavlid username or password'})
        
        except login_model.DoesNotExist:
                return render(request, 'Home/login.html',{'message':'Inavlid username or password'})



from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View


class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'Client/forgot_password.html')

    def post(self, request, *args, **kwargs):
            email = request.POST['email']
            try:
                user = login_model.objects.get(username=email)
                  # Fetch user based on email
                print(user)
                user_password = user.password  # Get the password hash (you won't send plain password)
                
                # You should ideally send a password reset link instead of the plain password
                subject = "Password Reset"
                message = f"Your password is: {user_password}"  # This is just an example; sending the plain password is not recommended
                from_email = "akashrpayyoli02@gmail.com"
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Your password has been sent to your email.")

                return redirect('login')  # Redirect to the login page

            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
            return render(request, 'Client/forgot_password.html')




class profile(View):
    def get(self,request):
        users=user_table.objects.filter(LOGINID__id=request.session['userid']).first()
        return render(request,"Client/profile.html",{'users':users})

class update_profile(View):
    def get(self,request):
        users=user_table.objects.filter(LOGINID__id=request.session['userid']).first()
        return render(request,"Client/profile.html",{'users':users})

class edit_profile(View):
    def get(self,request, id):
        user=user_table.objects.filter(LOGINID__id=request.session['userid']).first()
        return render(request,"Client/edit_profile.html",{'user':user})

    
    def post(self, request, id):
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        company_name = request.POST['company_name']
        
        # Get the uploaded file (optional, if a new file is uploaded)
        profileimage = request.FILES.get('profileimage', None)

        # Get the user instance
        client = user_table.objects.get(id=id)
        client.first_name = firstname  # ✅ No comma
        client.last_name = lastname  # ✅ No comma
        client.phone = phone  # ✅ No comma
        client.company_name = company_name  # ✅ No comma
        client.email = email  # ✅ No comma

        # Only update profile image if a new one is uploaded
        if profileimage:
            client.profileimage = profileimage

        client.save()

        messages.success(request, 'Profile updated!')
        return redirect('profile')

    

class sub_req(View):
    def get(self, request):
        # Initialize the form
        form = login_model.objects.get(id = request.session['userid'])
        return render(request, "Client/Submit_camp_request.html", {'form': form})
    def post(self, request):
        # Print request data for debugging
        print(request.POST)
        obj=user_table.objects.get(LOGINID__id = request.session['userid'])

        # Extract multiple selections as lists
        creative_requirements = request.POST.getlist('creative_requirements[]')
        ad_effects = request.POST.getlist('ad_effects[]')
        ad_placement = request.POST.getlist('ad_placement[]')

        # Initialize form with POST data
        form = CampaignRequestForm(request.POST)

        if form.is_valid():
            campaign = form.save(commit=False)  # Save the form without committing to the DB
            
            # Store the lists as comma-separated values (or use JSONField if applicable)
            campaign.creative_requirements = ', '.join(creative_requirements)
            campaign.ad_effects = ', '.join(ad_effects)
            campaign.ad_placement = ', '.join(ad_placement)
            campaign.CLIENT=obj
            campaign.save()  # Save the instance with the updated fields


            files = request.FILES.getlist('ad_files')  # Retrieve multiple files
            for file in files:
                CampaignFile.objects.create(campaign=campaign, file=file)  # Save each file
            messages.success(request, "Your campaign request has been submitted successfully!")
            return redirect('clienthome')

        # If the form is invalid, re-render with errors
        return render(request, "Client/Submit_camp_request.html", {'form': form})
    
class view_camp_request(View):
    def get(self,request):
        req=campaign_request.objects.all()
        return render(request,"Administrators/view_camp_request.html",{'req':req})
    
    
class view_cmp_request(View):
    def get(self,request,id):
        req=campaign_request.objects.filter(id=id).first()
        return render(request,"Administrators/Admin_View_Camp_Request.html",{'req':req})
  
# from .models import campaign_request, Task, employee_table, notification_table
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from .models import campaign_request  # Ensure it's imported

# def accept_campaign(request, campaign_id):
#     campaign = get_object_or_404(campaign_request, id=campaign_id)
    
#     if campaign.status == 'Accepted':  
#         messages.warning(request, "This campaign is already accepted.")
#     else:
#         campaign.status = 'Accepted'
#         campaign.save()
#         messages.success(request, "Campaign accepted successfully.")

#     return redirect('view_camp_request')  # Redirect to the campaign list

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.db.models import Count
from .models import campaign_request, Task, employee_table, Role, Department

# Define role-based tasks for each department
TASK_MAPPING = {
    "Creative Team": [
        {"title": "Create Ad Design", "description": "Design a creative ad", "role": "Graphic Designer"},
        {"title": "Write Ad Copy", "description": "Create ad text", "role": "Copywriter"},
        {"title": "Supervise Creative Work", "description": "Approve ad designs and copies", "role": "Creative Director"}
    ],
    "Campaign Management": [
        {"title": "Manage Campaign Strategy", "description": "Oversee campaign execution", "role": "Campaign Manager"},
        {"title": "Execute Campaign", "description": "Run and monitor ad campaign", "role": "Campaign Executor"}
    ],
    "Ad Operations Department": [
        {"title": "Analyze Performance", "description": "Monitor ad effectiveness", "role": "Ad Performance Analyst"},
        {"title": "Ad Placement", "description": "Manage ad placements", "role": "Ad Placement Specialist"}
    ]
}

# Assign tasks to the least busy employee in the correct role & department
def auto_assign_task(title, description, campaign, role_name, department_name):
    try:
        department = Department.objects.get(name=department_name)
        role = Role.objects.get(name=role_name, department=department)

        # Get employees in the role, sorted by workload
        employees = employee_table.objects.filter(role=role, department=department).annotate(
            task_count=Count('tasks')
        ).order_by('task_count')

        if employees.exists():
            assigned_employee = employees.first()  # Least busy employee
            task = Task.objects.create(
                title=title,
                task_description=description,
                assigned_to=assigned_employee,
                campaign=campaign,
                status="Pending"
            )
            return task
    except (Department.DoesNotExist, Role.DoesNotExist):
        return None
    
    from django.shortcuts import get_object_or_404, redirect
from .models import campaign_request, employee_table, Task

def accept_campaign(request, campaign_id):
    """
    When admin accepts a campaign, it assigns tasks to the correct employees.
    """
    campaign = get_object_or_404(campaign_request, id=campaign_id)
    campaign.status = "Accepted"
    campaign.save()

    for department_name, tasks in TASK_MAPPING.items():
        for task_data in tasks:
            auto_assign_task(task_data["title"], task_data["description"], campaign, task_data["role"], department_name)

    # Redirect to the campaign request list after accepting
    return redirect("view_camp_request")  # Update with the correct URL name

from django.shortcuts import render
from .models import Task, employee_table

from django.shortcuts import render
from .models import Task, employee_table

def view_tasks(request):
    tasks = Task.objects.select_related("assigned_to", "campaign").order_by("assigned_to__full_name")
    employees = employee_table.objects.filter(tasks__isnull=False).distinct().order_by("full_name")

    # 🔍 Debugging
    print("Tasks Count:", tasks.count())
    print("Employees Count:", employees.count())

    return render(request, "Administrators/task_list.html", {
        "tasks": tasks,
        "employees": employees
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, employee_table
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, employee_table

def reassign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    available_employees = employee_table.objects.filter(
        role=task.assigned_to.role, department=task.assigned_to.department
    )

    if request.method == "POST":
        new_employee_id = request.POST.get("new_employee")
        new_employee = get_object_or_404(employee_table, id=new_employee_id)
        task.assigned_to = new_employee
        task.save()
        return redirect("view_tasks")  # Redirect to task list after reassignment

    return render(request, "Administrators/reassign.html", {
        "task": task,
        "employees": available_employees
    })

from django.shortcuts import render, redirect
from .models import Task, employee_table, CreativeUpload

def emp_tasks(request):
    """ View tasks assigned to employees using session-based authentication. """
    
    if 'userid' not in request.session:
        return redirect("login")  # Redirect if no session exists

    try:
        user_id = request.session['userid']  
        employee = employee_table.objects.get(LOGINID=user_id)
    except employee_table.DoesNotExist:
        return redirect("login")

    # ✅ If Creative Director, show all tasks in "Review" status
    if employee.role.name == "Creative Director":
        tasks = Task.objects.filter(status="Review").select_related("campaign")
    else:
        tasks = Task.objects.filter(assigned_to=employee).select_related("campaign")

    # ✅ Fetch uploaded creatives for the tasks
    task_creatives = {task.id: CreativeUpload.objects.filter(task=task) for task in tasks}
    
    return render(request, "Employees/Tasks.html", {
        "tasks": tasks,
        "task_creatives": task_creatives,
        "is_cd": employee.role.name == "Creative Director",
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from .models import Task, employee_table, FinalCreative

def upload_final_creatives(request, task_id):
    """Creative Director uploads multiple final creatives for a task."""

    print("📌 Uploading final creatives...")  # ✅ Debugging: Start function
    print(f"🔹 Task ID: {task_id}")

    if 'userid' not in request.session:
        print("❌ User not authenticated!")  # ✅ Debugging
        return JsonResponse({"success": False, "message": "User not authenticated!"})

    user_id = request.session['userid']
    print(f"🔹 User ID: {user_id}")

    employee = get_object_or_404(employee_table, LOGINID=user_id)
    print(f"🔹 Employee Role: {employee.role.name}")

    if employee.role.name != "Creative Director":
        print("❌ Unauthorized: Only the Creative Director can finalize creatives!")  # ✅ Debugging
        return JsonResponse({"success": False, "message": "Only the Creative Director can finalize creatives!"})

    task = get_object_or_404(Task, id=task_id)
    print(f"✅ Task found: {task}")

    if request.method == "POST":
        uploaded_files = request.FILES.getlist("final_creatives")  # ✅ Get multiple files
        print(f"🔹 Files Received: {uploaded_files}")

        if not uploaded_files:
            print("❌ No files uploaded!")  # ✅ Debugging
            return JsonResponse({"success": False, "message": "No files selected!"})

        saved_files = []
        media_path = "media/final_creatives/"
        
        # ✅ Ensure directory exists
        if not os.path.exists(media_path):
            os.makedirs(media_path)

        fs = FileSystemStorage(location=media_path)

        for file in uploaded_files:
            print(f"📂 Saving file: {file.name}")  # ✅ Debugging

            filename = fs.save(file.name, file)  # ✅ Save each file
            file_path = "final_creatives/" + filename  # ✅ Store correct path
            print(f"✅ File saved at: {file_path}")

            # ✅ Save in FinalCreative model
            FinalCreative.objects.create(
                task=task, file=file_path, reviewed_by=employee
            )
            saved_files.append(file_path)

        print(f"✅ Final creatives uploaded: {saved_files}")
        return JsonResponse({
            "success": True,
            "message": "Final creatives uploaded successfully!",
            "files": saved_files
        })

    print("❌ File upload failed!")  # ✅ Debugging
    return JsonResponse({"success": False, "message": "File upload failed!"})

def send_creative_to_client(request, task_id):
    """Send the final approved creative to the client."""

    print("📌 Sending final creatives to the client...")  # ✅ Debugging
    print(f"🔹 Task ID: {task_id}")

    if 'userid' not in request.session:
        print("❌ User not authenticated!")  # ✅ Debugging
        return JsonResponse({"success": False, "message": "User not authenticated!"})

    user_id = request.session['userid']
    print(f"🔹 User ID: {user_id}")

    employee = get_object_or_404(employee_table, LOGINID=user_id)
    print(f"🔹 Employee Role: {employee.role.name}")

    if employee.role.name != "Creative Director":
        print("❌ Unauthorized: Only the Creative Director can send creatives!")  # ✅ Debugging
        return JsonResponse({"success": False, "message": "Only the Creative Director can send creatives to the client!"})

    task = get_object_or_404(Task, id=task_id)
    print(f"✅ Task found: {task}")

    # ✅ Check if there are final creatives before marking them as sent
    final_creatives = FinalCreative.objects.filter(task=task, sent_to_client=False)
    if not final_creatives.exists():
        print("❌ No approved creatives found!")  # ✅ Debugging
        return JsonResponse({"success": False, "message": "No approved creatives found to send!"})

    # ✅ Mark all final creatives as sent
    final_creatives.update(sent_to_client=True)
    print("✅ All creatives marked as sent to the client.")  # ✅ Debugging

    # ✅ Update task status to "Client Review"
    task.status = "Client Review"
    task.save()
    print(f"✅ Task status updated: {task.status}")  # ✅ Debugging

    return JsonResponse({"success": True, "message": "Final creatives sent to client!"})


# def send_creative_to_client(request, task_id):
#     """Send the final approved creative to the client."""

#     print("📌 Sending final creatives to the client...")  # ✅ Debugging
#     print(f"🔹 Task ID: {task_id}")

#     if 'userid' not in request.session:
#         print("❌ User not authenticated!")  # ✅ Debugging
#         return JsonResponse({"success": False, "message": "User not authenticated!"})

#     user_id = request.session['userid']
#     print(f"🔹 User ID: {user_id}")

#     employee = get_object_or_404(employee_table, LOGINID=user_id)
#     print(f"🔹 Employee Role: {employee.role.name}")

#     if employee.role.name != "Creative Director":
#         print("❌ Unauthorized: Only the Creative Director can send creatives!")  # ✅ Debugging
#         return JsonResponse({"success": False, "message": "Only the Creative Director can send creatives to the client!"})

#     task = get_object_or_404(Task, id=task_id)
#     print(f"✅ Task found: {task}")

#     # ✅ Check if there are final creatives before marking them as sent
#     final_creatives = FinalCreative.objects.filter(task=task, sent_to_client=False)
#     if not final_creatives.exists():
#         print("❌ No approved creatives found!")  # ✅ Debugging
#         return JsonResponse({"success": False, "message": "No approved creatives found to send!"})

#     # ✅ Mark all final creatives as sent
#     final_creatives.update(sent_to_client=True)
#     print("✅ All creatives marked as sent to the client.")  # ✅ Debugging

#     # ✅ Update task status to "Client Review"
#     task.status = "Client Review"
#     task.save()
#     print(f"✅ Task status updated: {task.status}")  # ✅ Debugging

#     return JsonResponse({"success": True, "message": "Final creatives sent to client!"})




from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CampaignFile, campaign_request

@login_required
def client_campaign_creatives(request, campaign_id):
    # Ensure the campaign exists and belongs to the logged-in client
    campaign = get_object_or_404(campaign_request, id=campaign_id, client=request.user)

    # Get all creatives related to this campaign
    creatives = CampaignFile.objects.filter(campaign=campaign)

    return render(request, 'client/campaign_creatives.html', {'campaign': campaign, 'creatives': creatives})











from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import login_model, user_table, campaign_request, FinalCreative

def client_campaigns(request):
    """Show only approved campaigns of the logged-in client and their final creatives."""

    user_id = request.session.get("userid")  # ✅ Get logged-in client ID
    if not user_id:
        return redirect("/login")  # Redirect to login if session does not exist

    # ✅ Get logged-in client
    login_user = get_object_or_404(login_model, id=user_id)
    user = get_object_or_404(user_table, LOGINID=login_user)

    # ✅ Check the correct field for approval (e.g., `status`)
    campaigns = campaign_request.objects.filter(CLIENT=user, status="Accepted")

    return render(request, "Client/View_campaign.html", {"campaigns": campaigns})

# import json
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from .models import campaign_request, FinalCreative, notification_table

# def client_campaign_creatives(request, campaign_id):
#     """Display the final approved creatives for a client's campaign."""
    
#     campaign = get_object_or_404(campaign_request, id=campaign_id)

#     # ✅ Fetch all final creatives linked to the campaign
#     final_creatives = FinalCreative.objects.filter(task__campaign=campaign)

#     return render(request, "Client/View_final_creatives.html", {
#         "campaign": campaign,
#         "final_creatives": final_creatives
#     })

# @csrf_exempt  # Only use this if you're testing API calls without CSRF token
# def approve_or_reject_final_creative(request, creative_id):
#     """
#     Handles approving or rejecting final creatives by the client.
#     Works with `FinalCreative` model.
#     """
#     final_creative = get_object_or_404(FinalCreative, id=creative_id)  # Get the creative
#     campaign = final_creative.task.campaign  # Get the related campaign

#     if request.method == "POST":
#         try:
#             # Check if JSON or Form Data is received
#             if request.content_type == "application/json":
#                 data = json.loads(request.body)
#             else:
#                 data = request.POST  # Handle form data

#             action = data.get("action", "").strip()  # Ensure action is retrieved safely
#             message = data.get("message", "").strip()

#             # Debugging: Print received data
#             print(f"Received Data: action={action}, message={message}")

#             if not action:
#                 return JsonResponse({"error": "Missing action parameter"}, status=400)

#             # ✅ Approve Final Creative
#             if action == "approve":
#                 final_creative.sent_to_client = True
#                 final_creative.approved_by_client = True  # Mark as approved
#                 final_creative.save()

#                 final_creative.task.status = "Completed"
#                 final_creative.task.save()

#                 messages.success(request, "Final creative approved by client!")  

#             # ❌ Reject Final Creative
#             elif action == "reject":
#                 if not message:
#                     return JsonResponse({"error": "Rejection message is required"}, status=400)

#                 final_creative.sent_to_client = False
#                 final_creative.approved_by_client = False  # Mark as not approved
#                 final_creative.task.status = "Review"
#                 final_creative.task.feedback = message  # Store rejection reason
#                 final_creative.task.save()

#                 # ✅ Notify Creative Director  
#                 notification_table.objects.create(
#                     CLIENT=campaign.CLIENT,  # ✅ Correct field name
#                     description=f"Final creative {final_creative.id} was rejected by the client. Reason: {message}",
#                     status="Pending Review"
#                 )

#                 messages.warning(request, "Final creative rejected and sent for review.")  

#             else:
#                 return JsonResponse({"error": "Invalid action provided"}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format!"}, status=400)

#         return redirect("client_campaign_creatives", campaign_id=campaign.id)

#     return JsonResponse({"error": "Invalid request method!"}, status=405)

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import campaign_request, FinalCreative, notification_table

def client_campaign_creatives(request, campaign_id):
    """Display the final approved creatives for a client's campaign."""
    
    campaign = get_object_or_404(campaign_request, id=campaign_id)

    # ✅ Fetch all final creatives linked to the campaign
    final_creatives = FinalCreative.objects.filter(task__campaign=campaign)

    return render(request, "Client/View_final_creatives.html", {
        "campaign": campaign,
        "final_creatives": final_creatives
    })

@csrf_exempt  # Only use this if you're testing API calls without CSRF token
def approve_or_reject_final_creative(request, creative_id):
    """
    Handles approving or rejecting final creatives by the client.
    Works with `FinalCreative` model.
    """
    final_creative = get_object_or_404(FinalCreative, id=creative_id)  # Get the creative
    campaign = final_creative.task.campaign  # Get the related campaign

    if request.method == "POST":
        try:
            # Check if JSON or Form Data is received
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST  # Handle form data

            action = data.get("action", "").strip()  # Ensure action is retrieved safely
            message = data.get("message", "").strip()

            if not action:
                return JsonResponse({"error": "Missing action parameter"}, status=400)

            # ✅ Approve Final Creative
            if action == "approve":
                final_creative.sent_to_client = True
                final_creative.approved_by_client = True  # Mark as approved
                final_creative.save()

                final_creative.task.status = "Completed"
                final_creative.task.save()

                # ✅ Notify Creative Director about the approval
                notification_table.objects.create(
                    CLIENT=campaign.CLIENT,  # The campaign's client is notified
                    description=f"Final creative {final_creative.id} has been approved by the client.",
                    status="unread"  # Mark the notification as unread
                )

                messages.success(request, "Final creative approved by client!")

            # ❌ Reject Final Creative
            elif action == "reject":
                if not message:
                    return JsonResponse({"error": "Rejection message is required"}, status=400)

                final_creative.sent_to_client = False
                final_creative.approved_by_client = False  # Mark as not approved
                final_creative.task.status = "Review"
                final_creative.task.feedback = message  # Store rejection reason
                final_creative.task.save()

                # ✅ Notify Creative Director about the rejection
                notification_table.objects.create(
                    CLIENT=campaign.CLIENT,  # The campaign's client is notified
                    description=f"Final creative {final_creative.id} was rejected by the client. Reason: {message}",
                    status="unread"  # Mark the notification as unread
                )

                messages.warning(request, "Final creative rejected and sent for review.")

            else:
                return JsonResponse({"error": "Invalid action provided"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format!"}, status=400)

        return redirect("client_campaign_creatives", campaign_id=campaign.id)

    return JsonResponse({"error": "Invalid request method!"}, status=405)

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import campaign_request, FinalCreative, notification_table, employee_table
from django.shortcuts import render, redirect
from .models import employee_table, notification_table

from django.shortcuts import render, redirect
from .models import employee_table, notification_table

def creative_director_notifications(request):
    """Display all notifications for the Creative Director."""
    
    # Check if the user is authenticated via session
    if 'userid' not in request.session:
        return redirect('login')  # Redirect to login page if session has no user ID
    
    try:
        # Fetch user based on session ID
        user = login_model.objects.get(id=request.session['userid'])
        
        # Fetch the employee by matching LOGINID with the logged-in user
        employee = employee_table.objects.get(LOGINID=user)

        # Fetch unread notifications
        notifications = notification_table.objects.filter(status="unread")

        # Get employee's profile image or default image if not available
        employee_image = employee.profileimage.url if employee.profileimage else "/static/images/default-avatar.png"

        # Pass employee name along with the notifications and image to the template
        return render(request, "Employees/cdnotifications.html", {
            "notifications": notifications,
            "employee_name": employee.full_name,  # Pass employee name to template
            "employee_image": employee_image,  # Pass employee image to template
        })
    
    except login_model.DoesNotExist:
        # Handle case where user does not exist in the login model
        return redirect('error_page')  # Redirect to an error page (create one if needed)

    except employee_table.DoesNotExist:
        # Handle case where no matching employee is found
        return redirect('error_page')  # Redirect to an error page (create one if needed)
from django.shortcuts import render, get_object_or_404, redirect
from .models import FinalCreative, CampaignFile
from django.contrib import messages

def reupload_final_creative(request, creative_id):
    """Allow the Creative Team to upload a new version of a rejected creative."""
    
    final_creative = get_object_or_404(FinalCreative, id=creative_id)  # Get the rejected creative
    campaign = final_creative.task.campaign  # Get the related campaign

    # Check if the current user has permission to upload creatives
    # Assuming the current user is a member of the Creative Team
    if request.user.role != "Creative Team":
        messages.error(request, "You do not have permission to upload creatives.")
        return redirect("home")

    if request.method == "POST" and request.FILES:
        # Handle the uploaded files
        uploaded_file = request.FILES.get('creative_file')
        
        if uploaded_file:
            # Save the new creative file
            CampaignFile.objects.create(creative=final_creative, file=uploaded_file)
            
            # Update the final creative status to "Pending Approval"
            final_creative.sent_to_client = False  # Reset to not sent
            final_creative.approved_by_client = False  # Reset approval status
            final_creative.save()

            # Update task status back to "In Progress"
            final_creative.task.status = "In Progress"
            final_creative.task.save()

            messages.success(request, "Creative re-uploaded successfully! Please wait for client approval.")
            return redirect("client_campaign_creatives", campaign_id=campaign.id)
        else:
            messages.error(request, "Please upload a valid file.")
            
    return render(request, "CreativeTeam/reupload_creative.html", {"final_creative": final_creative})

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from .models import Task, employee_table, CreativeUpload

# def upload_creative(request, task_id):
#     """ Employees upload multiple creatives for assigned tasks. """

#     if "userid" not in request.session:
#         messages.error(request, "Unauthorized. Please log in.")
#         return redirect("employee_tasks")  # Redirect to employee tasks page

#     employee = get_object_or_404(employee_table, LOGINID=request.session["userid"])
#     task = get_object_or_404(Task, id=task_id, assigned_to=employee)

#     if request.method == "POST" and request.FILES.getlist("creative_files"):
#         for file in request.FILES.getlist("creative_files"):
#             CreativeUpload.objects.create(
#                 task=task,
#                 uploaded_by=employee,
#                 file=file
#             )
#         messages.success(request, "Creatives uploaded successfully!")
#     else:
#         messages.error(request, "Invalid request! Please select files to upload.")

#     return redirect("employee_tasks")  # Redirect back to tasks page


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task, employee_table, CreativeUpload

def upload_creative(request, task_id):
    """ Allow only Creative Team (except Creative Director) to upload creatives. """

    if "userid" not in request.session:
        messages.error(request, "Unauthorized. Please log in.")
        return redirect("employee_tasks")  # Redirect to employee tasks page

    employee = get_object_or_404(employee_table, LOGINID=request.session["userid"])

    # ✅ Ensure only allowed roles (Creative Team except Creative Director) can upload creatives
    allowed_roles = ["Graphic Designer", "Content Creator", "Copywriter"]
    if employee.role.name not in allowed_roles:
        messages.error(request, "You are not authorized to upload creatives.")
        return redirect("employee_tasks")

    task = get_object_or_404(Task, id=task_id, assigned_to=employee)

    if request.method == "POST" and request.FILES.getlist("creative_files"):
        for file in request.FILES.getlist("creative_files"):
            CreativeUpload.objects.create(
                task=task,
                uploaded_by=employee,
                file=file
            )

        # ✅ Update task status to "Review" when creative is uploaded
        if task.status != "Review":
            task.status = "Review"
            task.save()

        messages.success(request, "Creatives uploaded successfully! Task status updated to 'Review'.")
    else:
        messages.error(request, "Invalid request! Please select files to upload.")

    return redirect("employee_tasks")  # Redirect back to tasks page

from django.shortcuts import redirect
from .models import CreativeUpload

@csrf_exempt
def approve_creative(request, creative_id):
    if request.method == "POST":
        try:
            # Retrieve form data from POST request
            action = request.POST.get("action")
            print("✅ Action:", action)  # Debug log

            # Fetch the creative file
            creative = CreativeUpload.objects.get(id=creative_id)
            print("✅ Creative Found:", creative)

            if action == "approve":
                creative.status = "Approved"
            elif action == "reject":
                creative.status = "Rejected"
            else:
                print("❌ Invalid Action")
                return redirect('employee_tasks')  # Redirect to an error page if action is invalid

            creative.save()
            print("✅ Status Updated Successfully")
            
            # Redirect to the task page or any other appropriate page
            return redirect('employee_tasks', task_id=creative.task.id)  # Replace with correct view name and task_id

        except CreativeUpload.DoesNotExist:
            print("❌ Creative Not Found")
            return redirect('employee_tasks')  # Redirect to an error page if creative is not found
        except Exception as e:
            print("❌ Error:", str(e))
            return redirect('employee_tasks')  # Redirect on general error

    return redirect('employee_tasks')  # If not POST method, redirect to error page

# from django.shortcuts import render
# from .models import CreativeUpload
# import os

# def view_creatives(request, task_id):
#     # Get all creatives for a specific task
#     creatives = CreativeUpload.objects.filter(task_id=task_id)

#     for creative in creatives:
#         if creative.file.url.lower().endswith(".txt"):
#             # Read the content of the text file
#             file_path = creative.file.path
#             with open(file_path, 'r') as file:
#                 creative.text_content = file.read()

#     return render(request, 'Employees/view_creatives.html', {'creatives': creatives})
from django.shortcuts import render, get_object_or_404
from .models import CreativeUpload, Task

def view_creatives(request, task_id):
    # Get the specific task (campaign)
    task = get_object_or_404(Task, id=task_id)

    # Get creatives only for this task
    creatives = CreativeUpload.objects.filter(task=task)

    return render(request, 'Employees/view_creatives.html', {
        'task': task,
        'creatives': creatives
    })

# @csrf_exempt
# def finalize_creative(request, task_id):
#     """ Allow Creative Director to finalize approved creatives and send them to the client """
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             feedback = data.get("feedback", "")

#             task = Task.objects.get(id=task_id)
#             creatives = task.creatives.filter(status="Approved")

#             if not creatives.exists():
#                 return JsonResponse({"error": "No approved creatives to finalize!"}, status=400)

#             task.status = "Completed"
#             task.feedback = feedback
#             task.save()

#             return JsonResponse({"message": "Final creative sent for client approval!"})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     return JsonResponse({"error": "Invalid request"}, status=400)


# from django.shortcuts import render
# from .models import Task  # Ensure Task model is imported

# def admin_view_tasks(request):
#     tasks = Task.objects.all()  # Fetch all assigned tasks
#     return render(request, "Administrators/task_list.html", {"tasks": tasks})












    
class reject_campaign(View):
       def get(self,request, id):
        print("dddddd")
        cam=campaign_request.objects.get(id=id)
        cam.status="Rejected"
        cam.save()
        notification_table.objects.create(
        CLIENT=cam.CLIENT,
        description=f"Your campaign request '{cam.campaign_name}' has been accepted.",status='unread'
    )
        return redirect('view_camp_request')
    
class mng_employee(View):
    def get(self,request):
        a=employee_table.objects.all()
        return render(request,"Administrators/Manage_employee.html",{'a':a})
    


from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import employee_table, user_table  # Make sure to import the models
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import employee_table, login_model

class edit_employee(View):
    def get(self, request, id):
        # Fetch the employee record from the database using the id
        try:
            employee = employee_table.objects.get(id=id)
        except employee_table.DoesNotExist:
            messages.error(request, 'Employee not found!')
            return redirect('mng_employee')  # Redirect to the employee management page
        
        return render(request, "Administrators/Edit_employee.html", {'employee': employee})

    def post(self, request, id):
        # Fetch the employee record from the database using the id
        try:
            employee = employee_table.objects.get(id=id)
        except employee_table.DoesNotExist:
            messages.error(request, 'Employee not found!')
            return redirect('mng_employee')
        
        # Get the updated values from the form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        job_title = request.POST.get('job_title')
        # date_of_joining = request.POST.get('date_of_joining')
        password = request.POST.get('password')
        
        profileimage = request.FILES.get('image', None)  # Profile image is optional
        
        # Update the employee details
        employee.full_name = full_name
        employee.email = email
        employee.phone = phone
        employee.role = role
        employee.job_title = job_title
        # employee.date_of_joining = date_of_joining
        
        if profileimage:
            employee.profileimage = profileimage
        
        employee.save()

        # Update the associated user details (login model)
        user = employee.LOGINID
        if password:  # Only update password if provided
            user.password = password  # Consider hashing the password if necessary
        user.save()

        messages.success(request, 'Employee details updated successfully!')
        return redirect('mng_employee')  # Redirect to the employee management page
from django.http import JsonResponse
from .models import Role

def get_roles(request):
    department_id = request.GET.get('department_id')
    if department_id:
        roles = Role.objects.filter(department_id=department_id).values('id', 'name')
        return JsonResponse(list(roles), safe=False)
    return JsonResponse([], safe=False)





from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
import random
import string
from .models import login_model, employee_table
from .forms import EmployeeForm

def generate_random_password(length=10):
    """Generate a random password with letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            print("✅ Form is valid")  # Debugging

            employee = form.save(commit=False)
            print(f"🔹 Employee Data Before Save: {employee.full_name}, {employee.email}, {employee.department}, {employee.role}")

            random_password = generate_random_password()
            print(f"🔹 Generated Password: {random_password}")

            try:
                user = login_model.objects.create(
                    username=employee.email, 
                    password=random_password,  
                    type='employee',
                )
                employee.LOGINID = user  

                employee.save()
                print(f"✅ Employee {employee.full_name} saved successfully!")  

            except Exception as e:
                print(f"❌ Error saving employee: {e}")

            messages.success(request, '✅ Employee Added Successfully')
            return redirect('mng_employee')

        else:
            print(f"❌ Form is invalid: {form.errors}")  # Debugging

    else:
        form = EmployeeForm()

    return render(request, 'Administrators/add_employee.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import login_model  

class ChangePasswordView(View):
    def get(self, request):
        if 'userid' not in request.session:  
            return redirect('login')  # Redirect to login if not logged in
        return render(request, "Employees/password_reset.html")

    def post(self, request):
        if 'userid' not in request.session:
            return redirect('login')

        user_id = request.session['userid']
        user = login_model.objects.get(id=user_id)

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if old password matches
        if user.password != old_password:
            messages.error(request, "Old password is incorrect!")
            return redirect('change_password')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match!")
            return redirect('change_password')

        # Update password
        user.password = new_password  # Store as plain text (⚠ Not recommended! See security note below)
        user.save()

        messages.success(request, "Password changed successfully!")
        return redirect('emphome')  # Redirect to employee home page


class delete_employee(View):
    def get(self,request,id):
        a=employee_table.objects.get(id=id).delete()
        return redirect('mng_employee')



    
class Adinventory(View):
    def get(self,request):
        return render(request,"Admin/Ad_inventory.html")
    

















