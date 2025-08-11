from django.core.paginator import Paginator


def get_pagination(request, queryset):
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return page_obj
    
