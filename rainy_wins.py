class Winning_in_the_Rain():

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_rain_wins(self):
        raining_wins = pd.concat([self.dataframe, pd.get_dummies(self.dataframe['FTR'])], axis = 1).reset_index()

        away_games = pd.DataFrame(
            {'away rain games': raining_wins['AwayTeam'].value_counts()    })
        home_games = pd.DataFrame(
            {'home rain games': raining_wins['HomeTeam'].value_counts()    })

        raining_wins['winner'] = 'tie game'

        for i in range(len(raining_wins['A'])):
            if raining_wins['A'][i] == 1:
                raining_wins['winner'][i] = raining_wins['AwayTeam'][i]
            if raining_wins['H'][i] == 1:
                raining_wins['winner'][i] = raining_wins['HomeTeam'][i]        

        total_wins = pd.DataFrame(
            {'wins': raining_wins['winner'].value_counts()
            })

        appearances = pd.concat([away_games, home_games, total_wins], axis = 1)
        appearances['appearances'] = 0
        appearances = appearances.fillna(0)

        for i in range(len(appearances['home rain games'])):
            appearances['appearances'][i] = appearances['home rain games'][i] + appearances['away rain games'][i]


        winning_rain_pct = []
        for i in range(len(appearances['home rain games'])):
            if appearances['appearances'][i] == 0:
                winning_rain_pct.append(0)
            else:
                winning_rain_pct.append(round(float(appearances['wins'][i]) / float(appearances['appearances'][i]), 2))

        appearances['winning_rain_pct'] = winning_rain_pct

        appearances = appearances.fillna('0').drop(['home rain games', 'away rain games'], axis=1)
        return appearances

season2011 = Winning_in_the_Rain(rainy_wins)
season2011.get_rain_wins()