#! PYTHON 3
#
#Team:
#   Ernie Tsybulnik,
#   Chin Huynh
#   Ben Rieckers
#
#Class: CPSC 450
#Assignment: FriendNet (Final Part)
#
#"Best Friend Chain"
#   We will be using Dijkstras algorithm, in essence finding the
#   shortest path from user A to user B. Dijkstras alg. is somewhat
#   similar to breadth-first-search, but it respects edge costs.
#   Link to video about the alg:
#   https://www.youtube.com/watch?v=8Ls1RqHCOPw
#
#2 killer features
#   -Recommended Friends
#       This will work by looking at the friends of user 'A' and then based 
#       on A's likeability of his friends, the algorithm will recommend
#       friends of those friends also based on how good of friends they are.
#       It will recommend friends who have likability >7 of friends of the user
#       who have likability of >7.
#       It will also recommend frienemies of friends who have likeability <4 of
#       friends of the user who have likability of <4. (Double negative = positive?)
#       
#   -Who has the most mutual friends as you?
#       Given a user A, the algorithm will go through the entire graph
#       searching for the user(s) who has the most mutual friends as you.
#       This will simply be iterating through everyone's list of friends
#       comparing them to your friends. The person who has the most
#       mutual friends will updated as we loop through all of the
#       people.
#
#____________________________________________


file = open("friend_network.txt", "r")

data = []

#reads the lines from the file one by one and then
# creates a lists of lists with those lines
for line in file:
    line = line.strip('\n')
    temp = line.split(" ")
    temp[2] = int(temp[2])
    data.append(temp)

file.close()

#contains the name and index of each person
name = dict()
adjList = []

count = 0

#index in adjList corresponds to name at that index in 'peopleInOrder'
peopleInOrder = []

#creates adjacency list and dictionary
#format: [ [['Scooter', 10], ['Daisy', 2]], [['Roland', 8]] ]
for curr in data:
    #if name is not in the dictionary, adds it to the
    #dictionary and then appends a list with the the
    # friends name and value of their relationship
    if name.get(curr[0]) == None:
        name[curr[0]] = count
        adjList.append([[curr[1], curr[2]]])
        count += 1
        peopleInOrder.append(curr[0])
    #if name is in dictionary, gets the index and adds
    # the friends name and value of relationship to the
    # adjList at the appropriate index
    else:
        adjList[name.get(curr[0])].append([curr[1], curr[2]])

def checkUser():
    user = input("What user? (Case-Sensitive) ")
    if name.get(user) == None:
        print(user, "does NOT exist.")
    else:
        print(user, "does exist.")

def checkConnection():
    users = (input("What users (seperated by spaces)(Case-sensitive)? ")).split(" ")
    found = True
    if name.get(users[0]) == None:
        print("User", users[0], "does not exist.")
        found = False
    if name.get(users[1]) == None:
        print("User", users[1], "does not exist.")
        found = False
    if found:
        for friends in adjList[name.get(users[0])]:
            if friends[0] == users[1]:
                print("The connection from", users[0], "to", users[1],
                      "has weight", friends[1], ".")
                return
        print("The edge from", users[0], "to", users[1], "does not exist.")


def dijkstra2(Graph, source):
    dist = dict()
    prev = dict()
    for v in peopleInOrder:
        dist[v] = float("inf")
        prev[v] = None
    dist[source] = 0
    Q = list(peopleInOrder)
    while len(Q) > 0:
        minK = Q[0]
        for user in Q:
            if dist.get(user) <= dist.get(minK):
                minK = user
        Q.remove(minK)
        neighbors = adjList[name.get(minK)]
        for person in neighbors:
            alt = dist[minK] + 10-person[1]
            if alt < dist[person[0]]:
                dist[person[0]] = alt
                prev[person[0]] = minK
    return prev

def bestFriendChain(personA, personB):
    connections = dijkstra2(adjList, personA)
    chain = []
    chain.append(personB)
    while personB != personA and personB != None:
        personB = connections.get(personB)
        chain.append(personB)
    if personB == None:
        print("No chain exists between the users")
    else:
        print("Best friend chain is ", list(reversed(chain)))

def mostMutualFriends(user):
    print("")
    found = True
    if name.get(user) == None:
        print("User does not exist")
        found = False
    elif found:
        userIndex = name.get(user)
        personIndex = []
        maxMutual = 0
        userFriends = adjList[userIndex]
        adjListLength = len(adjList)
        #loops over all people in adjList
        for index in range(0, adjListLength):
            if index != userIndex:
                count = 0
                #loops over all friends of person at that index
                for people in adjList[index]:
                    #compares with users friends
                    for friends in adjList[userIndex]:
                        if(people[0] == friends[0]):
                            count += 1
                if(count > maxMutual):
                    maxMutual = count
                    personIndex = [index]
                elif(count == maxMutual ):
                    personIndex.append(index)
        #print results
        if( maxMutual != 0 ):
            print(user, "has", maxMutual, "mutual friend(s) with:")
            for index in personIndex:
                print(peopleInOrder[index])
        else:
            print("Nobody has mutual friends with", user)

def isFriendsWith(a, b):
    flag = False
    for friends in adjList[name.get(a)]:
        if friends[0] == b:
            flag = True
            break
    return flag

def recommendFriend(user):
    found = True
    if name.get(user) == None:
        print("User does not exist")
        found = False
    elif found:
        frenemies = []
        bestFriends = []
        fenemyCount = 0
        bestFriendCount = 0
        for friends in adjList[name.get(user)]:
                #If A hates B
                if friends[1] < 4:
                    #Find first friend that B hates that is not user or already friends with user
                    for Bfriends in adjList[name.get(friends[0])]:
                        if Bfriends[1] < 4 and Bfriends[0] != user and not isFriendsWith(user, Bfriends[0]):
                            frenemies.append(Bfriends[0])
                            fenemyCount += 1
                elif friends[1] > 7:
                    #Find first person that B like
                    for Bfriends in adjList[name.get(friends[0])]:
                        if Bfriends[1] > 7 and Bfriends[0] != user and not isFriendsWith(user, Bfriends[0]):
                            bestFriends.append(Bfriends[0])
                            bestFriendCount += 1
        print("Recommended frenemies for ", user, ": ", frenemies)
        print("Recommended best friends for ", user, ": ", bestFriends)

def main():
    exitProgram = False
    while exitProgram == False:
        print()
        print("What do you want to do?")
        print("1) Check if user exists.")
        print("2) Check the connection between users.")
        print("3) Best Friend Chain")
        print("4) Most mutual friends")
        print("5) Recommend friends")
        print("6) Quit")
        print()
        command = int(input())
        if command == 1:
            checkUser()
        elif command == 2:
            checkConnection()
        elif command == 3:
            users = (input("What users (seperated by spaces)(Case-sensitive)? ")).split(" ")
            bestFriendChain(users[0], users[1])
        elif command == 4:
            user = (input("What user? (Case-sensitive): "))
            mostMutualFriends(user)
        elif command == 5:
            user = (input("What user? (Case-sensitive): "))
            recommendFriend(user)
        elif command == 6:
            exitProgram = True
        else:
            print("Not a valid selection, please pick from the choices above.")
            

main()
