from docx import Document
from docx.shared import RGBColor, Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
 
class ResumeTemplate:
    def CreateResume(self,data):

        # Create a new word document
        document = Document()
        section = document.sections[0]
        section.left_margin = Inches(0.5) # set left margin to 0.5 inch
        section.right_margin = Inches(0.5) # set left margin to 0.5 inch
        section.page_height = Inches(11.0) # set page height to 11 inches
        section.page_width = Inches(8.5) # set page width to 8.5 inches
        section.header_distance = Inches(0.5) # set header distance to 0.5 inches

        # Add a heading to the document with custom font and size
        header = document.add_heading(data['Name'], 0)
        header.style.font.name = 'Arial'
        header.style.font.size = Pt(16)
        header.style.font.color.rgb = RGBColor(0, 0, 0)

        # Add your name, address, contact information with custom font and size
        document.add_paragraph(data['Address'] + '| ' + data['Email'] + '| ' + data['Phone'] + '| ' + data['LinkedIn'], style='Normal').style.font.name = 'Arial'


        # Add a section for your objective
        document.add_heading('Objective', level=1)
        document.add_paragraph(data['Objective'], style='Normal').style.font.name = 'Arial'


        # Add a section for your work experience
        document.add_heading('Work Experience', level=1)
        # Add your work experience, job title, and duration as bullet points
        experiences = data['experiences']
        
        for exp in experiences:          
            p = document.add_paragraph(style='List Bullet')
            p.add_run(exp['company'] + ', ').bold = True
            p.add_run(exp['title'] + ', ').bold = True
            p.add_run(exp['duration']).italic = True
            p = document.add_paragraph(style='List Bullet 2')
            p.add_run(exp['description']).italic = True

        # Add a section for your education
        document.add_heading('Education', level=1)
        education = data["education"]
        for edu in education:
            school = edu["school"]
            degree = edu["degree"]
            start_date = edu["start_date"]
            end_date = edu["end_date"]
            city = edu["city"]
            description = edu["description"]

            p = document.add_paragraph( )
            p.add_run(school).bold = True
            p.add_run('\n' + degree).bold = True
            p.add_run('\n').alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.add_run('\n' + start_date + ' - ' + end_date)
            p.add_run('\n' + city)
            p.add_run('\n' + description).italic = True
            p.add_run('\n')

        # Add a section for your technical skills
        document.add_heading('Skills', level=1)
        document.add_paragraph(data['Skills'], style='Normal').style.font.name = 'Arial'

        # Add a section for your achievements
        document.add_heading('Achievements', level=1)
        document.add_paragraph(data['Achievement'], style='Normal').style.font.name = 'Arial'




        return document

