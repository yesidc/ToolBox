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