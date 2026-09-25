import sqlite3



class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("tutorial.db")
        self.cur = self.connection.cursor()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Currencies (
                ID INTEGER PRIMARY KEY, 
                CODE VARCHAR UNIQUE, 
                FULLNAME VARCHAR, 
                SIGN VARCHAR
            )
        """)


        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS ExchangeRates (
                ID INTEGER PRIMARY KEY, 
                BaseCurrencyId INTEGER NOT NULL, 
                TargetCurrencyId INTEGER NOT NULL, 
                Rate Decimal(6),
                
                FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies(ID),
                FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies(ID),
                
                UNIQUE (BaseCurrencyId, TargetCurrencyId)
            )
        """)


    currencies_data = [("RUB", "Russian Ruble", "₽"),
                       ("USD", "US Dollar", "$"),
                       ("EUR", "Euro", "€"),
                       ("JPY", "Yen", "¥"),
                       ("KZT", "Tenge", "₸")
                      ]


    def get_currency_id(self, code):
        self.cur.execute("SELECT id FROM Currencies WHERE code = ?", (code,))
        result = self.cur.fetchone()
        if result is None:
            return None
        return result[0]

    def seed_data(self):
        sql_query_currencies = "INSERT OR IGNORE INTO Currencies (code, fullname, sign) VALUES (?, ?, ?)"
        self.cur.executemany(sql_query_currencies, self.currencies_data)
        self.connection.commit()


        rub_id = self.get_currency_id("RUB")
        usd_id = self.get_currency_id("USD")
        eur_id = self.get_currency_id("EUR")
        kzt_id = self.get_currency_id("KZT")


        exchangerates_data = [(usd_id, rub_id, 75.93),
                              (eur_id, usd_id, 1.14),
                              (eur_id, rub_id, 86.59),
                              (rub_id, kzt_id, 6.16),
                              (usd_id, kzt_id, 441.76)
                              ]


        sql_query_exchangerates = "INSERT OR IGNORE INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)"


        self.cur.executemany(sql_query_exchangerates, exchangerates_data)


        self.connection.commit()


