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


def create_cover_letter_non_chatgpt(company, name, keywords, my_name, my_skills, my_experience,
                        my_number, my_education, my_email):
    parent_path = os.getcwd()
    education_list = []
    experience_list = []
    '''for job in my_experience:
        experience_list.append(f'{job[0]} at {job[1]} from {job[3]}')
    experience_list = ', '.join(experience_list)

    for degree in my_education:
        education_list.append(f'{degree[0]} in {degree[1]} from {degree[2]} to {degree[3]} at {degree[4]}')
    education_list = ', '.join(education_list)'''
    filename = re.sub(r'\W+', '', name)
    company_name= re.sub(r'\W+', '', company)

    output_file = f'{parent_path}/{company_name}/{filename}_cover_letter.pdf'
    keyword_string = ', '.join(keywords)


    text_width = 400

    # Create a PDF document
    pdf_canvas = canvas.Canvas(output_file, pagesize=letter)

    # Set font and size
    pdf_canvas.setFont("Times-Roman", 12)

    # Set the position for the content
    x_position = 75
    y_position = 700

    pdf_canvas.drawString(x_position, y_position, 'David Doty')
    y_position -= 15
    pdf_canvas.drawString(x_position, y_position, name)
    y_position -= 15
    pdf_canvas.drawString(x_position, y_position, company_name)
    y_position -= 15
    pdf_canvas.drawString(x_position, y_position, str(datetime.date.today()))
    y_position -= 30

    pdf_canvas.setFont("Times-Roman", 12)

    cover_letter = text = f'''To whom it may concern,\n
        I am writing to express my interest in the {name} position at {company}. I am a talented software developer with over two years of experience at General Motors. I am sure that my experience at General Motors, as well as my education, will make me a perfect candidate to join the {company} team.\n
        My primary focus in my position at General Motors has been the development of ETL pipelines. I specialize in using Apache Spark to pull data from our Hadoop data lake, clean it, and store it in our Oracle database.  My familiarity with the data in our system also enabled me to perform ad-hoc data analytics for our product insights team. Because of this, I gained experience using data reporting tools like PowerBI and Tableau. I am excited to see how my ETL and data analysis experience can translate to the needs of {company}.\n
        When I am not focusing on ETL at GM, I spend my time working on a variety of different tasks. I have worked extensively in SQL databases, API integrations, release pipelines, Unix/Bash scripting, and even training machine learning models. Throughout all of this, I am expected to help support the product in our production environment, so I have experience working on-call 24/7/365. My experience in that environment at General Motors has prepared me for similar fast-paced environments, and as a result, I know that I can fit right in at{company}.\n
        In addition to my experience, I have extensive education with a bachelor’s degree in physics and a master’s degree in data science that will be completed in May. My education has given me the tools that have not only made me a better developer but have provided an understanding of the ML/AI landscape that will be so vitally important in all aspects of the industry for years to come. I am eager to add my knowledge to {company}.\n
        Thank you so much for your time, and please feel free to reach out to me to further discuss this opportunity! I look forward to discussing how my skills can be a part of {company}.

    '''
    # Split the cover letter content into paragraphs
    paragraphs = cover_letter.split('\n')

    # Write each paragraph to the PDF
    for paragraph in paragraphs:
        for pg in wrap(paragraph.strip(), 120):
            pdf_canvas.drawString(x_position, y_position, pg)
            y_position -= 15  # Adjust the vertical position for the next paragraph
        y_position -= 7
    y_position -=8

    pdf_canvas.drawString(x_position, y_position, 'With Gratitude, ')
    y_position -= 67
    '''This section is for keyword stuffing. Note: may ATS programs check for keyword stuffing an intentionally filter
    out those cover letters. But hey, if you wanna try your luck, go for it.'''

    with open('Signature.png') as img:
        pdf_canvas.drawInlineImage('Signature.png',x_position,y_position, 230, 60)

    y_position -= 15
    pdf_canvas.drawString(x_position, y_position, 'David Doty')
    try:
        os.mkdir(f'{parent_path}/{company_name}')
    except FileExistsError:
        print('directory exists')
    # Save the PDF
    pdf_canvas.save()


company = 'TEST'
name = 'TEST'
keywords = ['TEST']
my_name = 'TEST'
my_skills = 'TEST'
my_experience  = 'TEST'
my_number = 'TEST'
my_education = 'TEST'
my_email = 'TEST'
create_cover_letter(company, name, keywords, my_name, my_skills, my_experience,
                        my_number, my_education, my_email)

