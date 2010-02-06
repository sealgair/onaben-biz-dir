"""
"""
from django.forms.models import inlineformset_factory
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.template import RequestContext

from directory.models import Business, Category, Address, PhoneNumber
from directory.forms import BusinessForm

def manager_by(show_by):
    if show_by.lower() == "business":
        return Business.objects
    elif show_by.lower() == "category":
        return Category.objects
    else:
        raise Http404("show by type '%s' not found" % show_by)

def show_list(request, show_by="business", search="", alpha="", page=1, page_size=10):
    manager = manager_by(show_by)
    
    if (request.method == 'POST'):
        search = request.POST['search']
    if (search):
        data = manager.search(search)
    else:
        data = manager.all()
    
    if (alpha):
        page = manager.alpha_index(alpha, search)/page_size+page
    
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
                   'search':search,
                   'data': data_page.object_list,
                   'alphabet': manager.alphabet(),
                   'next_page': next_page, 
                   'prev_page': prev_page,
                   'num_pages': pages.num_pages}
    if (search != ""):
        render_args['search'] = search
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
    biz = Business()
    AddressFormset = inlineformset_factory(Business, Address, extra=1, can_delete=False)
    PhoneFormset = inlineformset_factory(Business, PhoneNumber, extra=1, can_delete=False)
    if request.method == 'POST':
        biz_form = BusinessForm(request.POST, instance=biz)
        addy_formset = AddressFormset(request.POST, instance=biz)
        phone_formset = PhoneFormset(request.POST, instance=biz)
        
        if biz_form.isValid() and addy_formset.isValid():
            return HttpResponseRedirect('/welcome')
    else:
        biz_form = BusinessForm(instance=biz)
        addy_formset = AddressFormset(instance=biz)
        phone_formset = PhoneFormset(instance=biz)
    return render_to_response('directory/register.html', 
                              {'biz_form':biz_form, 
                               'addy_formset':addy_formset, 
                               'phone_formset':phone_formset}, 
                              context_instance=RequestContext(request))