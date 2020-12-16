from django.shortcuts import render


def index(request):
    # return
    return render(request, 'news/index.html', {'page_obj': None})

#
# def test(request):
#     objects = ['join1', 'paul2', 'georgy3', 'ringo4', 'join5', 'paul6', 'georgy7']
#     paginator = Paginator(objects, 2)
#     page_num = request.GET.get('page', 1)
#     page_objects = paginator.get_page(page_num)
#     return render(request, 'news/test.html', {'page_obj': page_objects})
