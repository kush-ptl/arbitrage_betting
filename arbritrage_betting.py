from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

my_url = 'https://www.rotowire.com/betting/tools/arbitrage-calculator.php'

uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'html.parser')

containers = page_soup.findAll('div', {'class':'games'})
results = []

for container in containers:
    event = container.find('div', {'class':'event__box'})
    matchup = event.find('div', {'class':'event__matchup'})
    away = matchup.find('div', {'class':'event__away'})
    away_team = away.div.div.text.strip().split()[0]
    home = matchup.find('div', {'class':'event__home'})
    home_team = home.div.div.text.strip().split()[0]

    odds = event.findAll('div', {'class':'ml'})
    greatest_pos = float('-inf')
    greatest_neg = float('-inf')
    count = 0
    for odd in odds:
        condition = odd.find('div', {'class':'event__condition'})

        if (condition != None):
            condition_team = condition.div.text.strip().split()[0]
            condition_odds = condition.div.text.strip().split()[-1]

            if (condition_odds[1] == '+'):
                curr_odd = int(condition_odds[2:-1])
                if (curr_odd > greatest_pos):
                    greatest_pos = curr_odd
            elif (condition_odds[1] == '-'):
                curr_odd = int(condition_odds[1:-1])
                if (curr_odd > greatest_neg):
                    greatest_neg = curr_odd
        count += 1
    
    if (greatest_pos > abs(greatest_neg)):
            result = [home_team, away_team, greatest_pos, greatest_neg]
            results += result

if not results:
    print("No opportunities :( Try again later!")
else:
    print(results)
print(my_url)