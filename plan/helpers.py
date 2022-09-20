from tbcore.models import PlanCategoryOnlineIdea, CategoryOnlineIdea
from django.db.models import Q

# todo DELETE FUNCTION, function implemented as class method. take a look at the Plan's model
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


def context_summary(user, current_plan):
    """
    Summarizes user's progress
    Args:
        user: current log-in user
        current_plan: plan user is currently working on.
    Returns:
        category_idea_checklist: List whose elements are tuples with the following structure: (category_name, [idea_name, pcoi_instance_id])
        category_done_summary: Set containing categories for which the user has selected at least one idea.
    """
    pcoi = PlanCategoryOnlineIdea.objects.get_pcoi(user, current_plan)
    category_idea_checklist = []
    info_idea = []
    category_done_summary = current_plan.category_done(mode='category_name')

    for c in category_done_summary:
        # all these pcoi objects are related to a single category for which user already chose at least one idea

        query_category= pcoi.filter(category__category_name=c)
        for pcoi_instance in query_category:
            idea_name = pcoi_instance.idea.idea_name
            # this id used to delete the pcoi object from checklist page
            pcoi_instance_id = pcoi_instance.pk
            info_idea.append((idea_name, pcoi_instance_id))

        category_idea_checklist.append((c, info_idea))
        info_idea=[]
    return category_idea_checklist, category_done_summary


def get_category(category_url):
    """
    Fetches the CategoryOnlineIdea objects
    """
    # There are a total of eight building blocks hence 8 CategoryOnlineIdea objects.
    return CategoryOnlineIdea.objects.get(category__category_url=category_url)

def get_ideas(user, category_url, current_user_plan_id):
    """
    Fetches all ideas that belong to a particular user, plan and category from PlanCategoryOnlineIdea object.
    """

    if user.is_anonymous:
        return None
    else:
        idea_list = [i.idea.id for i in PlanCategoryOnlineIdea.objects.filter(
            Q(plan__user=user) & Q(plan__pk=current_user_plan_id) & Q(
                category__category_url=category_url))]
        return idea_list