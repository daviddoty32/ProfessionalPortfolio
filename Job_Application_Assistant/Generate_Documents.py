import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from Get_ChatGPT_Results import get_chatGPT_results
import re


def create_cover_letter(company, name, keywords, my_name, my_skills, my_experience,
                        my_number, my_education, my_email):
    parent_path = os.getcwd()
    education_list = []
    experience_list = []
    for job in my_experience:
        experience_list.append(f'{job[0]} at {job[1]} from {job[3]}')
    experience_list = ', '.join(experience_list)

    for degree in my_education:
        education_list.append(f'{degree[0]} in {degree[1]} from {degree[2]} to {degree[3]} at {degree[4]}')
    education_list = ', '.join(education_list)
    filename = re.sub(r'\W+', '', name)
    company_name= re.sub(r'\W+', '', company)

    output_file = f'{parent_path}/{company_name}/{filename}_cover_letter.pdf'
    keyword_string = ', '.join(keywords)
    cover_letter_prompt = f'''
        My name is {my_name}.
        Write a 250 word cover letter body for a {name} job application at {company}. 
        I have the following skills: {', '.join(my_skills)}. 
        Use these keywords if they align with my skills:
        {keyword_string}. 
        My education is as Follows: {education_list}. 
        My experience is as follows:{experience_list}.
        Don't include variable fields. Start with 'To whome it may concern,' as the heading.
        My phone number is {my_number} and my email is {my_email}.
        '''

    cover_letter = get_chatGPT_results(cover_letter_prompt)
    text_width = 400

    # Create a PDF document
    pdf_canvas = canvas.Canvas(output_file, pagesize=letter)

    # Set font and size
    pdf_canvas.setFont("Times-Roman", 12)

    # Set the position for the content
    x_position = 100
    y_position = 700

    # Split the cover letter content into paragraphs
    paragraphs = cover_letter.split('\n')

    # Write each paragraph to the PDF
    for paragraph in paragraphs:
        for pg in wrap(paragraph.strip(), 75):
            pdf_canvas.drawString(x_position, y_position, pg)
            y_position -= 15  # Adjust the vertical position for the next paragraph
        y_position -= 7

    pdf_canvas.setFillColorRGB(255, 255, 255)
    y_position -= 20
    '''This section is for keyword stuffing. Note: may ATS programs check for keyword stuffing an intentionally filter
    out those cover letters. But hey, if you wanna try your luck, go for it.'''

    '''for words in wrap(', '.join(keywords), 75):
        pdf_canvas.drawRightString(x_position, y_position, words)
        y_position -= 7'''

    try:
        os.mkdir(f'{parent_path}/{company_name}')
    except FileExistsError:
        print('directory exists')
    # Save the PDF
    pdf_canvas.save()


def create_resume(name, company, email, phone, education, experience, skills, keywords, job_app_title):
    # Create a PDF document

    parent_path = os.getcwd()
    filename = re.sub(r'\W+', '', name)
    company = re.sub(r'\W+', '', company)
    output_file = f"{parent_path}/{company}/{filename}_resume.pdf"
    education_list = []
    for degree in education:
        education_list.append(f'{degree[0]} in {degree[1]}, {degree[4]}'
                              f'                    from {degree[2]} to {degree[3]}')

    pdf_canvas = canvas.Canvas(output_file, pagesize=letter)

    my_bio = f'''I am talented software developer at General Motors looking to find a position that will allow me to
    utilize my skills working with data. I love coding, analysis, and the process of working with data.'''

    # Set serif font and size
    pdf_canvas.setFont("Times-Bold", 16)

    # Add name
    pdf_canvas.drawCentredString(300, 750, name)

    # Set serif font for the rest of the content
    pdf_canvas.setFont("Times-Bold", 12)

    # Add contact information
    contact_info = f"Email: {email}"
    phone_info = f'Phone: {phone}'
    pdf_canvas.drawString(100, 730, contact_info)
    pdf_canvas.drawString(100, 715, phone_info)
    y_position = 670
    pdf_canvas.setFont("Times-Roman", 12)

    pdf_canvas.line(75, y_position + 12, 550, y_position + 12)
    for bio in wrap(my_bio, 100):
        pdf_canvas.drawCentredString(300, y_position, bio)
        y_position -= 15
    pdf_canvas.line(75, y_position + 9, 550, y_position + 9)

    y_position -= 15
    # Add education section
    pdf_canvas.setFont("Times-Bold", 14)
    pdf_canvas.drawString(100, y_position, "Education:")
    y_position -= 15
    pdf_canvas.setFont("Times-Roman", 12)
    for edu_item in education:
        pdf_canvas.drawString(120, y_position, f'{edu_item[0]} in {edu_item[1]}, {edu_item[4]}')
        pdf_canvas.drawRightString(540, y_position, f'{edu_item[2]} - {edu_item[3]}')
        y_position -= 15
        for descriptor in edu_item[5]:
            pdf_canvas.drawString(150, y_position, f'-{descriptor}')
            y_position -= 15
        y_position -= 15

    # Add experience section
    pdf_canvas.setFont("Times-Bold", 14)
    pdf_canvas.drawString(100, y_position - 15, "Experience:")
    y_position -= 30
    pdf_canvas.setFont("Times-Roman", 12)

    for exp_item in experience:

        pdf_canvas.drawString(120, y_position, f'{exp_item[0]}, {exp_item[1]}')
        pdf_canvas.drawRightString(540, y_position, f'{exp_item[2]}', )
        y_position -= 15
        for descriptor in exp_item[3]:
            pdf_canvas.drawString(150, y_position, f'-{descriptor}')
            y_position -= 15

        y_position -= 15

    # Add skills section
    pdf_canvas.setFont("Times-Bold", 14)
    pdf_canvas.drawString(100, y_position - 15, "Skills:")
    y_position -= 45
    pdf_canvas.setFont("Times-Roman", 12)

    counter = 0
    skill_string = ', '.join(skills)
    skill_query_prompt = f'''Return the 7 most relevant skills for a {job_app_title} position from the following list
    , delimited by the '|' character: {skill_string}'''
    print(skill_query_prompt)

    skill_string = get_chatGPT_results(skill_query_prompt)
    print(skill_string)
    skills = skill_string.split('|')
    print(skills)
    for skill in ['Attention to Detail', 'Superb Communication skills', 'Leadership']:
        skills.append(skill)

    for skill_item in skills:
        skill_item = skill_item.replace("\n", '')
        if counter % 2 == 0:
            pdf_canvas.drawString(120, y_position, f'-{skill_item}')
        else:
            pdf_canvas.drawString(360, y_position, f'-{skill_item}')
            y_position -= 15
        counter += 1

    keywords = ', '.join(keywords)

    pdf_canvas.setFillColorRGB(255, 255, 255)
    '''This section is for keyword stuffing. Note: may ATS programs check for keyword stuffing an intentionally filter
    out those resumes. But hey, if you wanna try your luck, go for it.'''
    '''for word in wrap(keywords, 75):
        pdf_canvas.drawString(120, y_position, word)
        y_position -= 7'''
    # Save the PDF
    try:
        os.mkdir(f'{parent_path}/{company}')
    except FileExistsError:
        print('directory exists')

    pdf_canvas.save()
