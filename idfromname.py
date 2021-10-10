#NOTE YET IMPLEMENTED. It would have to
#reject a request if there are multiple members
#with that name as well. 
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
