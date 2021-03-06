from bs4 import BeautifulSoup
import requests

def ratinghist(player_id):
    tourney_ratings = {}

    histurl = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?"+str(player_id)


    hist = requests.get(histurl).text
    soup = BeautifulSoup(hist, 'lxml')
    #number of history pages
    pages = len(soup.find_all('nobr'))

    for i in range(pages):
        page_ratings = histpage(player_id, i+1)
        tourney_ratings.update(page_ratings)


    return tourney_ratings



def histpage(player_id, pagenum):
    pageratings = {}


    histurl = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?"+str(player_id)+'.'+str(pagenum)



    hist = requests.get(histurl).text
    soup = BeautifulSoup(hist, 'lxml')
    #number of history pages



    tables = soup.find_all('table')
    bigtable = tables[3]
    subtables = bigtable.find_all('table')
    tourneytable = subtables[2]
    for row in tourneytable.find_all('tr')[2:]:
        cells = row.find_all('td')

        if len(str(cells[2].text)) == 1:
            continue
        rating = str(cells[2].text).split(' ')[0]
        tourney_id = str(cells[0].small.text).strip()


        pageratings[tourney_id] = rating
    return pageratings


def rating_table(uscf_id, opp_rating_zone,tourney_dict):

    gamelogs = []
    #technically shouldn't remake this dictionary here, but come on
    result_dict = {
    'W':1,
    'L':0,
    'D':.5
    }
    search_url = "https://www.uschess.org/datapage/gamestats.php?memid="+str(uscf_id)+"&ptype=G&rs=R&dkey="+str(opp_rating_zone)+"&drill=G"
    search_info = requests.get(search_url).text

    soup = BeautifulSoup(search_info,'lxml')

    #we can skip a bunch of children, the ratings have this tag
    ratingcells = soup.find_all('nobr')



    for r in ratingcells:

        #there are a few headers w the nobr tag, filter them out

        if '(R)' in str(r.contents):
            game_info = {}
            rating_string = str(r.contents)
            opp_rating = rating_string.split(' ')[0]
            game_info['opp_rating'] = opp_rating[2:]
            #the nobr is a child of a cell in the row. get the next cell
            result_cell = r.parent.next_sibling
            game_result = str(result_cell.text)
            game_info['result'] = result_dict[game_result]
            #the url for the tournament is in the first cell of the parent row
            row = result_cell.parent
            tourney_url = row.find('a')['href']
            #get tournament id from end ur url
            tourney_id = tourney_url.split('?')[-1]



            if tourney_id not in tourney_dict:
                continue
            your_rating = tourney_dict[tourney_id]
            game_info['your_rating'] = your_rating
            gamelogs.append(game_info)
    return gamelogs

def all_gamestats(uscf_id):
    print('getting tournament history')
    tourney_ratings = ratinghist(uscf_id)

    opp_rating_dict = {}
    print('getting opponents ratings')
    for i in range(1,28):
        zone = i*100
        new_stats = rating_table(uscf_id, zone, tourney_ratings)

        opp_rating_dict[zone] = new_stats

    return opp_rating_dict
