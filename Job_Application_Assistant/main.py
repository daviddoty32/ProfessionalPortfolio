import os
from Generate_Documents import create_resume
from Generate_Documents import create_cover_letter
from Get_Job_Listing import get_linkedIn_job_listings, get_LinkedIn_job_listing_singular
import re


def main(url):
    my_skills = ['Ad-hoc Data Analysis', 'ETL', 'Data Visualization', 'Object-Oriented Programming',
                 'Python, SQL, and R', 'Database concepts', 'Business Intelligence', 'TensorFlow',
                 'Tableau and PowerBI', 'Jupityr Notebooks', 'Time-series/Multivariate analysis',
                 'Big Data Strategy']

    '''Degree, Degree recieved, major, Year start, year finished, University, descriptors (list) '''
    my_education = [['B.S.', 'Physics', 'August 2017', 'May 2021', 'Texas A&M University',
                     ['Learned complex mathematics and statistics',
                      'Developed basic programming skills that I use in my career']],
                    ['M.S', 'Data Science', 'May 2023', 'Present', 'Texas Tech University', [
                        'Studied advanced mathematical analysis and data-driven decisioning',
                        'Studied big data strategies and industry standards',
                        'Gained hands-on experience in analytical technologies and machine learning'
                    ]],
                    ['M.B.A.', 'General Business', 'January 2022', 'Present', 'Texas Tech University',
                     ['Learned about essential business processes, and how to evaluate business metrics',
                      'Expanded my knowledge of statistics to business-centric applications',
                      'Familiarized myself with business analysis frameworks such as SWOT and Five Forces']]]

    my_experience = [['Software Developer', 'General Motors', 'July 2021 - Present', [
        'Performed ad-hoc data analytics on key business metrics', 'Developed ETL pipelines using Apache Spark',
        'Drove innovation around the use of machine learning and AI'
    ]]]

    my_name = 'David Doty'
    my_number = ''
    my_email = ''


    # So you'll see me use this in multiple different files. This is for MY computer. Change it for yours.
    parent_path = os.getcwd()
    locations = ['Spring', 'The Woodlands', 'Houston', 'Conroe', 'Remote']
    locations = ['remote']
    job_queries = ['Data Science', 'Data Analyst', 'Software Developer', 'Data Engineer', 'Game Developer']

    for city in locations:
        for job_query in job_queries:
            if(url == None):
                df = get_linkedIn_job_listings(job_query, city, 'TX', 'ENTRY_LEVEL', 35)
                job_queries = ['Data Science', 'Data Analyst', 'Software Developer', 'Data Engineer', 'Game Developer']
            else:
                df = get_LinkedIn_job_listing_singular(url)

            try:
                if(url == None):
                    df.loc[df[['name', 'company']].drop_duplicates().index].to_csv(
                        f'{job_query.replace(" ", "_")}{city.replace(" ", "_")}JobListingAndCoverLetters.csv')
            except AttributeError:
                continue

            for index, row in df.iterrows():
                company = row['company']
                name = row['name']
                filename = re.sub(r'\W+', '', name)
                if os.path.isfile(f'{parent_path}\\{company}\\{filename}_cover_letter.pdf') is False:
                    # cover_letter = row['cover_letters']
                    keywords = row['keywords']

                    create_cover_letter(company, name, keywords, my_name, my_skills, my_experience,
                                        my_number, my_education, my_email)
                    create_resume(my_name, company, my_email, my_number,
                                  my_education, my_experience, my_skills, keywords, name)
                else:
                    print(f'{parent_path}/{company}/{filename} files Already exists')


main(None)

