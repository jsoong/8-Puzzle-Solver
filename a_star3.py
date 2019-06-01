from queue import PriorityQueue

#this class to keep the state of the game 
class State_game:

    #dim: dimension of the game grid
    #parent: parent of the current state
    #mystate: current state of the game
    #goal: final state required
    #cost: h(n) until now basically
    #direction: 1,2,3,4 implying D,R,U,L basically the move that brought from parent to current state
    def __init__(self, dim, parent, mystate, goal, cost, direction, choice):
        self.direction = direction
        self.dim = dim
        self.cost = cost
        self.mystate = mystate
        self.dist = self.get_distance(goal, choice)
        self.ind = self.str_rep(mystate)
        self.parent = parent

        #this stores wherever the zero index is
        self.zero_ind = 0
        for i in range(len(mystate)):
            if mystate[i] == 0:
                self.zero_ind = i

    #functions so that the priority queue doesnt throw errors
    def __eq__(self, other):
        return False

    def __lt__(self, other):
        return other

    #finds distance between the current state and the goal state
    def get_distance(self, goal, choice):
        dist = 0
        n = self.dim
        x_arr = [0]*(n*n)
        y_arr = [0]*(n*n)
        for i in range(1,len(self.mystate)):
            x,y = i//n,i%n
            x_arr[self.mystate[i]] += x
            y_arr[self.mystate[i]] += y
            x_arr[goal[i]] += -x
            y_arr[goal[i]] += -y

        for i in range(1,len(self.mystate)):
            dist += abs(x_arr[i]) + abs(y_arr[i])
            
        if choice == 1:
            return dist
        
        return dist + 2*self.calculate_conflicts(goal)
    
    #to get the string representation of the current game
    def str_rep(self,state):
        temp = ""
        for i in state:
            temp += str(i)
        return temp

    #this calculates the conflicts in the current and the goal
    def calculate_conflicts(self, goal):
        curr = self.mystate
        n = self.dim
        conflicts = 0
        line_arr = [[] for i in range(n)]
        
        goal_indices = [0]*(n*n)
        curr_indices = [0]*(n*n)
        
        for i in range(len(curr)):
            goal_indices[goal[i]] = i
            curr_indices[curr[i]] = i
            
        for i in range(len(curr)):
            curr_line = curr_indices[curr[i]]//3
            goal_line = goal_indices[curr[i]]//3
            if curr_line == goal_line:
                line_arr[curr_line].append(curr[i])
                
        for arr in line_arr:
            for i in range(len(arr)):
                for j in range(i):
                    if (curr_indices[arr[i]] - curr_indices[arr[j]])*(goal_indices[arr[i]] - goal_indices[arr[j]])<1:
                        conflicts += 1
            

        return conflicts
                
    
            
    #to get the children(next moves) of the current state
    def get_children(self, goal):
        n = self.dim
        x,y = self.zero_ind//n,self.zero_ind%n
        children = [None]*4
        if x + 1<n:
            children[3] = self.swap(self.zero_ind,(x+1)*n+y)
                
        if y + 1<n:
            children[2] = self.swap(self.zero_ind,x*n+y+1)

        if x - 1>=0:
            children[1] = self.swap(self.zero_ind,(x-1)*n+y)

        if y - 1>=0:
            children[0] = self.swap(self.zero_ind,x*n+y-1)

        return children

    #this is a helper function for the get_children method
    #it returns a new array with the required move(L.U.D.R) taken
    def swap(self,n1,n2):
        #print(n1,n2)
        arr = self.mystate.copy()
        temp = arr[n1]
        arr[n1] = arr[n2]
        arr[n2] = temp
        return arr
            

#to get the string representation of the current game            
def str_rep(state):
        temp = ""
        for i in state:
            temp += str(i)
        return temp


def Solve(start_state, goal, dim, choice):
    #starting state with parent as none and h(n) = 0
    start = State_game(dim, None, start_state, goal, 0, -1, choice)

    priorityQueue = PriorityQueue()

    visited = set()

    #keeps a count of the number of nodes created
    count = 0
    
    priorityQueue.put((start.dist,start))    
    found = False
    new_child = None

    #while the priority queue is not empty and the goal hasnt been found
    while(priorityQueue.qsize()>0 and not found):

        #this gives the node with the smallest f(n) in the queue
        closest = priorityQueue.get()[1]

        #for the same node we get the next swap configuration in children
        children = closest.get_children(goal)

        
        visited.add(closest.ind)
        i=0
        for child in children:
            #i=1,2,3,4 tells if we go L,U,R,D
            i+=1
            #this means this direction was not available
            if child == None: continue
            
            if str_rep(child) not in visited:
                count += 1
                new_child = State_game(dim, closest, child, goal, closest.cost+1,i, choice)

                #check if we have reached goal. For goal dist = 0
                if new_child.dist==0:
                    found = True
                    break
                temp = (new_child.dist + closest.cost+1, new_child)
                priorityQueue.put(temp)


    f = []
    moves = []

    #here we return the data required for the output
    if(found):
        #we take the goat and backtrack to its parents to find the moves played and f(n)
        temp = new_child
        while temp.parent != None:
            moves.append(temp.direction)
            f.append(temp.cost+temp.dist)
            temp = temp.parent
        f.append(temp.cost+temp.dist)
        return (f,moves,count)
    
    return None
    

if __name__ == "__main__":
    
    f = open("Input7B.txt",'r')
    f2 = open("Output7B.txt",'w')
    n=3
    choice = int(input("Heuristics: Enter 1 for Manhattan or 2 for Manhattan + linear conflicts: "))

    start_state = [0]*(n*n)

    for i in range(n):
        line = f.readline()
        f2.write(line)
        vals = [int(i) for i in line.split()]
        for j in range(n): start_state[i*3+j] = vals[j]
        
    f.readline()
    f2.write("\n")

    goal_state = [0]*(n*n)

    for i in range(n):
        line = f.readline()
        f2.write(line)
        vals = [int(i) for i in line.split()]
        for j in range(3): goal_state[i*3+j] = vals[j]

    f.close()

    f2.write("\n")
        
    x = Solve(start_state, goal_state, n, choice)

    actions = ""
    fn = ""
    move_type = ['L','U','R','D']
    if x==None:
        print("Not possible")
    else:
        (f,moves,count) = x
        fn += str(f[-1]) + " "
        #the moves and f(n) were returned in reverse order so we run loop backwards
        for i in range(len(moves)-1,-1,-1):
            actions += move_type[moves[i]-1] + " "
            fn+= str(f[i]) + " "

        f2.write("\n")
        f2.write(str(len(moves)) + "\n")
        f2.write(str(count) + "\n")
        f2.write(actions + "\n")
        f2.write(fn)
        
            
    f2.close()    



    

 
