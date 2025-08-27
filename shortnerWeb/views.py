from django.shortcuts import render

# Create your views here.
def main_page(request):
    """Main page view for the URL shortener"""
    return render(request, 'shortner/main.html')
