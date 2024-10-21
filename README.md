![birrwatch logo](static\images\birrwatch1.png)
## BirrWatch
BirrWatch is a web platform that consolidates foreign exchange rates from multiple Ethiopian banks, providing users with up-to-date and easily accessible currency information. The platform automatically scrapes exchange rate data from over 20 banks and displays the rates in a simple, user-friendly interface.
### Project Goal
BirrWatch aims to simplify the process of comparing exchange rates across different banks by collecting, storing, and displaying exchange rate data in a centralized location. Users can view current rates, track currency trends, and make informed decisions without having to manually visit each bank’s website.

### Key Features
Currency Comparison Table: Displays real-time exchange rates from various banks side by side.
Interactive Graphs: Visualizes historical trends for currencies or compares rates between banks.
Automated Data Updates: Exchange rate data is refreshed automatically every few hours.
Responsive Design: The platform is mobile-friendly, providing a seamless experience across devices.

### Technologies Used
Python: For web scraping and backend functionality.
Flask: As the web framework for the backend and RESTful API.
MySQL: To store the scraped exchange rate data.
Alpine.js: For frontend interactivity.
Bootstrap: For responsive and modern styling.
Chart.js: To create interactive data visualizations.

### Installation
Clone this repository:
`git clone https://github.com/sofoniasgd/birrwatch.git`

Navigate into the project directory:
`cd birrwatch`

Create a virtual enviroment
`python -m venv venv`

Activate the virtual enviroment
`source venv/bin/activate`

Install the required dependencies:
`pip install -r requirements.txt`

Set up the MySQL database:
Create a new MySQL database.
Configure your database connection settings in the .env file.

Run the application:
`flask run`

### License
This project is licensed under the MIT License.