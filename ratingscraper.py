from bs4 import BeautifulSoup
import requests

def get_id(name):
    splitname = name.split(' ')
    firstname = splitname[0]
    lastname = splitname[1]
    #this is gross, but what can you do?
    search_url = "https://new.uschess.org/player-search?submit=1&pager=1&display_name="+firstname+"%2520"+lastname+"&rating_94%5Bmin%5D=&rating_94%5Bmax%5D=&quick_rating_95%5Bmin%5D=&quick_rating_95%5Bmax%5D=&blitz_rating_96%5Bmin%5D=&blitz_rating_96%5Bmax%5D=&online_regular_rating_165%5Bmin%5D=&online_regular_rating_165%5Bmax%5D=&online_blitz_rating_98%5Bmin%5D=&online_blitz_rating_98%5Bmax%5D=&online_quick_rating_97%5Bmin%5D=&online_quick_rating_97%5Bmax%5D=&correspondence_rating_101%5Bmin%5D=&correspondence_rating_101%5Bmax%5D="
    search_info = requests.get(search_url).text
    search_parser = BeautifulSoup(search_info, 'lxml')

    body = search_parser.find('tbody')
    print(body).text


def rating_from_crosstable(player_id, cross_url):
    cross_info = requests.get(cross_url).text
    soup = BeautifulSoup(cross_info, 'lxml')
    #this could probs be sped up. we'll see how bad the total runtime is
    ratingindex = str(soup).find(str(player_id)+ ' / R: ')
    if ratingindex == -1:
        print('not found')
        return
    #strips space from 3 digit rating, P from provisional
    rating = str(soup)[ratingindex+13:ratingindex+18].strip()
    if rating == 'Unra':
        return 0
    return int(rating)


def ratinghist(player_id):
    tourney_ratings = {}

    histurl = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?"+str(player_id)


    hist = requests.get(histurl).text
    soup = BeautifulSoup(hist, 'lxml')
    #number of history pages
    pages = len(soup.find_all('nobr'))
    print(pages)
    for i in range(pages):
        page_ratings = histpage(player_id, i+1)
        tourney_ratings.update(page_ratings)
    print(len(tourney_ratings))

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
        print('hist table is '+tourney_id)

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
    print(requests.get(search_url))
    soup = BeautifulSoup(search_info,'lxml')

    #we can skip a bunch of children, the ratings have this tag
    ratingcells = soup.find_all('nobr')
    print(len(ratingcells))


    for r in ratingcells:
        print(str(r.contents))
        #there are a few headers w the nobr tag, filter them out

        if '(R)' in str(r.contents):
            game_info = {}
            rating_string = str(r.contents)
            opp_rating = rating_string.split(' ')[0]
            game_info['opp_rating'] = opp_rating
            #the nobr is a child of a cell in the row. get the next cell
            result_cell = r.parent.next_sibling
            game_result = str(result_cell.text)
            game_info['result'] = result_dict[game_result]
            #the url for the tournament is in the first cell of the parent row
            row = result_cell.parent
            tourney_url = row.find('a')['href']
            #get tournament id from end ur url
            tourney_id = tourney_url.split('?')[-1]
            print('tourney length is '+str(len(tourney_id)))


            if tourney_id not in tourney_dict:
                continue
            your_rating = tourney_dict[tourney_id]
            game_info['your_rating'] = your_rating
            gamelogs.append(game_info)
    return gamelogs

def all_gamestats(uscf_id):
    tourney_ratings = ratinghist(uscf_id)

    opp_rating_dict = {}
    for i in range(1,28):
        zone = i*100
        new_stats = rating_table(uscf_id, zone, tourney_ratings)
        print(len(new_stats))
        opp_rating_dict[zone] = new_stats

    return opp_rating_dict










    #the first table with a header is the one we're looking for
    # table_header = soup.find('th')

    # full_table = table_header.parent.parent
    # rows = full_table.findChildren('tr')
    # for row in rows:
    #     cells = row.findChildren('nobr')
    #     for cell in cells:
    #         print(str(cell.contents))


#opp_rating_table(12872878,1700)
