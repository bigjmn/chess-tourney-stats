import matplotlib.pyplot as plt

def plotcircles(data):
    fig, ax = plt.subplots()
    ax.set_xlim((1000, 2600))
    ax.set_ylim((1000, 2600))
    ax.set_xlabel('player rating')
    ax.set_ylabel('opponent rating')

    for k in data:
        circle = plt.Circle(k[0],5,color=k[1],alpha=.6)
        ax.add_patch(circle)
    fig.savefig('graphics/plotcircles.png')

def barstack(bardata):
    bardata.plot(x='rating difference', kind='bar', stacked=True,
    title='Results by Rating Difference')
    plt.savefig('graphics/barplot.png')


def makegraphics(circledata, bardata):
    plotcircles(circledata)
    barstack(bardata)
    return
