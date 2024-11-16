from bs4 import BeautifulSoup
from preprocessing import VolkswagenModel
import pandas as pd
import requests

data = []

# Simple web scraper


for page_number in range(1, 563):
    # There is 563 pages. 

    url = f"https://www.otomoto.pl/osobowe/volkswagen?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all('article', attrs={'class': 'ooa-1g2kumr eayvfn60'})
    if len(articles) == 0: articles = soup.find_all('article', attrs={'class': 'ooa-1rudse5 eayvfn60'})

    for article in articles:
        
        price = article.find_all('span', attrs={'class': 'ooa-1bmnxg7 eayvfn611'})
        rest = article.find_all('li', attrs={'class': 'ooa-1k7nwcr e19ivbs0'})
        model = article.find_all('a')
        estimations = article.find_all('p', attrs={'class': 'e1xj1nw30 ooa-ixk3xj er34gjf0'})

        if rest[0].text == 'Niski przebieg' and len(estimations) == 0: row = VolkswagenModel(price[0].text, rest[1].text, rest[2].text, rest[3].text, rest[4].text, model[0].text, '-')
        elif rest[0].text != 'Niski przebieg' and len(estimations) == 0: row = VolkswagenModel(price[0].text, rest[0].text, rest[1].text, rest[2].text, rest[3].text, model[0].text, '-')
        elif rest[0].text == 'Niski przebieg' and len(estimations) != 0: row = VolkswagenModel(price[0].text, rest[1].text, rest[2].text, rest[3].text, rest[4].text, model[0].text, estimations[0].text)
        elif rest[0].text != 'Niski przebieg' and len(estimations) != 0: row = VolkswagenModel(price[0].text, rest[0].text, rest[1].text, rest[2].text, rest[3].text, model[0].text, estimations[0].text)
        
        row.clean_data()
        data.append(row.return_data())

df = pd.DataFrame(data)
df.columns = ['Price', 'Year', 'Mileage', 'Tank capacity', 'Fuel type', 'Model', 'Estimation']
print(df)
print(df.dtypes)

for index, row in df.iterrows():
    if row["Price"] == '-' or row["Mileage"] == '-' or row["Tank capacity"] == '-' or row["Model"] == '-': 
        df = df.drop(labels=[index], axis=0)

df.to_csv('./AI_UniClasses_Assesment/data/otomoto.csv')