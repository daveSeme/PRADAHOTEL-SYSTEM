from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.forms import ModelForm
from django.db import models





    # Create the PDF object, using the appropriate page size and orientation
c = canvas.Canvas("receipt.pdf", pagesize=landscape(letter))

c.setTitle("Prada Hotels")

  
    # Save the PDF file
c.save()

