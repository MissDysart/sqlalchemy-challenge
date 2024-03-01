# sqlalchemy-challenge
## Module 10 Challenge - Adv SQL

Acknowledgements
I was able to create most of the challenge with class activities. The following resources helped where activities fell short:
- Peers: J. Montgomery for helping with the precipitation plot and L. Tschudi for reminding me to check my terminal path.
- GeeksforGeeks.org for information on the replace function.

Files and folders in repository:
1. SurfsUp folder
    - hi_climate.ipynb covers 'Part 1: Analyze and Explore the Climate Data' for a Hawaii vacation.
    - app.py covers 'Part 2: Design your Climate App'
2. Resources folder contains files that were provided in the Starter Code.
    - hawaii_measurements.csv
    - hawaii_statons.csv
    - hawaii.sqlite

Part 1:
- Use SQLAlchemy to connect to hawaii.sqlite, reflect tables, and create and close session.
- The Precipitation Analysis asked for the most recent date in the dataset to use to collect a year's worth of data into a Pandas DataFrame and create a visual. Also gathered the summary statistics for the data.
- The Station Analysis asked for the number of stations and their temperature observations. It then asked for the min, max, and average temperatures for the most active station. After gathering a year's worth of temperature data, I created a histogram with the help of another Pandas Dataframe.

Part 2:
- Use hawaii.sqlite and information gathered from Part 1 to create a Flask API with the following pages:
    - Static routes
        - Homepage with all available routes.
        - Precipitation page for the precipitation analysis from Part 1.
        - Stations page for a list of stations in 'stations.csv'.
        - tobs page for temperature observations for the most active station (found in Part 1).
    - Dynamic routes
        - One page to return the min, average, and max temperatures from a user-input start date.
        - A second page to return the min, average, and max temperatures for user-input start and end dates.