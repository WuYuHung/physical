from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from doctor.forms import HomeForm
from datetime import datetime

# def index(request):
#     if request.user.is_authenticated and request.user.has_perm("doctor.doctor"):
#         return render(request, "doctor.html", {})
#     else:
#         return redirect("/patient/")


class HomeView(TemplateView):  
  template_name = 'doctor.html'  

  def get(self, request):    
    form = HomeForm()    
    return render( request, self.template_name, {'form':form})  

  def post(self, request):
    form = HomeForm(request.POST)    
    if form.is_valid():
      instance = form.save(commit=False)
      instance.start_time = datetime.now()     
      instance.doctor = "123" 
      instance.save()   # Add   
    #   text = form.cleaned_data['post']      
      form = HomeForm()      
      return redirect('/doctor')  # Add   
    return render(request, self.template_name, {'form':form})