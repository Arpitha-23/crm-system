
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.utils import timezone
from .decorators import manager_required

from django.db.models import Avg, Q

from django.contrib import messages

from django.contrib.auth.decorators import login_required

import csv

from .models import (
    Lead,
    LeadScoreRule
)

from .forms import (
    LeadForm,
    ActivityForm
)

from .services import calculate_lead_score


# ============================================================
# LEAD LIST
# ============================================================


@login_required
def lead_list(request):

    leads = Lead.objects.all().order_by('-created_at')

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        leads = leads.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(company__icontains=search)
        )

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if status:

        leads = leads.filter(
            status=status
        )

    min_score = request.GET.get(
        'min_score',
        ''
    ).strip()

    if min_score:

        try:

            leads = leads.filter(
                score__gte=int(min_score)
            )

        except ValueError:

            pass

    return render(
        request,
        'leads/lead_list.html',
        {
            'leads': leads,
            'search': search,
            'selected_status': status,
            'min_score': min_score,
        }
    )
# ============================================================
# CREATE LEAD
# ============================================================

@login_required
def lead_create(request):

    if request.method == 'POST':

        form = LeadForm(
            request.POST
        )

        if form.is_valid():

            lead = form.save(
                commit=False
            )

            lead.created_by = request.user

            # Calculate lead score automatically
            lead.score = calculate_lead_score(
                lead
            )

            lead.save()

            messages.success(
                request,
                'Lead created successfully.'
            )

            return redirect(
                'lead_list'
            )

    else:

        form = LeadForm()

    return render(
        request,
        'leads/lead_form.html',
        {
            'form': form
        }
    )


# ============================================================
# LEAD DETAIL
# ============================================================

@login_required
def lead_detail(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk
    )

    activities = lead.activities.all()

    # Upcoming follow-ups
    upcoming_activities = activities.filter(
        completed=False,
        due_date__isnull=False,
        due_date__gte=timezone.now()
    ).order_by(
        'due_date'
    )

    # Overdue follow-ups
    overdue_activities = activities.filter(
        completed=False,
        due_date__isnull=False,
        due_date__lt=timezone.now()
    ).order_by(
        'due_date'
    )

    # Completed activities
    completed_activities = activities.filter(
        completed=True
    ).order_by(
        '-created_at'
    )

    context = {

        'lead': lead,

        'activities': activities,

        'upcoming_activities':
            upcoming_activities,

        'overdue_activities':
            overdue_activities,

        'completed_activities':
            completed_activities,

    }

    return render(
        request,
        'leads/lead_detail.html',
        context
    )


# ============================================================
# EDIT LEAD
# ============================================================

@login_required
def lead_edit(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk
    )

    if request.method == 'POST':

        form = LeadForm(
            request.POST,
            instance=lead
        )

        if form.is_valid():

            old_status = lead.status

            lead = form.save(
                commit=False
            )

            # Recalculate lead score
            lead.score = calculate_lead_score(
                lead
            )

            # Record conversion date
            # when lead becomes Closed Won
            if (
                lead.status == 'closed_won'
                and old_status != 'closed_won'
            ):

                lead.converted_at = timezone.now()

            # Clear conversion date if lead
            # moves away from Closed Won
            elif (
                lead.status != 'closed_won'
                and old_status == 'closed_won'
            ):

                lead.converted_at = None

            lead.save()

            messages.success(
                request,
                'Lead updated successfully.'
            )

            return redirect(
                'lead_detail',
                pk=lead.pk
            )

    else:

        form = LeadForm(
            instance=lead
        )

    return render(
        request,
        'leads/lead_form.html',
        {
            'form': form,
            'edit_mode': True,
            'lead': lead
        }
    )


# ============================================================
# CREATE ACTIVITY / FOLLOW-UP
# ============================================================

@login_required
def activity_create(request, lead_id):

    lead = get_object_or_404(
        Lead,
        pk=lead_id
    )

    if request.method == 'POST':

        form = ActivityForm(
            request.POST
        )

        if form.is_valid():

            activity = form.save(
                commit=False
            )

            activity.lead = lead

            activity.user = request.user

            activity.save()

            messages.success(
                request,
                'Follow-up activity created successfully.'
            )

            return redirect(
                'lead_detail',
                pk=lead.pk
            )

    else:

        form = ActivityForm()

    return render(
        request,
        'leads/activity_form.html',
        {
            'form': form,
            'lead': lead
        }
    )


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    # --------------------------------------------------------
    # Basic Statistics
    # --------------------------------------------------------

    total_leads = Lead.objects.count()

    qualified_leads = Lead.objects.filter(
        status='qualified'
    ).count()

    closed_won = Lead.objects.filter(
        status='closed_won'
    ).count()

    closed_lost = Lead.objects.filter(
        status='closed_lost'
    ).count()


    # --------------------------------------------------------
    # Average Lead Score
    # --------------------------------------------------------

    average_score = Lead.objects.aggregate(
        average=Avg('score')
    )['average'] or 0


    # --------------------------------------------------------
    # Conversion Rate
    # --------------------------------------------------------

    total_closed = (
        closed_won +
        closed_lost
    )

    if total_closed > 0:

        conversion_rate = (
            closed_won /
            total_closed
        ) * 100

    else:

        conversion_rate = 0


    # --------------------------------------------------------
    # Pipeline Data
    # --------------------------------------------------------

    pipeline_data = [

        {
            'name': 'New',
            'count': Lead.objects.filter(
                status='new'
            ).count()
        },

        {
            'name': 'Contacted',
            'count': Lead.objects.filter(
                status='contacted'
            ).count()
        },

        {
            'name': 'Qualified',
            'count': Lead.objects.filter(
                status='qualified'
            ).count()
        },

        {
            'name': 'Proposal',
            'count': Lead.objects.filter(
                status='proposal'
            ).count()
        },

        {
            'name': 'Negotiation',
            'count': Lead.objects.filter(
                status='negotiation'
            ).count()
        },

        {
            'name': 'Closed Won',
            'count': Lead.objects.filter(
                status='closed_won'
            ).count()
        },

        {
            'name': 'Closed Lost',
            'count': Lead.objects.filter(
                status='closed_lost'
            ).count()
        },

    ]


    # --------------------------------------------------------
    # Chart Data
    # --------------------------------------------------------

    pipeline_labels = [

        item['name']

        for item in pipeline_data

    ]

    pipeline_values = [

        item['count']

        for item in pipeline_data

    ]


    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------

    context = {

        'total_leads':
            total_leads,

        'qualified_leads':
            qualified_leads,

        'closed_won':
            closed_won,

        'closed_lost':
            closed_lost,

        'average_score':
            round(
                average_score,
                2
            ),

        'conversion_rate':
            round(
                conversion_rate,
                2
            ),

        'pipeline_data':
            pipeline_data,

        'pipeline_labels':
            pipeline_labels,

        'pipeline_values':
            pipeline_values,

    }


    return render(
        request,
        'leads/dashboard.html',
        context
    )


# ============================================================
# IMPORT LEADS FROM CSV
# ============================================================

@login_required
def import_leads(request):

    if request.method == 'POST':

        csv_file = request.FILES.get(
            'csv_file'
        )

        if not csv_file:

            messages.error(
                request,
                'Please select a CSV file.'
            )

            return redirect(
                'import_leads'
            )


        # ----------------------------------------------------
        # Check file extension
        # ----------------------------------------------------

        if not csv_file.name.lower().endswith(
            '.csv'
        ):

            messages.error(
                request,
                'Only CSV files are allowed.'
            )

            return redirect(
                'import_leads'
            )


        try:

            decoded_file = (

                csv_file
                .read()
                .decode('utf-8-sig')
                .splitlines()

            )

            reader = csv.DictReader(
                decoded_file
            )


            created_count = 0

            skipped_count = 0


            # ------------------------------------------------
            # Process each row
            # ------------------------------------------------

            for row in reader:

                email = row.get(
                    'email',
                    ''
                ).strip()


                # --------------------------------------------
                # Email required
                # --------------------------------------------

                if not email:

                    skipped_count += 1

                    continue


                # --------------------------------------------
                # Prevent duplicate emails
                # --------------------------------------------

                if Lead.objects.filter(
                    email=email
                ).exists():

                    skipped_count += 1

                    continue


                # --------------------------------------------
                # Create Lead
                # --------------------------------------------

                lead = Lead.objects.create(

                    first_name=row.get(
                        'first_name',
                        ''
                    ).strip(),

                    last_name=row.get(
                        'last_name',
                        ''
                    ).strip(),

                    email=email,

                    phone=row.get(
                        'phone',
                        ''
                    ).strip(),

                    company=row.get(
                        'company',
                        ''
                    ).strip(),

                    job_title=row.get(
                        'job_title',
                        ''
                    ).strip(),

                    status=row.get(
                        'status',
                        'new'
                    ).strip() or 'new',

                    source=row.get(
                        'source',
                        'website'
                    ).strip() or 'website',

                    notes=row.get(
                        'notes',
                        ''
                    ).strip(),

                    created_by=request.user

                )


                # --------------------------------------------
                # Automatic Lead Scoring
                # --------------------------------------------

                score = 0


                rules = LeadScoreRule.objects.filter(
                    is_active=True
                )


                for rule in rules:

                    field_value = getattr(
                        lead,
                        rule.field,
                        ''
                    )


                    field_value = str(
                        field_value
                    ).strip().lower()


                    rule_value = str(
                        rule.value
                    ).strip().lower()


                    matched = False


                    # ----------------------------------------
                    # EXISTS
                    # ----------------------------------------

                    if rule.operator == 'exists':

                        matched = bool(
                            field_value
                        )


                    # ----------------------------------------
                    # CONTAINS
                    # ----------------------------------------

                    elif rule.operator == 'contains':

                        matched = (
                            rule_value
                            in field_value
                        )


                    # ----------------------------------------
                    # EQUALS
                    # ----------------------------------------

                    elif rule.operator == 'equals':

                        # "*" means any non-empty value

                        if rule_value == '*':

                            matched = bool(
                                field_value
                            )

                        else:

                            matched = (
                                field_value
                                == rule_value
                            )


                    # ----------------------------------------
                    # STARTS WITH
                    # ----------------------------------------

                    elif rule.operator == 'starts_with':

                        matched = (
                            field_value.startswith(
                                rule_value
                            )
                        )


                    # ----------------------------------------
                    # Add points
                    # ----------------------------------------

                    if matched:

                        score += rule.points


                # --------------------------------------------
                # Keep score between 0 and 100
                # --------------------------------------------

                lead.score = min(
                    score,
                    100
                )


                lead.save(
                    update_fields=[
                        'score'
                    ]
                )


                created_count += 1


            # ------------------------------------------------
            # Success Message
            # ------------------------------------------------

            messages.success(

                request,

                f'{created_count} leads imported successfully. '
                f'{skipped_count} leads skipped.'

            )


        except Exception as e:

            messages.error(

                request,

                f'Error importing CSV: {e}'

            )


        return redirect(
            'lead_list'
        )


    return render(
        request,
        'leads/import_leads.html'
    )

# ============================================================
# LEAD SCORE RULE LIST
# ADMIN / MANAGER ONLY
# ============================================================

@login_required
@manager_required
def score_rule_list(request):

    rules = LeadScoreRule.objects.all().order_by(
        '-points',
        'name'
    )

    return render(
        request,
        'leads/score_rule_list.html',
        {
            'rules': rules
        }
    )


# ============================================================
# DELETE LEAD SCORE RULE
# ADMIN / MANAGER ONLY
# ============================================================

@login_required
@manager_required
def score_rule_delete(request, pk):

    rule = get_object_or_404(
        LeadScoreRule,
        pk=pk
    )

    if request.method == 'POST':

        rule.delete()

        messages.success(
            request,
            'Lead score rule deleted successfully.'
        )

        return redirect(
            'score_rule_list'
        )

    return render(
        request,
        'leads/score_rule_delete.html',
        {
            'rule': rule
        }
    )


