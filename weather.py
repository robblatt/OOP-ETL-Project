import pandas as pd
from dateutil import parser
import requests
import sqlite3
import datetime
import warnings
warnings.filterwarnings("ignore")

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

c.execute("""SELECT * FROM Matches;""")
matches = pd.DataFrame(c.fetchall())
matches.columns = [x[0] for x in c.description]

# Assumed location for Berlin for the purposes of this project.

berlin_lat = '52.520008'
berlin_long = '13.404954'

api_key = ''# USE YOUR OWN, YOU MOOCH

class Weather():

    
    def __init__(self, dataframe, year, lat, long, DarkSky_API):
        self.dataframe = dataframe
        self.year = year
        self.lat = lat
        self.long = long
        self.DarkSky_API = DarkSky_API

    
    def get_rain(self):
        """Time is timestamp, everything must be a string. Returns a list of DarkSky
        information. If you've already run this before, you can comment out the API
        call and reference a local file instead to save on API calls. Otherwise comment
        out the read_csv line. Executed within the rainy_days function."""
    #     dark_sky = []
    #     for days in time:
    #         resp = requests.get('https://api.darksky.net/forecast/' + self.DarkSky_API + '/' + self.lat + ',' + self.long + ',' + days + '?exclude=flags,hourly,daily,alerts')
    #         dark_sky.append(resp.json()['currently'])
        dark_sky = pd.read_csv('weather.csv') # Comment out this line if you don't have the data already
        return dark_sky

    
    def rainy_days(self):
        """Outputs a dataframe.
        Columns: 'Match_ID' - integer - unique match ID
                 'Date'     - string  - this is the date as input. The function converts it so 
                                        the Dark Sky API can handle it.
                 'AwayTeam' - string  - Away team's name
                 'HomeTeam' - string  - Home team's name
                 'FTR'      - string  - Three possible options.
                                     'A' for a victory for the Away Team
                                     'H' for a victory for the Home Team
                                     'D' for a draw
                 'rain'     - Boolean - Indicates if it was raining
                 """
        
        # In order to work with the Dark Sky API, we have to convert the list of dates to a timestamp
        
        gameDate = []
        for i in range(len(self.dataframe['Date'])):
            dt = parser.parse(self.dataframe['Date'][i])
            gameDate.append(dt)
            
        # Creates the DataFrame we'll use, adds the timestamped column,
        # and resets the index because we are now sorting by the year.
        # Otherwise the range(len(x)) would not work. We also create a 
        # set of unique dates for use later on.

        self.dataframe['gamedate'] = gameDate
        matches_year = matches[matches["Season"] == self.year].reset_index()
        dates = list(set(matches_year['gamedate']))

        timestamp = []
        for date in range(len(dates)):
            stamp = str(matches_year['gamedate'][date].timestamp())
            timestamp.append(stamp[:-2])

        # This is the Dark Sky API call. Use a csv of the data you get to
        # conserve API calls to easily stay under the 1k/day maximum. Using the
        # set created earlier, you have 6 opportunities to pull all of the dates.
        # Then we create a DataFrame of the response and filter that down to
        # the columns we need.
            
        the_rain = Weather(self.lat, self.long, 2011, timestamp, self.DarkSky_API)
            
        ds_df = pd.DataFrame(the_rain.get_rain())

        df_rain = pd.DataFrame(
            {'rainy': ds_df['icon'],
             'date': ds_df['time'],
            })

        # The Dark Sky data is in timestamp, so this brings it back to match
        # the original data, create a new dataframe of the unique dates and 
        # the rain condition.
        
        for day in range(len(ds_df['time'])):
            ds_df['time'][day] = datetime.datetime.utcfromtimestamp(ds_df['time'][day]).strftime('%Y-%m-%d')

        rain = pd.DataFrame(columns=['date', 'raining'])

        rain['date'] = ds_df['time']

        # Compare our unique dates in a loop and append the weather conditions.
        
        for i in range(len(ds_df['precipType'])):
            if ds_df['precipType'][i] == 'rain':
                rain.raining[i] = True
            else:
                rain.raining[i] = False
                
        rain_year = []
        for i in range(len(matches_year['Date'])):
            if matches_year['Date'][i] in list(rain.date[rain['raining'] == True]):
                rain_year.append(True)
            else:
                rain_year.append(False)

        matches_year['rain'] = rain_year
        
        # Creates the result, output as a dataframe with the columns mentioned earlier.

        result = matches_year[['Match_ID','Date','AwayTeam', 'HomeTeam', 'FTR', 'rain']]

        return result
    
season = Weather(matches, 2011, berlin_lat, berlin_long, api_key)

# Use this if you want a list of only the matches where it was raining.

rainy_wins = season.rainy_days()[season.rainy_days()['rain'] == True].reset_index()

rainy_wins

