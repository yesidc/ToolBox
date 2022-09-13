from tbcore.models import PlanCategoryOnlineIdea


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
        list whose elements are tuples with the following structure: (category_name, [idea_name,idea_id])
    """
    pcoi = PlanCategoryOnlineIdea.objects.get_pcoi(user, current_plan)
    category_idea_checklist = []
    info_idea = []
    category_done_summary = current_plan.category_done(mode='category_name')

    for c in category_done_summary:
        # all these pcoi objects are related to a single category for which user already chose at least one idea
        # todo optimize this query
        query_category= pcoi.filter(category__category_name=c)
        for pcoi_instance in query_category:
            idea_name = pcoi_instance.idea.idea_name
            idea_id = pcoi_instance.idea.pk
            info_idea.append((idea_name, idea_id))

        category_idea_checklist.append((c, info_idea))
        info_idea=[]
    return category_idea_checklist
