from IPython.display import Audio
import reportlab
from reportlab.pdfgen import canvas
from jinja2 import Template
import json
import pdfkit 

# Define the sample input data
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
data = load_data()
# Load the template
with open("template.html", "r") as file:
    template = Template(file.read())

# Render the template with the sample input data
html = template.render(data=data)

# Write the HTML code to a file
with open("resume_output.html", "w") as file:
    file.write(html)

# Create a canvas object to generate the PDF
c = canvas.Canvas("resume_output.pdf")

# Load the HTML file and draw it on the canvas
c.drawString(72, 720, html)

# Save the PDF
c.save()

import pdfkit 
wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")  #by using configuration you can add path value.
pdfkit.from_file('resume_output.html', 'output.pdf', configuration = wkhtml_path)
#pdfkit.from_url('https://stackoverflow.com/questions/33705368/unable-to-find-wkhtmltopdf-on-this-system-the-report-will-be-shown-in-html', 'C:/Users/Admin/Desktop/Trial1.pdf', configuration = wkhtml_path)
