#! PYTHON 3
#
#Team:
#   Ernie Tsybulnik,
#   Chin Huynh
#   Ben Rieckers
#
#Class: CPSC 450
#Assignment: FriendNet (Deliverable 2)
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
#       Thus if A rates B a 9 then it will recommend all of B's friends who
#       are ranked 7 and above whereas if A rated B a 7 then it would only
#       recommend the friends of B that are rated 9 or above.
#       
#   -Who has the most mutual friends as you?
#       Given a user A, the algorithm will go through the entire graph
#       searching for the user who has the most mutual friends as you.
#       This will simply be iterating through everyones list of friends
#       comparing them to your friends. The person who has the most
#       mutual friends will updated as we loop through all of the
#       people.
#
#____________________________________________

try:
    from Queue import PriorityQueue, Empty 
except:
    from queue import PriorityQueue, Empty

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
    print(adjList)
    print("")
    userIndex = name.get(user)
    #if(userIndex != 0):
    personIndex = []
    maxMutual = 0
##    else:
##        personIndex = 1
##        maxMutual = 0
    userFriends = adjList[userIndex]
    print("index is", userIndex)
    print("friends are", userFriends)
    adjListLength = len(adjList)
    #print("adjList", adjListLength)
    for index in range(0, adjListLength):
        if index != userIndex:
            count = 0
            for people in adjList[index]:
                for friends in adjList[userIndex]:
                    if(people[0] == friends[0]):
                        count += 1
            if(count > maxMutual):
                maxMutual = count
                personIndex = [index]
                #print("person index after clearing", personIndex)
                #personIndex.append(index)
            elif(count == maxMutual ):
                personIndex.append(index)
    if( maxMutual != 0 ):
        print("the max mutual is", maxMutual)
        print("the person index is", personIndex)
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
        print("User ", users[0], " does not exist")
        found = false
    elif found:
        possibleFriends = []
        possibleFriendCount = 0
        for friends in adjList[name.get(user)]:
            if possibleFriendCount < 4:
                #If A hates B
                if friends[1] < 3:
                    #Find first friend that B hates that is not user or already friends with user
                    for Bfriends in adjList[name.get(friends[0])]:
                        if Bfriends[1] < 3 and Bfriends[0] != user and not isFriendsWith(user, Bfriends[0]):
                            possibleFriends.append(Bfriends[0])
                            possibleFriendCount += 1
                            break
                #If A doesn't like B
                elif friends[1] < 6:
                    #Find first friend that B doesn't like
                    for Bfriends in adjList[name.get(friends[0])]:
                        if Bfriends[1] > 2 and Bfriends[1] < 6 and Bfriends[0] != user and not isFriendsWith(user, Bfriends[0]):
                            possibleFriends.append(Bfriends[0])
                            possibleFriendCount += 1
                            break
                #If A is pretty good friends with B
                elif friends[1] < 9:
                    #Find first friend that B is pretty good friends with
                    for Bfriends in adjList[name.get(friends[0])]:
                        if Bfriends[1] > 5 and Bfriends[1] < 9 and Bfriends[0] != user and not isFriendsWith(user, Bfriends[0]):
                            possibleFriends.append(Bfriends[0])
                            possibleFriendCount += 1
                            break
                #Else A and B are very good friends
                else:
                    #Find first person that B like
                    for Bfriends in adjList[name.get(friends[0])]:
                        if Bfriends[1] > 8 and Bfriends[0] != user and Bfriends[0] and not isFriendsWith(user, Bfriends[0]):
                            possibleFriends.append(Bfriends[0])
                            possibleFriendCount += 1
                            break
        print("Recommended friends for ", user, ": ", possibleFriends)
        
        
    
def main():
    exitProgram = False
    while exitProgram == False:
        print()
        print("What do you want to do?")
        print("1) Check if user exists.")
        print("2) Check the connection between users.")
        print("3) Dijkstra’s Algorithm")
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
