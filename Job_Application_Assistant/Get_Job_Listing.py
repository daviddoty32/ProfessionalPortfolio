import yake
import pandas
import bs4
import requests
import time
import random

''' Function for getting the job listings. The variables are the job query (i.e. data science, software development, etc.),
city, state, radius away from that city, and the job_level (entry level, senior, etc)
We're gonna be using some web scraping from Indeed.com
'''


def get_linkedIn_job_listings(job_query, city, state, radius, job_level):
    counter = 0
    name_list = []
    company_list = []
    clr_keyword_list = []
    href_list = []

    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 2

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size,
                                                dedupLim=deduplication_threshold,
                                                top=numOfKeywords, features=None)
    while (counter < 1000):
        try:
            '''Setting up YAKE to get keywords from job details.'''

            '''Doing the initial scrape to 1. get the listings and 2. set up the eventual dict for the dataframe'''
            '''Note that I will eventually need to make this url configurable'''

            # job_query = job_query.replace(' ', '$20')
            # city = city.replace(' ', '$20')
            url = f'https://www.linkedin.com/jobs/search?keywords={job_query}&location={city}%2C%20Texas%2C%20' \
                  f'United%20States&locationId=&geoId=102600341&f_TPR=&distance=25&f_E=2&position=1&pageNum=0' \
                  f'&start={counter}'
            print(url)
            request = requests.get(url)
            print(request.status_code)
            soup = bs4.BeautifulSoup(request.content, 'html.parser')
            try:
                soup = soup.find('ul', {'class': 'jobs-search__results-list'}).findAll('li')
            except:
                continue
            if len(soup) < 1:
                break

            keywords = []
        except TypeError:
            print('Something broke, starting get_linkedIn_job_listings again')
            return get_linkedIn_job_listings(job_query, city, state, radius, job_level)

        for i in soup:
            try:
                counter += 1
                time.sleep(3 + random.random())
                i_url = i.find('a')['href']
                print(i_url)
                i_request = requests.get(i_url)
                new_soup = bs4.BeautifulSoup(i_request.content, 'html.parser')
                name = i.find('h3', {'class': 'base-search-card__title'}).text.strip()
                company = i.find('h4', {'class': 'base-search-card__subtitle'}).text.strip()
                new_soup = new_soup.find('div', {'class': 'decorated-job-posting__details'})
                if company is None or name is None or i_url is None:
                    print('company is None')
                    continue
                ul = new_soup.findAll('li')
                keywords = []
                for i in ul:
                    keywords_list = custom_kw_extractor.extract_keywords(i.text)
                    keys = pandas.DataFrame(keywords_list, columns=['word', 'score'])
                    for index, word in keys.iterrows():
                        keywords.append(word['word'])
                    del keys
                clr_keyword_list.append(', '.join(keywords))
                company_list.append(company)
                name_list.append(name)
                href_list.append(i_url)
                print([len(name_list), len(clr_keyword_list), len(company_list), len(href_list)])


            except AttributeError:
                print('This listing is busted, moving on')
                pass
            except TypeError:
                print('This listing is busted, moving on')
                pass

    output = []
    for x in clr_keyword_list:
        output.append(x)
    dict = {'name': name_list, 'company': company_list, 'keywords': output, 'href': href_list}
    df = pandas.DataFrame(dict)
    print(df)
    return df

def get_LinkedIn_job_listing_singular(url):
    name_list = []
    company_list = []
    clr_keyword_list = []
    href_list = []

    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 2

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size,
                                                dedupLim=deduplication_threshold,
                                                top=numOfKeywords, features=None)

    print(url)
    i_request = requests.get(url)
    new_soup = bs4.BeautifulSoup(i_request.text, 'html.parser')
    name = new_soup.find('h1', {'class': 'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title'}).text.strip()
    company = new_soup.find('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'}).text.strip()
    print(name, company)
    new_soup = new_soup.find('body').find('div', {'class': 'decorated-job-posting__details'})

    ul = new_soup.findAll('li')
    keywords = []
    for i in ul:
        keywords_list = custom_kw_extractor.extract_keywords(i.text)
        keys = pandas.DataFrame(keywords_list, columns=['word', 'score'])
        for index, word in keys.iterrows():
            keywords.append(word['word'])
        del keys
    clr_keyword_list.append(', '.join(keywords))
    company_list.append(company)
    name_list.append(name)
    href_list.append(url)
    print([len(name_list), len(clr_keyword_list), len(company_list), len(href_list)])


    output = []
    for x in clr_keyword_list:
        output.append(x)
    dict = {'name': name_list, 'company': company_list, 'keywords': output, 'href': href_list}
    df = pandas.DataFrame(dict)
    print(df)
    return df