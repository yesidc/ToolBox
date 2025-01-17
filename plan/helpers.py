from tbcore.models import Plan, PlanCategoryOnlineIdea, Category, OnlineIdea
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
import re





def category_done(curret_user_plan):
    """
    Returns the categories for which a user has already selected an idea.
    Args:
        value: a user's plan
    """
    # categories/blocks for which the user has already selected an idea
    plan_category = set()
    # iterates over the PlanCategoryOnlineIdea instances
    for p in curret_user_plan.plan_category_onlide_idea_plan.all():
        # category name
        plan_category.add(p.category.category_url)
    return plan_category


def is_ajax(request):
    """
    Checks if request == ajax request.
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def context_summary(user, current_plan, checklist=True):
    """
    Summarizes user's progress
    Args:
        user: current log-in user
        current_plan: plan user is currently working on.
    Returns:
        category_idea_checklist: List whose elements are tuples with the following structure:  [('teaching-material', [(...), (...), (...)]),]), ('human-touch', [...])]
        (category_name, ([idea_name, pcoi_instance_id,pcoi_instance_note,pcoi_instance_complexity],...))
       
        category_done_summary: Set containing categories for which the user has selected at least one idea.
    """
    # all pcoi objects related to a current logged user and a current plan
    pcoi = PlanCategoryOnlineIdea.objects.get_pcoi(user, current_plan)

    category_idea_checklist = []
    info_idea = []
    if checklist:
        category_done_summary = current_plan.category_done(mode='category_name')
    else:
        category_done_summary = current_plan.category_done(mode='url')

    for c in category_done_summary:
        # all these pcoi objects are related to a single category for which user already chose at least one idea
        if checklist:
            query_category = pcoi.filter(category__category_name=c)
        else:
            query_category = pcoi.filter(category__category_url=c)

        for pcoi_instance in query_category:
            idea_name = pcoi_instance.idea.idea_name
            if checklist:
                # this id used to delete the pcoi object from checklist page
                pcoi_instance_id = pcoi_instance.pk
                pcoi_instance_note = pcoi_instance.notes
                pcoi_instance_complexity = pcoi_instance.idea.task_complexity
                info_idea.append((idea_name, pcoi_instance_id, pcoi_instance_note, pcoi_instance_complexity))
            else:
                info_idea.append(idea_name)

        category_idea_checklist.append((c, info_idea))
        info_idea = []
    return category_idea_checklist, category_done_summary


def get_ideas(user, category_url, current_user_plan_id):
    """
    Fetches all ideas that belong to a particular user, plan and category from PlanCategoryOnlineIdea object.
    """

    if user.is_anonymous or current_user_plan_id is None:
        return None
    else:
        idea_list = [i.idea.id for i in PlanCategoryOnlineIdea.objects.filter(
            Q(plan__user=user) & Q(plan__pk=current_user_plan_id) & Q(
                category__category_url=category_url))]
        return idea_list


def has_plan(request):
    """
    Checks if user has already created a plan.
    Returns: returns false is user has not added any plans yet.
    """
    if not Plan.objects.select_related('user').filter(user=request.user).exists():
        messages.add_message(request, messages.INFO, 'First create a plan to be able to save your progress.')
        return False
    else:
        return True


def save_pcoi(request, current_user_plan, current_category, current_idea):
    """
    Create PlanCategoryOnlineIdea instance.
    """

    # prevents user from saving the same ideas twice for the same course plan.
    try:
        PlanCategoryOnlineIdea.objects.create(
            plan=Plan.objects.get(pk=current_user_plan),
            category=Category.objects.get(category_url=current_category),
            idea=OnlineIdea.objects.get(pk=current_idea),

        )
        return True


    except IntegrityError:

        return False
