
# Summative Lab for Flatiron School's Data Science Module 2 

## The Goal

Discover how rain effected the outcome of German Bundesliga football games during the 2011 season.

## Methodology

- The game results came from an sqlite file from this [kaggle page](https://www.kaggle.com/laudanum/footballdelphi), which consisted of game results from 1993 - 2016 from English Premier League and German Bundesliga.
- For the assignment, we were asked to assume that all games in the 2011 season occured in Berlin and to use the Dark Sky API to discover if it had rained during the specific game.
- Using Python, my team (along with [LinhDan Nguyen](https://github.com/lnhdn) & [Kal Lemma](https://github.com/klemma14)), we used Pandas to evaluate, clean the data, and create visualizations, and write the data into a MongoDB database.

![The process](https://raw.githubusercontent.com/robblatt/OOP-ETL-Project/master/Screen%20Shot%202019-08-06%20at%2010.18.39%20AM.png)

## Results

![animated gif of results](https://raw.githubusercontent.com/robblatt/OOP-ETL-Project/master/game%20results.gif)

- We were able to successfully create a MongoDB database of the wins and losses.

### Files
- Football Weather Final.ipynb
  * The final project
  
- Get Weather and Rain Wins Percentage.ipynb
  * An attempt to create a dataframe of the wins/losses and cross-reference it with the rain data

- index.ipynb
  * The original instructions for the assignment

- Project 2.ipynb
  * Contains EDA
  
- database.sqlite
  * Original data

- weather.py
  * Contains the function for getting the weather for the appropriate dates from the DarkSky API

- weather.csv
  * In order to minimize the DarkSky API calls, the csv was created
