from mystats import jstats

def diffgrid(stats, blocksize):
        batchgrid = [[]*(1200//blocksize)]
        for g in stats:
            for game in stats[j]:
                opp_rating = game['opp_rating']
                if opp_rating == '(Unrated)':
                    continue
                opp_rating = int(opp_rating)
                your_rating = game['your_rating']
                if your_rating == '(Unrated)':
                    continue
                your_rating = int(your_rating)
                rating_diff = opp_rating - your_rating

def gamegrid(stats, blocksize):







    units = 2700//blocksize
    for i in range(units):
        opplist = []
        for j in range(units):
            opplist.append([0,0])
        batchgrid.append(opplist)
    for g in stats:
        for game in stats[g]:
        #get indeces, adjust for min 100 rating
            opp_rating = game['opp_rating']
            if opp_rating == '(Unrated)':
                continue
            opp_rating = int(opp_rating)
            opp_index = (opp_rating-100)//blocksize
            player_rating = game['your_rating']
            if player_rating == '(Unrated)':
                continue
            player_rating = int(player_rating)
            player_index = (player_rating-100)//blocksize

            batchgrid[player_index][opp_index][0]+=game['result']
            batchgrid[player_index][opp_index][1]+=1



    return batchgrid
