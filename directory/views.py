"""
"""
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from utils.alphapaginator import AlphaPaginator
from directory.models import Business, Category
from directory.forms import BusinessForm

def manager_by(show_by):
    if show_by.lower() in ("business", "businesses"):
        return Business.approved
    elif show_by.lower() in ("category", "categories"):
        return Category.objects
    else:
        raise Http404("show by type '%s' not found" % show_by)

def show_list(request, show_by="businesses", page=1, page_size=10):
    manager = manager_by(show_by)
    data = manager.all()
    
    pages = AlphaPaginator(data, page_size)
    data_page = pages.page(page)
    
    context = {'show_by': show_by,
               'paginator': pages,
               'data': data_page.object_list}
    if data_page.next_page_number() <= pages.num_pages:
        context['next_page'] = data_page.next_page_number()
    if data_page.previous_page_number() > 0:
        context['prev_page'] = data_page.previous_page_number()
    
    return render_to_response('directory/list.html', context,
                              context_instance=RequestContext(request))

def show_detail(request, show_by="business", name=""):
    type = ""
    obj = None
    if (show_by == "business"):
        obj = Business.objects.get(name=name)
        type = "biz"
    elif (show_by == "category"):
        obj = Category.objects.get(name=name)
        type = "cat"

    return render_to_response('directory/%s.html' % type, {type: obj, 'show_by': show_by},
                              context_instance=RequestContext(request))

def register(request):
    """
    Registration form view
    """
    biz_form = BusinessForm(request.POST)
    if request.method == 'POST':
        if 'owners-add' in request.POST:
            biz_form.formsets['owners'].extra += 1
            biz_form.formsets['owners']._construct_forms()
        else:
            if biz_form.is_valid():
                biz_form.save()
                return HttpResponseRedirect(reverse('splash'))
    else:
        biz_form = BusinessForm()
    return render_to_response('directory/register.html', 
                              {'biz_form': biz_form}, 
                              context_instance=RequestContext(request))

