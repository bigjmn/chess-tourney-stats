import matplotlib.pyplot as plt
import numpy as np
from create_grid import gamegrid
from mystats import jstats
import math
import pandas as pd
def labplot(cell):
    tot_games = cell[1]
    if tot_games == 0:
        return 0
    winrate = cell[0]/cell[1]
    return winrate


def get_colors(cell):
    tot_games = cell[1]
    #if no games in cell, transparency is 100%
    if tot_games == 0:
        return (0,0,0,0)
    winrate = cell[0]/cell[1]
    win_color = int(255*winrate)
    #don't want to do 255-win_color in case it's a tie.
    #would rather 127 and 127
    loss_color = int(255*(1-winrate))
    #bit random here, we'll see how it goes.
    alpha = int(min(255, (1-.5**tot_games)*256))
    purp = 10*tot_games


    return (loss_color, win_color, purp, alpha)

def get_graph(grid, canvasdim):
    #could transform the grid in place,
    #but it's already a reasonable size now,
    #and not dependent on the number of games played
    cuts = len(grid)
    squaresize = canvasdim//cuts
    print(squaresize)
    graph = Image.new(mode="RGBA", size=(canvasdim,canvasdim))
    ctx = ImageDraw.Draw(graph)
    for i in grid:
        rectdims = [i[0]*squaresize, i[1]*squaresize, i[0]*squaresize+squaresize, i[1]*squaresize+squaresize]
        rectcol = get_colors(grid[i])
        print(rectcol)

        ctx.rectangle(rectdims, fill=rectcol)
    return graph


def plot_graph(grid):

    for i in grid:
        grid[i] = labplot(grid[i])
    return grid

def plotfromstats(stats):
    res = {
    0:[[],[]],
    .5:[[],[]],
    1:[[],[]]
    }

    for g in stats:
        for game in stats[g]:
            opp_rating = game['opp_rating']
            if opp_rating == '(Unrated)':
                continue
            opp_rating = int(opp_rating)
            your_rating = game['your_rating']
            if your_rating == '(Unrated)':
                continue
            result = game['result']
            res[result][0].append(your_rating)
            res[result][1].append(opp_rating)
    return res


def circfromstats(stats):
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




#p = circfromstats(jstats)


a, b = circfromstats(jstats)

def graphnow(myplot):
    fig, ax = plt.subplots()
    ax.set_xlim((1000, 2600))
    ax.set_ylim((1000, 2600))

    for k in myplot:
        circle = plt.Circle(k[0],5,color=k[1],alpha=.6)
        ax.add_patch(circle)
    fig.savefig('plotcircles.png')

def barstack(diffdata):
    diffdata.plot(x='rating difference', kind='bar', stacked=True,
    title='Stacked Bar Graph by dataframe')
    plt.savefig('barplot.png')

v = barstack(b)
