import utils


class DStarLite:

    def __init__(self):
        self.nodeStart = "A"
        self.nodePrev = self.nodeStart
        self.nodeGoal = "G"

        self.km = 0

        self.pq = utils.PriorityQueue()
        self.edgeCost = { "AB": 1, "BC": 1, "BD": 1, "CD": 1, "CG": 1, "DG": 10 }
        self.prevEdgeCost = { "AB": 1, "BC": 1, "BD": 1, "CD": 1, "CG": 1, "DG": 10 }
        self.gValue = { "A": float('inf'), "B": float('inf'), "C": float('inf'), "D": float('inf'), "G": float('inf') }
        self.rhs = { "A": float('inf'), "B": float('inf'), "C": float('inf'), "D": float('inf'), "G": 0 }
        self.heuristic = self.getHeuristics()

        self.pq.push( (self.nodeGoal, (self.heuristic[self.nodeGoal], 0)) )

    def getNeighbours(self, node):
        if (node == "A"):
            return ["B"]
        elif (node == "B"):
            return ["A", "C", "D"]
        elif (node == "C"):
            return ["B", "D", "G"]
        elif (node == "D"):
            return ["B", "C", "G"]
        elif (node == "G"):
            return ["C", "D"]
        else:
            return None

    # Return heuristic of all nodes from start node / robot node
    def getHeuristics(self):
        if (self.nodeStart == "A"):
            return { "A": 0, "B": 1, "C": 2, "D": 2, "G": 3 }
        elif(self.nodeStart == "B"):
            return { "A": 1, "B": 0, "C": 1, "D": 1, "G": 2 }
        elif(self.nodeStart == "C"):
            return { "A": 2, "B": 1, "C": 0, "D": 1, "G": 1 }
        elif(self.nodeStart == "D"):
            return { "A": 2, "B": 1, "C": 1, "D": 0, "G": 1 }
        elif(self.nodeStart == "G"):
            return { "A": 3, "B": 2, "C": 1, "D": 1, "G": 0 }
        else:
            return None

    def calculateKeys(self, nodeName):
        k1 = min(self.gValue[nodeName], self.rhs[nodeName]) + self.heuristic[nodeName] + self.km
        k2 = min(self.gValue[nodeName], self.rhs[nodeName])
        return ( k1, k2 )

    def updateVertex(self, nodeName):

        if ( (self.gValue[nodeName] != self.rhs[nodeName]) and (nodeName in self.pq.getNames()) ):
            self.pq.update( (nodeName, self.calculateKeys(nodeName)) )

        elif ( (self.gValue[nodeName] != self.rhs[nodeName]) and (nodeName not in self.pq.getNames()) ):
            self.pq.push( (nodeName, self.calculateKeys(nodeName)) )

        elif ( (self.gValue[nodeName] == self.rhs[nodeName]) and (nodeName in self.pq.getNames()) ):
            self.pq.remove( (nodeName, self.calculateKeys(nodeName)) )

    def computeShortestPath(self):
        # While queue has elements in it AND the top element in queue is LT key or startNode/robotNode 
        # OR rhs_startNode > gValue_startNode
        while( ( (self.pq.queue) and self.pq.topKey() < self.calculateKeys(self.nodeStart) ) \
                or self.rhs[self.nodeStart] > self.gValue[self.nodeStart] ):
            tmpNode = self.pq.top()
            u = tmpNode[0]
            kOld = tmpNode[1]
            kNew = self.calculateKeys(u)

            if(kOld < kNew):
                self.pq.update( (u, (kNew[0], knew[1])) )
            elif (self.gValue[u] > self.rhs[u]):
                self.gValue[u] = self.rhs[u]
                self.pq.remove(tmpNode)

                # get predecessors
                for pred in self.getNeighbours(u):
                    if(pred != "G"):
                        alphaEdge = utils.getAlphaOrder(u, pred)
                        self.rhs[pred] = min( self.rhs[pred], self.edgeCost[alphaEdge] + self.gValue[u] )
                        self.updateVertex(pred)
            else:
                gOld = self.gValue[u]
                self.gValue[u] = float('inf')

                # get predecessors and current node itself
                predecessors = self.getNeighbours(u)
                predecessors.append(u)
                for pred in predecessors: # represented as s in paper
                    alphaEdge = utils.getAlphaOrder(u, pred)
                    if (rhs[pred] == self.edgeCost[alphaEdge] + gOld):
                        if(pred != "G"):
                            rhsList = []
                            # update rhs to be min of all successors
                            for succ in self.getNeighbours(pred): # represented as s' in paper
                                alphaEdge = utils.getAlphaOrder(pred, succ)
                                rhsList.append(self.edgeCost[alphaEdge] + self.gValues[succ])
                            self.rhs[pred] = min(rhsList)
                    self.updateVertex(pred)


if __name__ == "__main__":
    dlite = DStarLite()
    dlite.pq.display()

    dlite.computeShortestPath()

    while (dlite.nodeStart != dlite.nodeGoal):
        nextState  = "X"
        nextStateList = dlite.getNeighbours(dlite.nodeStart)
        nextStateCost = []
        for succ in nextStateList:
            alphaEdge = utils.getAlphaOrder(dlite.nodeStart, succ)
            nextStateCost.append(dlite.edgeCost[alphaEdge] + dlite.gValue[succ])
        idx = nextStateCost.index(min(nextStateCost))
        dlite.nodeStart = nextStateList[idx]

        # TODO: Scan the graph for changed edge costs
        # TODO: update edgeCosts and prevEdgeCosts

        if (dlite.edgeCost != dlite.prevEdgeCost):
            
            # Update km
            newHeuristic = dlite.getHeuristics[dlite.nodePrev]
            dlite.km = dlite.km + newHeuristic[dlite.nodePrev]
            dlite.nodePrev = dlite.nodeStart

            # Update source nodes of all changed edges
            # do stuff
            # do stuff







    #utils.testPriorityQueue()




















# Error in slides, First iteration, C's keys were wrong. They should be 3,1 was given as 3,2 in slides
# In first loop, should A get dequed? In mine, it does not, so make while condition >= in the OR case?



#utils.testPriorityQueue()