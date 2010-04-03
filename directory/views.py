"""
"""
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.template import RequestContext
from django.core.urlresolvers import reverse

from directory.models import Business, Category
from directory.forms import BusinessForm

def manager_by(show_by):
    if show_by.lower() == "business":
        return Business.objects
    elif show_by.lower() == "category":
        return Category.objects
    else:
        raise Http404("show by type '%s' not found" % show_by)

def show_list(request, show_by="business", alpha="", page=1, page_size=10):
    manager = manager_by(show_by)
    
    data = manager.all()
    
    if (alpha):
        page = manager.alpha_index(alpha)/page_size+page
    
    pages = Paginator(data, page_size)    
    try: # Make sure page request is an int. If not, deliver first page.
        page = int(page)
    except ValueError:
        page = 1    
    #make sure page is a valid number
    page = min(max(page, 1), pages.num_pages) #not less than one & not greater than available pages
    data_page = pages.page(page)
    
    next_page = min(page+1, pages.num_pages)    
    if next_page <= page: next_page = None
    prev_page = max(page-1, 1)
    if prev_page >= page: prev_page = None
    
    render_args = {'show_by':show_by,
                   'data': data_page.object_list,
                   'alphabet': manager.alphabet(),
                   'next_page': next_page, 
                   'prev_page': prev_page,
                   'num_pages': pages.num_pages}
    if (alpha != ""):
        render_args['alpha'] = alpha
    return render_to_response('directory/list.html', render_args,
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

