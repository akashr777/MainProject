
from django.urls import path
# from .views import assign_task,employee_tasks, upload_creative
from .views import get_roles
# from .views import get_employees
# from .views import view_task
# from .views import accept_campaign  # Ensure it's correctly imported
from django.conf.urls.static import static
from django.conf import settings

from .views import *
from . import views


urlpatterns = [


    path('',homepage.as_view(),name='homepage'),
    path('registration',registration.as_view(),name='registration'),
    path('login/',login.as_view(),name='login'),
    path('ForgotPasswordView', ForgotPasswordView.as_view(), name='ForgotPasswordView'),
    path('adminhome',adminhome.as_view(),name='adminhome'),
    path('clienthome',clienthome.as_view(),name='clienthome'),
    path("get-notifications/", get_notifications, name="get_notifications"),
    path("mark-notifications-read/", mark_notifications_as_read, name="mark_notifications_as_read"),
    path('emphome',emphome.as_view(),name='emphome'),
    path('about',about.as_view(),name='about'),
    path('profile',profile.as_view(),name='profile'),
    path('edit_profile/<int:id>',edit_profile.as_view(),name='edit_profile'),
    path('mng_client',mng_client.as_view(),name='mng_client'),
    path('mng_employee',mng_employee.as_view(),name='mng_employee'),
    path('add_employee/', add_employee, name='add_employee'),  
    path('edit_employee/<int:id>',edit_employee.as_view(),name='edit_employee'),
    # path('add_department/', add_department, name='add_department'),

    path('delete_employee/<int:id>',delete_employee.as_view(),name='delete_employee'),
    path('delete_client/<int:id>',delete_client.as_view(),name='delete_client'),
    # path('accept_campaign/<int:id>',accept_campaign.as_view(),name='accept_campaign'),
    path("accept-campaign/<int:campaign_id>/", accept_campaign, name="accept_campaign"),

    path('reject_campaign/<int:id>',reject_campaign.as_view(),name='reject_campaign'),
    path('sub_req',sub_req.as_view(),name='sub_req'),
    path('view_camp_request',view_camp_request.as_view(),name='view_camp_request'),
    path('view_cmp_request/<int:id>',view_cmp_request.as_view(),name='view_cmp_request'),


    # path('assign_task/', assign_task, name='assign_task'),
    # path('admin_task_list/', admin_task_list, name='admin_task_list'),


    # path('employee_tasks/', employee_tasks, name='employee_tasks'),  
    # path('task/<int:task_id>', views.task_detail, name='task_detail'),

    # path('task/<int:task_id>/', view_task, name='view_task'),  # ✅ Task details page

    path("tasks/", views.view_tasks, name="view_tasks"),  # Ensure this path exists

    path('reassign-task/<int:task_id>/', reassign_task, name='reassign_task'),
    path('employee_tasks/', emp_tasks, name='employee_tasks'),  # URL for viewing employee tasks
    path('upload_creative/<int:task_id>/', upload_creative, name='upload_creative'),  # Upload creative
    path('approve_creative/<int:creative_id>/', views.approve_creative, name='approve_creative'),

    path('view-creatives/<int:task_id>/', views.view_creatives, name='view_creatives'),

    path("upload-final-creatives/<int:task_id>/", upload_final_creatives, name="upload_final_creatives"),
    path("send-final-creative/<int:task_id>/", send_creative_to_client, name="send_final_creative"),

    path('client/campaigns/', views.client_campaigns, name='client_campaigns'),

      path("approve/<int:campaign_id>/", approve_creative, name="approve_client_creative"),
    path('creative-director/notifications/', views.creative_director_notifications, name='creative_director_notifications'),
    path("client/campaign/<int:campaign_id>/creatives/", client_campaign_creatives, name="client_campaign_creatives"),

    path('client/final-creative/<int:creative_id>/approval/', approve_or_reject_final_creative, name='approve_or_reject_final_creative'),


    # path('finalize_creative/<int:task_id>/', finalize_creative, name='finalize_creative'),  # Final approval

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),



    # path('upload-creative/<int:task_id>/', views.upload_creative, name='upload_creative'),
    # path('emp_adlist', emp_adlist.as_view(), name='emp_adlist'),


    # path('review_creative/<int:campaign_id>/', review_creative, name='review_creative'),


    # path('client/accepted_campaigns/', views.client_accepted_campaigns, name='client_accepted_campaigns'),

    # path("upload_final_creative/<int:campaign_id>/", upload_final_creative, name="upload_final_creative"),

    # path('finalize_creative/<int:campaign_id>/', finalize_creative_submission, name='finalize_creative_submission'),


    # path('review-project/<int:project_id>/', views.review_project, name='review_project'),
    # path('submit-final-ad/<int:project_id>/', views.submit_final_ad, name='submit_final_ad'),

    # path("tasks/<int:task_id>/delete/", delete_task, name="delete_task"),


    # path('send_final_creative_to_client/<int:campaign_id>/', send_final_creative_to_client, name='send_final_creative_to_client'),

    # path('send_final_creative_to_client/<int:campaign_id>/', send_final_creative_to_client, name='send_final_creative_to_client'),

    # path('campaign/<int:campaign_id>/ad-creatives/', view_ad_creatives, name='view_ad_creatives'),



    # path('adcreative/<int:creative_id>/approve/', approve_adcreative, name="approve_adcreative"),
    # path('adcreative/<int:creative_id>/reject/', reject_adcreative, name="reject_adcreative"),
    # path('adcreative/<int:creative_id>/reply/', reply_adcreative, name="reply_adcreative"),


    path('Adinventory',Adinventory.as_view(),name='Adinventory'),




    path('get_roles/', get_roles, name='get_roles'),  # ✅ URL for AJAX


    # path("get_employees/", get_employees, name="get_employees"),



    # path("get_campaign_details/", get_campaign_details, name="get_campaign_details"),

    # path('ad_inventory/', ad_inventory_view, name='ad_inventory'),  # ✅ Correct Path
    # path('ad-space/create/', create_ad_space, name='create_ad_space'),
    # path('time-slot/create/', create_time_slot, name='create_time_slot'),
    # path('ad-space/delete/<int:ad_space_id>/', delete_ad_space, name='delete_ad_space'),
    # path('time-slot/delete/<int:time_slot_id>/', delete_time_slot, name='delete_time_slot'),

    # path("assign-ad/", assign_ad_to_slot, name="assign_ad"),






]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)