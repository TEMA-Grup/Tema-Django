def company_choices(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        qs = getattr(user, "companies", None)
        return {
            "user_companies": qs.all() if qs else [],
            "active_company_id": getattr(user, "active_company_id", None),
        }
    return {"user_companies": [], "active_company_id": None}