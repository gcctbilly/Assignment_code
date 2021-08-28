import math

whole_data = {'userx': {'passwordx': {'name': 'X', 'friends': ['Y','W'], 'articles': {'A2' : { 'content': 'contentA2', 'quote': 'A1'} } } },
              'userw': {'passwordw': {'name': 'W', 'friends': ['Y','X'], 'articles': {'A3' : { 'content': 'contentA3', 'quote': 'A2'}, 'A1': { 'content': 'contentA1',  'quote': ''} } } },
              'usery': {'passwordy': {'name': 'Y', 'friends': ['Z','W','X'], 'articles': {'A5' : { 'content': 'contentA5', 'quote': 'A1'} } } },
              'userz': {'passwordz': {'name': 'Z', 'friends': ['Y'], 'articles': {'A4' : { 'content': 'contentA4', 'quote': 'A2'} } } }
                       }

username_to_password = {'userx' : 'passwordx', 'userw': 'passwordw', 'usery': 'passwordy', 'userz': 'passwordz' }

truename_to_username = {'X': 'userx', 'W': 'userw', 'Y': 'usery', 'Z': 'userz' }

title_to_username = {'A1': 'userw', 'A2': 'userx', 'A3': 'userw', 'A4': 'userz', 'A5': 'usery' }

def isFriend(x,y):
    """This function is used to find whether y is a friend of x"""
    data_base = whole_data  #saven the message
    username_to_p = username_to_password
    for username in data_base:        #Extract user password
        password = username_to_p[username]
        if data_base[username][password]["name"] == x:     #find user X
            for z in range(0,len(data_base[username][password]["friends"])):
                if data_base[username][password]["friends"][z] == y:    #find friends index y
                    return True
    return False


def Relationship(kol_list: list):
    """ This function will receive a kol_list with truename and return a list of list. Each list will contain two person
    who are friends. If there is no relation between kols, it will return an empty list"""
    data_base = whole_data  # copy data
    friends_list = []
    for i in range(len(kol_list) - 1):   # exam every two kols whether they are friend
        truename_left = kol_list[i]
        for j in range(i+1, len(kol_list)):
            append_list = []
            turename_right = kol_list[j]
            if isFriend(truename_left, turename_right):
                append_list.append(truename_left)
                append_list.append(turename_right)
                friends_list.append(append_list)
    return friends_list


def DirectReport(a:str):
    """ This fuction will receive an article and return a article list that direct  quote this article"""
    data_base = whole_data   # copy data
    username_to_p = username_to_password
    article_list = []

    for username in data_base: # look through every user
        password = username_to_p[username] # get password by username
        for title in data_base[username][password]['articles']: # exam whether the articles quote a
            if data_base[username][password]['articles'][title]['quote'] == a:
                article_list.append(title)

    return article_list

def Report(a:str):
    """ This fuction will receive an article and return a article list that direct or indirect quote this article"""
    article_list = DirectReport(a) # get the direct report
    if len(article_list) != 0: # if it has direct report do
        middle_list = article_list
        for i in range(len(middle_list)):
            article_list.extend(Report(middle_list[i]))  # use recursive function to get the quote article one by one until it does not any article quote target article
    return article_list

def Compute_influence(name:str):
    """ This function will receive a user's truename and return a list that contain usernames which quote
    this users articles"""
    truename_to_u = truename_to_username  #copy data
    username_to_p = username_to_password
    data_base = whole_data
    title_to_u = title_to_username
    username = truename_to_u[name]  #change turename to username
    password = username_to_p[username] # get password
    writer_usernames_list = []
    for title in data_base[username][password]['articles']: # look through every articles of this user
        article_list = Report(title) # get articles which quote this user's article
        for article in article_list:
            if title_to_u[article] not in writer_usernames_list and title_to_u[article] != username:
                writer_usernames_list.append(title_to_u[article])
    return(writer_usernames_list)

def anchor(A):
    """This function is used to find a anchor K of A, A directly or indirectly quote K"""
    M=[]
    m=1
    data_base = whole_data
    username_to_p = username_to_password
    for username in data_base:
        password = username_to_p[username]
        if A in data_base[username][password]['articles']:  #find A location
            K=data_base[username][password]['articles'][A]['quote']#find K
    while True:
        for username in data_base:
            password = username_to_p[username]
            if K in data_base[username][password]['articles']:   #search for where is K
                if data_base[username][password]['articles'][K]['quote']=='': #find anchor
                    return K
                else:
                    K=data_base[username][password]['articles'][K]['quote']   #loop

def isDirectSource(A,B):
    '''
    The user needs to input A and B, and the system will judge whether A is the direct source of B. If it is, return true. If not, it will return false.
    '''
    data_base = whole_data       #saven the message
    username_to_p = username_to_password
    for username in data_base:        #user's password
        password = username_to_p[username]
        if B in data_base[username][password]['articles']:   #find B's location
            if A in data_base[username][password]['articles'][B]['quote']:      #find A's location
                return True
            else:
                return False

def isSource(A,B):
    '''
    The user needs to input A and B. The system judges whether A is the direct or indirect source of B. If so, it returns true. Otherwise, it returns false.
    '''
    m=0
    data_base = whole_data       #saven the message
    username_to_p = username_to_password
    for username in data_base:           #user's password
        password = username_to_p[username]
        if B in data_base[username][password]['articles']:  #find B location
            K=data_base[username][password]['articles'][B]['quote']   #find K
            if K==B:      #Direct source
                return True
            elif K=='':   #It is the anchor
                return False
            else:
                while m==0:
                    for username in data_base:
                        password = username_to_p[username]
                        if K in data_base[username][password]['articles']:        #search for where is K
                            if data_base[username][password]['articles'][K]['quote'] == A:    #Check whether A belongs to K
                                return True
                                m=1
                            elif data_base[username][password]['articles'][K]['quote'] == '': #If it is the anchor. There is no source.
                                return False
                                m=1
                            else:
                                K=data_base[username][password]['articles'][K]['quote'] #loop

def register():
    """This function can present a register face that can lead people to input some information """
    username = input("Please input your username: ")
    password = input("Please input your password: ")
    username_to_password[username] = password
    truename = input("Please input your true name: ")
    truename_to_username[truename] = username
    whole_data[username] = {}
    whole_data[username][password] = {}
    whole_data[username][password]['name'] = truename
    whole_data[username][password]['friends'] = []
    whole_data[username][password]['articles'] = {}
    test = True
    while test:
        print("If you want to add friends please input 1")
        print("If you want to add articles please input 2")
        print("If you want to logout please input -1")
        i = input("Please input here: ")
        if i == "-1":
            break
        if i != "1" and i != "2":
            continue
        if i == "1": # input friends
            friends_test = True
            while friends_test:
                friends_name = input("Please input your friends true name: ")
                whole_data[username][password]['friends'].append(friends_name)
                j = input("If you want to add other friends please input 1, or you can input any other words to end: ")
                if j == "1":
                    continue
                else:
                    break
        if i == "2": # input article
            article_test = True
            while article_test:
                title = input("Please input your article's title: ")
                title_to_username[title] = username
                content = input("Please input your articles's content: ")
                quote = input("Please input the article's title that you quote, if not click Enter: " )
                whole_data[username][password]['articles'][title] = {}
                whole_data[username][password]['articles'][title]['content'] = content
                whole_data[username][password]['articles'][title]['quote'] = quote
                j = input("If you want to add other articles please input 1, or you can input any other words to end: ")
                if j == "1":
                    continue
                else:
                    break


def main():
    """ this function is used to print out the kol's name and their friends and register for user"""
    register_test = True
    while register_test:
        i = input("If you want to register please input 1, or input 2 to find the kols: ")
        if i != "1" and i != "2":
            continue
        if i == "1":
            register()
        if i == "2":
            register_test = False
    truename_to_u = truename_to_username  # copy data
    username_to_p = username_to_password
    data_base = whole_data
    title_to_u = title_to_username

    prime_kol_dict ={}
    t = eval(input("Please input 'T' here: "))
    p = eval(input("Please input 'P' here: "))
    total_writer = len(whole_data)
    max_writer = math.floor((total_writer * p) / 100)
    kol_list = []
    kol_name_list = []
    for username in data_base: # compute every users influence and add the person who influence > t to the prime_kol_dict
        password = username_to_p[username]
        truename = data_base[username][password]['name']
        influence = len(Compute_influence(truename))
        if influence > t:
            prime_kol_dict[truename] = influence
    if len(prime_kol_dict) < max_writer: # compare the length of prime_kol_dict and max_writer
        max_writer = len(prime_kol_dict)
    prime_kol_order = sorted(prime_kol_dict.items(), key = lambda x:x[1], reverse= True)
    for i in range(max_writer): # add the top t users to kol_list
        kol_list.append(prime_kol_order[i])
    i = max_writer
    test = True
    while test and i < len(prime_kol_order):  # if their is equal influence
        if prime_kol_order[i-1][1] == prime_kol_order[i][1]:
            kol_list.append(prime_kol_order[i])
        else:
            test = False
        i = i+1
    for i in range(len(kol_list)): # get the truename of kol
        kol_name_list.append(kol_list[i][0])
    relationship_list = Relationship(kol_name_list) # get the relationship of the kol
    print("The kols are:",kol_name_list)
    if len(relationship_list) != 0:
        print("Relationship between kols is: ")
        for i in range(len(relationship_list)):
            j = 0
            print("{} and {} is friends".format(relationship_list[i][j],relationship_list[i][j+1]))
    else:
        print("There is no relationship between kols")




main()



