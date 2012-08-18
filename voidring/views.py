from django.shortcuts import render_to_response

def home(request):

    var_ejemplo = 'cualquier cosa'
    return render_to_response('index.html', {'var_ejemplo': var_ejemplo})
