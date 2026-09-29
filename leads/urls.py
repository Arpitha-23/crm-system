
from django.urls import path

from . import views


urlpatterns = [

    # ============================================================
    # DASHBOARD
    # ============================================================

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),


    # ============================================================
    # LEADS
    # ============================================================

    path(
        'leads/',
        views.lead_list,
        name='lead_list'
    ),

    path(
        'leads/create/',
        views.lead_create,
        name='lead_create'
    ),

    path(
        'leads/<int:pk>/',
        views.lead_detail,
        name='lead_detail'
    ),

    path(
        'leads/<int:pk>/edit/',
        views.lead_edit,
        name='lead_edit'
    ),


    # ============================================================
    # FOLLOW-UP / ACTIVITY
    # ============================================================

    path(
        'leads/<int:lead_id>/activity/create/',
        views.activity_create,
        name='activity_create'
    ),


    # ============================================================
    # CSV IMPORT
    # ============================================================

    path(
        'import/',
        views.import_leads,
        name='import_leads'
    ),


    # ============================================================
    # LEAD SCORE RULES
    # ADMIN / MANAGER ONLY
    # ============================================================

    path(
        'score-rules/',
        views.score_rule_list,
        name='score_rule_list'
    ),

    path(
        'score-rules/<int:pk>/delete/',
        views.score_rule_delete,
        name='score_rule_delete'
    ),

]
