class VolkswagenModel(object):

    list_of_models = ["181", "Amarok", "Arteon", "Atlas", "Beetle", "Bora", "Buggy", "Caddy", "California", "Caravelle", "CC", "Corrado", "Crafter", "Eos", "Fox", "Garbus", "Golf", "Golf Plus", "Golf Sportsvan", "ID.3", "ID.4", "ID.5", "ID.6", "ID.Buzz", "Iltis", 
        "Jetta", "Kafer", "Karmann Ghia", "LT", "Lupo", "Multivan", "New Beetle", "Passat", "Passat CC", "Phaeton", "Polo", "Routan", "Santana", "Scirocco", "Sharan", "T-Cross", "T-Roc", "Taigo", "Teramont", "Tiguan", "Tiguan Allspace", "Touareg", "Touran", "Transporter", "up!", "Vento"]

    def __init__(self, price, year, mileage, capacity, fuel, model, estimation):

        self.price = price
        self.year = year
        self.mileage = mileage
        self.capacity = capacity
        self.fuel = fuel
        self.model = model
        self.estimation = estimation

    # Data cleaning
    def clean_data(self):

        # Price
        text = self.price.replace(" ", "")
        text = text.replace("PLN", "")
        try:
            self.price = int(text)
        except ValueError:
            self.price = '-'

        # Year
        try:
            self.year = int(self.year)
        except ValueError:
            self.year = '-'

        # Mileage
        text = self.mileage.replace(" ", "")
        text = text.replace("km", "")
        try:
            self.mileage = int(text)
        except ValueError:
            self.mileage = '-'

        # Fuel capacity
        text = self.capacity.replace(" ", "")
        text = text.replace("cm3", "")
        try:
            self.capacity = int(text)
        except ValueError:
            self.capacity = '-'

        # Fuel type
        # 0 -> Lack of data
        # 1 -> Petrol
        # 2 -> Petrol + LPG
        # 3 -> Petrol + CNG
        # 4 -> Electric
        # 5 -> Hybrid
        # 6 -> Hydrogen
        # 7 -> Diesel
        text = self.fuel.replace(" ", "")
        if text == "Benzyna": self.fuel = int(1)
        elif text == "Benzyna+LPG": self.fuel = int(2)
        elif text == "Benzyna+CNG": self.fuel = int(3)
        elif text == "Elektryczny": self.fuel = int(4)
        elif text == "Hybryda": self.fuel = int(5)
        elif text == "Wodór": self.fuel = int(6)
        elif text == "Diesel": self.fuel = int(7)
        else: self.fuel = int(0)

        # Model
        check = False
        for i, model in enumerate(self.list_of_models):
            if model in self.model:
                self.model = str(i)
                check = True
        if check == False: self.model = '-'
        else: self.model = int(self.model)

        # Estimation
        # 0 -> Lack of data
        # 1 -> Below average
        # 2 -> Within average
        # 3 -> Above average
        if self.estimation == "Poniżej średniej": self.estimation = int(1)
        elif self.estimation == "W granicach średniej": self.estimation = int(2)
        elif self.estimation == "Powyżej średniej": self.estimation = int(3)
        else: self.estimation = int(0)

    def return_data(self):

        return ([self.price, self.year, self.mileage, self.capacity, self.fuel, self.model, self.estimation])
