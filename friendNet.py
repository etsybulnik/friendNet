#! PYTHON 3
#
#Team:
#   Ernie Tsybulnik,
#   Chin Huynh
#   Ben Rieckers
#
#Class: CPSC 450
#Assignment: FriendNet (Deliverable 1)
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
    #if name is in dictionary, gets the index and adds
    # the friends name and value of relationship to the
    # adjList at the appropriate index
    else:
        adjList[name.get(curr[0])].append([curr[1], curr[2]])

#print("adjacency list")
#print(adjList)

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
    #print(users)

def main():
    exitProgram = False
    while exitProgram == False:
        print()
        print("What do you want to do?")
        print("1) Check if user exists.")
        print("2) Check the connection between users.")
        print("3) Quit")
        print()
        command = int(input())
        if command == 1:
            checkUser()
        elif command == 2:
            checkConnection()
        elif command == 3:
            exitProgram = True
        else:
            print("Not a valid selection, please pick from the choices above.")

main()
