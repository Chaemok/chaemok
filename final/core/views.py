from django.shortcuts import redirect

def theme_toggle(request):
    cur = request.session.get("theme", "dark")
    request.session["theme"] = "light" if cur == "dark" else "dark"
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)
