
def gamegrid(stats):

    batchgrid = {}
    for i in range(54):
        for j in range(54):
            batchgrid[(i,j)] = [0,0]
    for game in stats:
        #get indeces, adjust for min 100 rating
        opp_rating = int(game['opp_rating'])
        opp_index = opp_rating//50 - 2
        player_rating = int(game['your_rating'])
        player_index = player_rating//50 - 2

        batchgrid[(player_index, opp_index)][0]+=game['result']
        batchgrid[(player_index, opp_index)][1]+=1

    return gamegrid
