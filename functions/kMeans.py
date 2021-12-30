# Verson 1.5
# D. Kofler 2021

from matplotlib import pyplot as plt
import numpy, random, math

def createRandomDatapoints(amount, dimentionality): # creates random datapoints
    E = []
    pt = []

    for a in range(amount):
        pt.clear()
        for d in range(dimentionality):
            pt.append(random.randint(0,100))
        E.append(tuple(pt))
    
    return E


def euclideanDistance(dataPoint1, dataPoint2): # calculates euclidean distance
    pts = []
    
    dim = len(dataPoint1) #dimensionality of the data points

    for d in range(dim):
        pts.append((dataPoint1[d],dataPoint2[d]))

    sumSquares = 0
    for i,p in enumerate(pts):
        sumSquares += (p[1] - p[0]) ** 2

    return round(math.sqrt(sumSquares),2)


def AssignClusters(dataPoints, clusterAmount, optimize): # assigns datapoints to clusters using a k-Means algorithm
    C = []
    L = {}
    E = dataPoints
    k = clusterAmount

    dim = len(E[0]) #dimensionality of the data points

    def selectRandomCenters(k): # returns k random data points from all data points E
        return random.sample(E, k)

    # Choose random datapoints as starting cluster centers
    C = selectRandomCenters(k)

    def argminDistance(dataPoint): # returns index of closest cluster for a given datapoint
        minDistCenter = C[0]
        minDist = euclideanDistance(dataPoint,minDistCenter)

        for c in C:
            dist = euclideanDistance(dataPoint,c)
            if dist < minDist:
                minDist = dist
                minDistCenter = c
                
        return C.index(minDistCenter)

    # Find closest cluster for each datapoint
    for e in E:
        L[e] = argminDistance(e)

    def UpdateCluster(c): # moves given cluster to mean position of its current corresponding datapoints
        pts = []

        for l in L:
            if C[L[l]] == c:
                pts.append(l)

        sums = []
        newPosList = []

        for d in range(dim):
            sums.append(0)
            
            for p in pts:
                sums[d] += p[d]

            if sums[d] == 0:
                newPosList.append(50)
            else:
                newPosList.append(round(sums[d] / len(pts), 2))

        return tuple(newPosList)

    # optimize cluster-positions
    iter = 0
    maxIters = 100

    while optimize:
        changed = False

        # Update clusters
        for i,c in enumerate(C):
            C[i] = UpdateCluster(c)

        # Update minDist
        for e in E:
            minDist = euclideanDistance(e,C[argminDistance(e)])

            if minDist != euclideanDistance(e,C[L[e]]):
                L[e] = argminDistance(e)
                changed = True

        iter += 1

        if not changed or iter > maxIters:
            break
    
    ResDict = {}
    for l in L:
        ResDict[l] = C[L[l]]

    return ResDict


def findOptimalClusterAmount(E): # finds the optimal amount of clusters using the WCSS-method
    
    assinments = {}
    wcssDict = {}
    for i in range(2, 11): #try with up to 10 clusters
        assinments.clear()
        assinments = AssignClusters(E, i, True)

        wcss = 0
        for e in E:
            wcss += int(euclideanDistance(e, assinments[e]) ** 2)

        wcssDict[i] = wcss

        if i == 2:
            optimalClusterAmount = 10
        else:
            if optimalClusterAmount == 10 and wcssDict[i - 1] - wcss < wcssDict[2] / 10:
                optimalClusterAmount = i - 1

    print('Optimal number of clusters (change in WCSS < 10%): ' + str(optimalClusterAmount))

    X = []
    Y = []

    for w in wcssDict:
            X.append(w)
            Y.append(wcssDict[w])   

    plt.plot(X, Y, c = 'k')
    plt.title('Within Cluster Sum of Squares')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

    return optimalClusterAmount


def plotClusters(assignmentDict): # creates 2D or 3D plots of clusters and their assigned datapoints
    dataPoints = []
    clusterCenters = []

    for a in assignmentDict: 
        if (a not in dataPoints): #get data points from dict
            dataPoints.append(a)

        if (assignmentDict[a] not in clusterCenters): #get cluster centers from dict
            clusterCenters.append(assignmentDict[a])     

    dim = len(dataPoints[0]) #dimensionality of the data points
    if dim > 3:
        return

    clusterColors = {}

    for c in clusterCenters: #assign random colors to each cluster
        numbers = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        clusterColors[c] = '#' + ''.join('{:02X}'.format(n) for n in numbers)

    pts = []
    dataPointsPlot = []

    fig = plt.figure(figsize=(10,10))
    if (dim == 3):
        ax = fig.add_subplot(projection='3d')

    for i,c in enumerate(clusterCenters):
        pts.clear()
        dataPointsPlot.clear()

        for a in assignmentDict: # get datapoints assigned to current cluster
            if assignmentDict[a] == c:
                pts.append(a)

        for d in range(dim):
            dataPointsPlot.append([])
            for p in pts:   
                dataPointsPlot[d].append(p[d])

        #plot
        match dim:
            case 1: ##not working yet
                plt.scatter(c[0], s = 200, c = clusterColors[c], marker = 'x')
                plt.scatter(dataPointsPlot[0], s = 30, c = dataPointsPlot[c], marker = 'o')
            case 2:
                plt.scatter(c[0], c[1], s = 200, c = clusterColors[c], marker = 'x')
                plt.scatter(dataPointsPlot[0], dataPointsPlot[1], s = 30, c = clusterColors[c], marker = 'o')
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title('2D k-Means-clustering')

            case 3:
                ax.scatter(c[0], c[1], c[2], s = 200, c = clusterColors[c], marker = 'x', alpha = 1, depthshade = False)
                ax.scatter(dataPointsPlot[0], dataPointsPlot[1], dataPointsPlot[2], s = 30, c = clusterColors[c], marker = 'o', alpha = 1, depthshade = False)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
                plt.title('3D k-Means-clustering')

    plt.show()