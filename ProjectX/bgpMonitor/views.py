from django.shortcuts import render
from .bgpchecker import bgp_get_response
from .models import BGPCheckResult


def bgp_checker(request):
    context = {} 

    if request.method == 'POST':
        asn_input = request.POST.get('asn_input')
        result = bgp_get_response(asn_input)

        if result:
            # Check if an entry with the same ASN exists
            existing_entry = BGPCheckResult.objects.filter(as_number=result.get('as_number', '')).first()

            if existing_entry:
                # Update the existing entry
                existing_entry.as_name = result.get('as_name', '')
                existing_entry.source = result.get('source', '')
                existing_entry.longitude = result.get('longitude', 0.0)
                existing_entry.latitude = result.get('latitude', 0.0)
                existing_entry.country = result.get('country', '')
                existing_entry.save()
            else:
                # Create a new entry
                bgp_result = BGPCheckResult(
                    as_number=result.get('as_number', ''),
                    as_name=result.get('as_name', ''),
                    source=result.get('source', ''),
                    longitude=result.get('longitude', 0.0),
                    latitude=result.get('latitude', 0.0),
                    country=result.get('country', ''),
                )
                bgp_result.save()

            context = {'result': result}
        else:
            context = {'error': 'AS Number not found'}

    # Retrieve data from the database
    saved_results = BGPCheckResult.objects.all()
    context['saved_results'] = saved_results

    return render(request, 'bgp.html', context)
