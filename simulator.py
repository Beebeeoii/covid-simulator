from random import randint
import math
import matplotlib.pyplot as plt

MIN_X = 0
MAX_X = 1000
MIN_Y = 0
MAX_Y = 1000

TOTAL_DAYS = 10
DAYS_OF_CONTAGION = 0.02
DAYS_TO_RECOVER = 0.04
INTERVAL_SECONDS = 10

INFECTION_DISTANCE = 20
INFECTION_FROM_SICK_CHANCE = 0.5
INFECTION_FROM_CONTAGIOUS_CHANCE = 0.3

BOUNDARY_DISTANCE = 2

class Health:
    def __init__(self, status):
        self.status = status
    
    def getColour(self):
        if self.status == 0:
            return "g"
        elif self.status == 1:
            return "y"
        elif self.status == 2:
            return "r"
        elif self.status == 3:
            return "b"
        else:
            raise ValueError("Invalid health status")

class Point:
    def __init__(self, x, y):
        if x < 0 or x > 1000:
            raise ValueError(f"X must be between {MIN_X} and {MAX_X}!")
        if y < 0 or y > 1000:
            raise ValueError(f"Y must be between {MIN_Y} and {MAX_Y}!")
        self.x = x
        self.y = y

class Velocity:
    def __init__(self, speed, direction):
        if speed > 0.2 or speed < 0.1:
            raise ValueError("Magnitude must be between 0.1 and 0.2!")
        self.speed = speed
        self.direction = direction
    
    def getXVelocity(self):
        return self.speed * math.cos(math.radians(self.direction))

    def getYVelocity(self):
        return self.speed * math.sin(math.radians(self.direction))

# bad function but required by instructions
def distanceFromBoundary(person, threshold):
    wallNo = 0

    distanceXStart = person.position.x - MIN_X
    distanceXEnd = MAX_X - person.position.x
    distanceYStart = person.position.y - MIN_Y
    distanceYEnd = MAX_Y - person.position.y

    # bad code: better to put 4 distances in array, then sort, then get the index which represents the wall
    if distanceXStart < distanceXEnd: #closer to wall 2 than wall 0
        if distanceYStart < distanceYEnd: #closer to wall 3 than wall 1
            wallNo = 2 if distanceXStart < distanceYStart else 3
        else: #closer to wall 1 than wall 3
            wallNo = 2 if distanceXStart < distanceYEnd else 1
    else: #closer to wall 0 than wall 2
        if distanceYStart < distanceYEnd: #closer to wall 3 than wall 1
            wallNo = 0 if distanceXEnd < distanceYStart else 3
        else: #closer to wall 1 than wall 3
            wallNo = 0 if distanceXEnd < distanceYEnd else 1
    
    distance = min(distanceXStart, distanceXEnd, distanceYStart, distanceYEnd)

    if distance < threshold:
        return randint((wallNo + 1) * 90, (wallNo + 1) * 90 + 180)

    return person.velocity.direction

def calculateDistance(person1, person2):
    return ((abs(person1.position.x - person2.position.x)) ** 2 + (abs(person1.position.y - person2.position.y)) ** 2) ** 0.5

class Person:
    def __init__(self, health, position, velocity):
        self.health = health
        self.position = position
        self.velocity = velocity
        self.timeOfInfection = None
    
    def isInfectious(self):
        return True if self.health.status == 1 or self.health.status == 2 else False

nPerson = int(input("Input number of people 50<=n<=100\n"))
people = []

for i in range(nPerson):
    initialX = randint(MIN_X, MAX_X)
    initialY = randint(MIN_Y, MAX_Y)
    initialV = (randint(10, 20) / 100.0)
    initialT = randint(0, 360)

    if (i == nPerson - 1):
        sick = Person(Health(2), Point(initialX, initialY), Velocity(initialV, initialT))
        sick.timeOfInfection = 0
        people.append(sick)
        break

    people.append(Person(Health(0), Point(initialX, initialY), Velocity(initialV, initialT)))

# for p in people:
#     # print(p.position, p.velocity)
#     plt.plot([p.position.x], [p.position.y], f"{p.health.getColour()}o")

for time in range(0, TOTAL_DAYS * 24 * 60 * 60, INTERVAL_SECONDS):
    healthStatus = [0, 0, 0, 0]
    for p in people:
        # health update
        if (p.isInfectious()):
            if (time - p.timeOfInfection) >= DAYS_TO_RECOVER * 24 * 60 * 60:
                p.health = Health(3)
            elif (time - p.timeOfInfection) >= DAYS_OF_CONTAGION * 24 * 60 * 60:
                p.health = Health(2)
        else:
            for p1 in people:
                if p != p1 and p1.isInfectious():
                    if calculateDistance(p, p1) < INFECTION_DISTANCE:
                        if (randint(0, 100) / 100) < INFECTION_FROM_SICK_CHANCE if p1.health.status == 2 else INFECTION_FROM_CONTAGIOUS_CHANCE:
                            p.health = Health(1)
                            p.timeOfInfection = time
        
        healthStatus[p.health.status] += 1

        # print(p.velocity.direction, p.position.x, p.position.y)
        p.velocity = Velocity(p.velocity.speed, distanceFromBoundary(p, BOUNDARY_DISTANCE))
        
        newX = p.position.x + p.velocity.getXVelocity() * INTERVAL_SECONDS
        newY = p.position.y + p.velocity.getYVelocity() * INTERVAL_SECONDS

        # print(p.velocity.direction, newX, newY)

        p.position = Point(newX, newY)

        plt.plot([p.position.x], [p.position.y],  f"{p.health.getColour()}o")

    
    plt.title("Human Space")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis([0, 1000, 0, 1000])
    plt.text(0, 0, f"Healthy: {healthStatus[0]}\nInfected: {healthStatus[1]}\nSick: {healthStatus[2]}\nRecovered: {healthStatus[3]}\n\nTime (s): {time}")

    plt.draw()
    plt.pause(0.0000001)
    plt.clf()