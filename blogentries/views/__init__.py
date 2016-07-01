from django.http import HttpResponseServerError
import traceback

def handle_500_error(request):
    print traceback.format_exc()
    return HttpResponseServerError("Server Error occured. Please contact the administrator.")
