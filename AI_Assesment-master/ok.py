from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

class VolkswagenModel:
    # Define a list of models for validation
    list_of_models = ["181", "Amarok", "Arteon", "Atlas", "Beetle", "Bora", "Buggy", "Caddy", "California", 
                      "Caravelle", "CC", "Corrado", "Crafter", "Eos", "Fox", "Garbus", "Golf", "Golf Plus", 
                      "Golf Sportsvan", "ID.3", "ID.4", "ID.5", "ID.6", "ID.Buzz", "Iltis", "Jetta", "Kafer", 
                      "Karmann Ghia", "LT", "Lupo", "Multivan", "New Beetle", "Passat", "Passat CC", "Phaeton", 
                      "Polo", "Routan", "Santana", "Scirocco", "Sharan", "T-Cross", "T-Roc", "Taigo", "Teramont", 
                      "Tiguan", "Tiguan Allspace", "Touareg", "Touran", "Transporter", "up!", "Vento"]

    def __init__(self, price, year, mileage, capacity, fuel, model, estimation):
        self.price = price
        self.year = year
        self.mileage = mileage
        self.capacity = capacity
        self.fuel = fuel
        self.model = model
        self.estimation = estimation

    # Data cleaning function
    def clean_data(self):
        # Clean price
        self.price = self._parse_int(self.price.replace(" ", "").replace("PLN", ""))
        
        # Clean year
        self.year = self._parse_int(self.year)
        
        # Clean mileage
        self.mileage = self._parse_int(self.mileage.replace(" ", "").replace("km", ""))
        
        # Clean capacity
        self.capacity = self._parse_int(self.capacity.replace(" ", "").replace("cm3", ""))
        
        # Map fuel type to integer codes
        fuel_mapping = {"Benzyna": 1, "Benzyna+LPG": 2, "Benzyna+CNG": 3, 
                        "Elektryczny": 4, "Hybryda": 5, "Wodór": 6, "Diesel": 7}
        self.fuel = fuel_mapping.get(self.fuel.replace(" ", ""), 0)
        
        # Map model to an integer index if it matches a known model
        self.model = next((i for i, m in enumerate(self.list_of_models) if m in self.model), '-')
        
        # Map estimation to integer codes
        estimation_mapping = {"Poniżej średniej": 1, "W granicach średniej": 2, "Powyżej średniej": 3}
        self.estimation = estimation_mapping.get(self.estimation, 0)

    def _parse_int(self, value):
        try:
            return int(value)
        except ValueError:
            return '-'

    def return_data(self):
        return [self.price, self.year, self.mileage, self.capacity, self.fuel, self.model, self.estimation]

# Initialize data storage
data = []

# Web scraping loop
for page_number in range(1, 563):
    url = f"https://www.otomoto.pl/osobowe/volkswagen?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find article elements
    articles = soup.find_all('article', attrs={'class': 'ooa-1g2kumr eayvfn60'})
    if not articles:
        articles = soup.find_all('article', attrs={'class': 'ooa-1rudse5 eayvfn60'})

    for article in articles:
        # Extract relevant information
        price = article.find('span', class_='ooa-1bmnxg7 eayvfn611')
        rest = article.find_all('li', class_='ooa-1k7nwcr e19ivbs0')
        model = article.find_all('a')
        estimation = article.find('p', class_='e1xj1nw30 ooa-ixk3xj er34gjf0')

        # Handle missing data
        if not price or not rest or len(rest) < 5 or not model:
            continue

        # Initialize VolkswagenModel instance
        if rest[0].text == 'Niski przebieg' and not estimation:
            row = VolkswagenModel(price.text, rest[1].text, rest[2].text, rest[3].text, rest[4].text, model[0].text, '-')
        elif rest[0].text != 'Niski przebieg' and not estimation:
            row = VolkswagenModel(price.text, rest[0].text, rest[1].text, rest[2].text, rest[3].text, model[0].text, '-')
        elif rest[0].text == 'Niski przebieg' and estimation:
            row = VolkswagenModel(price.text, rest[1].text, rest[2].text, rest[3].text, rest[4].text, model[0].text, estimation.text)
        else:
            row = VolkswagenModel(price.text, rest[0].text, rest[1].text, rest[2].text, rest[3].text, model[0].text, estimation.text)
        
        # Clean and add data
        row.clean_data()
        data.append(row.return_data())
    
    # Pause to avoid overwhelming the server


# Create DataFrame
df = pd.DataFrame(data, columns=['Price', 'Year', 'Mileage', 'Tank capacity', 'Fuel type', 'Model', 'Estimation'])

# Remove rows with missing data
df = df[(df[['Price', 'Year', 'Mileage', 'Tank capacity', 'Model']] != '-').all(axis=1)]

# Save to CSV
df.to_csv('./AI_UniClasses_Assesment/data/otomoto.csv', index=False)
print(df.head())
