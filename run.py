import requests
from bs4 import BeautifulSoup
import csv


QBR_URL = 'https://www.espn.com/college-football/qbr'


class Scraper(object): 
    def __init__(self): 
        self.url = QBR_URL
        self.data = []
        self.soup = None
        self.columns = []

    def gather_html(self): 
        page = requests.get(self.url)    
        self.soup = BeautifulSoup(page.content, "html.parser")

    def gather_names(self):
        # Get the table
        QBR_table = self.soup.find("table")

        # Gather the rows, skip the first one 
        rows = QBR_table.find_all('tr')
        
        for row in rows: 
            name = row.find('a', class_='AnchorLink')
            if not name: 
                continue

            school = row.find('span')
            self.data.append([name.text, school.text])

        # Now append the columns names
        self.columns.append('Name')
        self.columns.append('School')
        
    def add_stats(self):
        stat_table = self.soup.find('div', class_ = 'Table__Scroller')

        # Add in the header information
        headers = stat_table.find_all('th')
        for header in headers: 
            self.columns.append(header.find('a').text)

        # Add in the values 
        rows = stat_table.find_all('tr')
        row_count = 0 
        for row in rows: 
            values = row.find_all('td')
            # Add in all of the values 
            if values: 
                full_row = [value.text for value in values]
                self.data[row_count] = [*self.data[row_count], *full_row]
                row_count+=1
            

    def write_file(self):
        # open the file in the write mode
        with open('QBR.csv', 'w') as f:
            # create the csv writer
            writer = csv.writer(f)

            # write the columns then rows
            writer.writerow(self.columns)
            for row in self.data:
                writer.writerow(row)



            

                





    
    

if __name__ == '__main__': 
    QbrScraper = Scraper()
    QbrScraper.gather_html()
    QbrScraper.gather_names()
    QbrScraper.add_stats()
    QbrScraper.write_file()