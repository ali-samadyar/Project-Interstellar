from django.shortcuts import render
from .bgpchecker import bgp_get_response

def bgp_checker(request):
    if request.method == 'POST':
        asn_input = request.POST.get('asn_input')
        result = bgp_get_response(asn_input)

        if result:
            context = {'result': result}
        else:
            context = {'error': 'AS Number not found'}

        return render(request, 'bgp.html', context)

    return render(request, 'bgp.html')