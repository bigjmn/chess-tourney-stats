import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

#prep the plots
def plotdata(stats):
    coldict = {
    0:'red',
    .5:'blue',
    1:'green'
    }

    #data for circles
    circlist = []

    #data for rating diff graph
    difflist = np.zeros((25,3))
    #for indexing based on result
    r = lambda a: int(2*a)

    rowlist = []
    for region in range(25):
        rowlist.append(region*50-600)



    for g in stats:
        for game in stats[g]:
            opp_rating = game['opp_rating']
            if opp_rating == '(Unrated)':
                continue
            opp_rating = int(opp_rating)
            your_rating = game['your_rating']
            if your_rating == '(Unrated)':
                continue
            your_rating = int(your_rating)
            result = game['result']
            circstats = [(your_rating, opp_rating), coldict[result]]
            circlist.append(circstats)
            diffstats = []
            rating_diff = opp_rating - your_rating
            #okay this part is gross, but I
            adj_diff = round(rating_diff/50)
            if abs(adj_diff)>12:
                continue

            difflist[adj_diff+12][r(result)]+=1
    df = pd.DataFrame(difflist)
    df.columns = ['lose', 'draw', 'win']
    df.insert(0,'rating difference', rowlist)




    return circlist, df





#a, b = plotdata(jstats)
