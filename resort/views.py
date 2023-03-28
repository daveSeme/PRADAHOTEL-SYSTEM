from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Rooms, Availability, Booking
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Booking

from django.contrib import messages
from .models import Profile, CustomUser
from .forms import ProfileForm, CustomUserForm

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
@login_required(login_url="user")
def  home(request):
       return render(request, 'index.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        # Get form data
        form=CustomUserForm(request.POST)
        # Create user
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            user1= authenticate(username=username, password=password1)
            if user1:
                login(request, user1)
                return redirect('home')
         
        else:
            messages.error(request, 'Password should be more than 8 characters.')
            return redirect('register')

        # Log in user
        
    else:
        form=CustomUserForm()

        return render(request, 'signup.html', {'form':form})







def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile successfully created')
            return redirect('home')
        else:
            messages.error(request, 'There was an error creating your profile. Please try again.')
    else:
        form = ProfileForm()
    
    context = {'form': form }
    return render(request, 'create_profile.html', context)



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user')

       
def  rooms(request):
       if request.method=='POST':
              checkin=request.POST['checkin']
              checkout=request.POST['checkout']
              type=request.POST['type']
              persons=request.POST['persons']
              return redirect(f'room_available/{type}')
       else:
              return render(request, 'rooms.html')

def  restaurant(request):
      
       return render(request, 'restaurant.html')

def  about(request):
       return render(request, 'about.html')

def  contact(request):
       return render(request, 'contact.html')


def  booking(request, pk):
       obj=Rooms.objects.get(id=pk)
       if request.method == "POST":
              checkin=request.POST['checkin']
              checkout=request.POST['checkout']
              persons=request.POST['guests']
              name=get_object_or_404(CustomUser, username=request.user.username)

              data=Booking.objects.create(
                    room=obj,
                    checkin=checkin,
                    checkout=checkout,
                    numberguests=persons,
                    name=name,
                    
              )
              data.save()
              obj.is_available=False
              obj.save()
              generate_receipt(pk)
              return redirect('bookings')
       else:
              return render(request, 'booking.html')
       


def booking_history(request):
    name=get_object_or_404(CustomUser, username=request.user.username)
    bookings = Booking.objects.filter(name=name)
    return render(request, 'booking_history.html', {'bookings': bookings})


def  room_available(request, type):
       obj=Availability.objects.filter(room_type=type).first()
       obj1=Rooms.objects.filter(room_type=obj, is_available=True).all()
       return render(request, 'roomsavailable.html',{"rooms":obj1})


def user(request):
       if request.method =='POST':
              username=request.POST['name']
              password=request.POST['password']
              user= authenticate(username=username, password=password)
              if user:
                     login(request, user)
                     return redirect("home")
              else:
                     return redirect("user")
       else:
              return render(request, 'user.html')



def create(number, type, price):
       for i in range(number):
              obj=get_object_or_404(Availability, room_type=f"{type}")
              obj1 = Rooms(room_type=obj, price=price, max_person=1, beds=1)
              obj1.save()

def log_out(request):
    logout(request)
    return redirect("user")





def generate_receipt(room_id):
    # Get the booking object from the database
    room = Rooms.objects.get(id=room_id)
    booking = Booking.objects.filter(room=room).first()

    doc = SimpleDocTemplate("receipt.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    style_center = ParagraphStyle(
        name='center',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        wordWrap='CJK'
    )

    data = [
        ["Name", "Checkin Date", "Checkout Date", "Amount", "No of Nights", "Total Amount"],
        [booking.name, str(booking.checkin), str(booking.checkout), str(booking.room.price), str((booking.checkout - booking.checkin).days), str((booking.checkout - booking.checkin).days * booking.room.price)]
    ]

    # set row heights based on the content
    rowHeights = [1.4*inch] # set the height of the first row to be larger
    for i in range(1, len(data)):
        rowHeights.append(max([len(str(d)) for d in data[i]]) * 0.25*inch)

    table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch], rowHeights=0.4*inch)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements = []
    elements.append(Paragraph("Prada Hotels Receipt", style_center))
    elements.append(table)

    doc.build(elements)
    with open("receipt.pdf", 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="receipt.pdf"'
        return response
