import requests
from bs4 import BeautifulSoup
import re
import threading
import queue
import time
def leetcode(name):
    data = dict()
    url = f'https://leetcode.com/{name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        questions_solves = soup.find('div', {'class':'text-[24px] font-medium text-label-1 dark:text-dark-label-1'})
        data['lc_questions_solved'] = questions_solves.text
        rank = soup.find('span', {'class':'ttext-label-1 dark:text-dark-label-1 font-medium'})
        data['lc_rank'] = rank.text
        questions = soup.find_all('span', attrs={'class':'mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1'})
        data['easy'] = questions[0].text
        data['medium'] = questions[1].text
        data['hard'] = questions[2].text
        contest_rating = soup.find('div', attrs={'class':'text-label-1 dark:text-dark-label-1 flex items-center text-2xl'})
        data['lc_contest_rating'] = contest_rating.text
    except:
        None
    return data

def gfg(name):
    data = dict()
    url = f'https://auth.geeksforgeeks.org/user/{name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')    
    try:
        questions_solved = soup.find_all('span',{'class':'score_card_value'})[1].text
        data['gfg_questions_solved'] = questions_solved
        questions_list = soup.find('ul', {'class':'tabs tabs-fixed-width linksTypeProblem'})
        if questions_list:
            for cat in questions_list.find_all('li'):
                for t in ['SCHOOL', 'BASIC', 'EASY', 'MEDIUM', 'HARD']:
                    if t in cat.text:
                        match = re.search(r'\((\d+)\)', cat.text)
                        num =  int(match.group(1))
                        data[t] = num 
                        break
    except:
        None
    return data

def codechef(name):
    data = dict()
    url = f"https://www.codechef.com/users/{name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')    
    try:
        rating = soup.find('div', attrs={'class':'rating-number'}).text
        star_section = soup.find('div', attrs={'class':'rating-star'})
        stars = len(star_section.find_all('span'))
        data['rating'] = rating
        data['stars'] = stars
        rating_header = soup.find('div', attrs={'class':'rating-header text-center'})
        highest_rating_tag = rating_header.find('small').text
        highest_rating = int(highest_rating_tag.split(' ')[2][:-1])
        data['highest_rating'] = highest_rating
        rating_ranks_tag = soup.find('div', attrs={'class':'rating-ranks'})
        rating_ranks_list = rating_ranks_tag.find_all('li')
        # print(rating_ranks_list)
        global_rank = int(rating_ranks_list[0].find('a').text)
        country_rank = int(rating_ranks_list[1].find('a').text)
        data['global_rank'] = global_rank
        data['country_rank'] = country_rank
    except:
        pass
    
    return data
        

def codeforces(name):
    data = dict()
    url = f"https://codeforces.com/profile/{name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')    
    try:
        info_tab = soup.find('div', attrs={'class':'info'})
        li_tags = info_tab.find_all('li')
        rating = None
        highest_rating = None 
        for li in li_tags:
            if 'Contest rating' in li.text:
                rating = int(li.find('span',{'class':'user-gray'}).text)
                data['rating'] = rating
                spans = li.find('span', {'class':'smaller'})
                highest_rating = int(spans.find_all('span')[1].text)
                data['highest_rating'] = highest_rating
        problems_sections_tab = soup.find('div', attrs={'class':'_UserActivityFrame_footer'})
        row1, row2 = problems_sections_tab.find_all('div', attrs={'class':'_UserActivityFrame_countersRow'})
        problems_solved = None
        last_year = None
        last_month = None 
        in_row = None
        data1 = row1.find_all('div', {'class':'_UserActivityFrame_counter'})
        problems_solved_tag = data1[0].find('div', {'class':'_UserActivityFrame_counterValue'})
        problems_solved = int(problems_solved_tag.text.split()[0])
        data['problems_solved'] = problems_solved
        last_year_tag = data1[1].find('div', {'class':'_UserActivityFrame_counterValue'})
        last_year = int(last_year_tag.text.split()[0])
        data['last_year'] = last_year
        last_month_tag = data1[2].find('div', {'class':'_UserActivityFrame_counterValue'})
        last_month = int(last_month_tag.text.split()[0])
        data['last_month'] = last_month
        data2 = row2.find_all('div', {'class':'_UserActivityFrame_counter'})
        in_row_tag = data2[0].find('div', {'class':'_UserActivityFrame_counterValue'})
        in_row = int(in_row_tag.text.split()[0])
        data['in_row'] = in_row
    except:
        pass    
    
    return data

