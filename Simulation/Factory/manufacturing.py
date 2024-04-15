import simpy
import random
from enum import Enum

class Debug(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4
    
class WrkStationStatus(Enum):
    START = 1
    IDLE = 2
    PRODUCING = 3
    RESTOCK = 4
    DOWN = 5
    STOP = 6
    
    def __str__(self):
        return str(self.name)
    
class ProductStatus(Enum):
    ORDERED = 1
    PRODUCING = 2
    DONE = 3
    FAIL = 4
    ABORT = 5
    INCOMPLETE = 6
    
    def __str__(self):
        return str(self.name)

class FactoryStatus(Enum):
    OPEN = 1
    CLOSED = 2
    SHUTDOWN = 3
    
    def __str__(self):
        return str(self.name)
    
TICKS_PER_DAY = 500 # Number of ticks that represent a day of production 
CLOSE_RATE = 0.01   # Probability of having a catastrophic accident and close that day
REJECT_RATE = 0.05  # Probability of rejecting a product at the end of the process
MAX_RAW_BIN = 25    # The max number of items each station will have at any given time
RESTOCK_UNITS = 3   # Number of restock units that the factory will have
RESTOCK_TIME = 2    # The average time units it takes the bus boy to restock a station
FIX_TIME = 3        # The average time for fixing the station
WORK_TIME = 4       # The average working time for the stations
WRK_STATIONS = 6    # Number of work stations in the factory
WRK_STATION_RATES = [0.2,0.1,0.15,0.05,0.07,0.1]    # Declared error rate of work stations
DEBUG_LEVEL = Debug.ERROR
       
def debugLog(level: Debug, msg: str, extra: str = "") -> None:
    if(level.value >= DEBUG_LEVEL.value):
        print(msg + (": " + extra if extra != "" else extra))

class Product(object):
    def __init__(self, id: int, env: simpy.Environment) -> None:
        self._status = ProductStatus.ORDERED
        self._id = id
        self._env = env
        self._currentStation = -1
        self._wrkStat = [False] * WRK_STATIONS
        self._wrkStatTime = [0] * WRK_STATIONS
        self._startClock = 0
        self._endClock = 0
    
    @property
    def status(self) -> ProductStatus:
        return self._status
    
    @status.setter
    def status(self, value: ProductStatus) -> None:
        self._status = value
        if(self._status == ProductStatus.PRODUCING and self._startClock == 0):
            self._startClock = self._env.now
            debugLog(Debug.DEBUG, 'The product %06d started production at %.2f' % (self._id, self._startClock))
        elif(self._status == ProductStatus.DONE or self._status == ProductStatus.FAIL or self._status == ProductStatus.ABORT):
            self._endClock = self._env.now
            debugLog(Debug.DEBUG, 'The product %06d finished production at %.2f' % (self._id, self._endClock), str(self._status))
        
    @property
    def processBy(self) -> int:
        return self._currentStation
    
    @processBy.setter
    def processBy(self, value: int) -> None:
        self._currentStation = value
        self._wrkStat[value] = True
        self._wrkStatTime[value] = self._env.now
        if(self._currentStation == 0):
            self.status = ProductStatus.PRODUCING
        debugLog(Debug.DEBUG, 'The product %06d received at workstation %02d at %.2f' % (self._id, (self._currentStation+1), self._wrkStatTime[value]))
        
    @property
    def isDone(self) -> bool:
        return all(self._wrkStat) and not self.isAborted
    
    @property
    def isAborted(self) -> bool:
        return self.status == ProductStatus.ABORT
    
    @property
    def nextStation(self) -> int:
        """Returns the next workstation that the product still has to visit

        Returns:
            int: The index of the next missing workstation
        """
        return next((i for i,v in enumerate(self._wrkStat) if not v), None)
    
    @property
    def prodTime(self) -> float:
        if(self._startClock == 0):
            return self._startClock
        elif(self._endClock == 0):
            return self._env.now - self._startClock
        return self._endClock - self._startClock
    
    def wasProccessedBy(self, id: int) -> bool:
        return self._wrkStat[id]
    
    def stopProduction(self, time: float) -> None:
        self._status = ProductStatus.INCOMPLETE
        self._endClock = time
            
class Workstation(object):
    def __init__(self, env: simpy.Environment, busBoy: simpy.Resource, id: int, errRate: float) -> None:
        self._id = id
        self._env = env
        self._busBoy = busBoy
        self._errRate = errRate
        self._binItems = MAX_RAW_BIN
        self._product = None
        self._unit = simpy.Resource(self._env)
        self._action = None
    
    @property
    def id(self) -> simpy.Process:
        return self._id + 1
    
    @property
    def action(self) -> simpy.Process:
        return self._action
    
    @action.setter
    def action(self, value) -> None:
        self._action = value
        
    @property
    def unit(self) -> simpy.Resource:
        return self._unit
    
    @property
    def product(self) -> Product:
        return self._product
    
    @product.setter
    def product(self, value: Product) -> None:
        self._product = value
        self._product.processBy = self._id
        
    def endProduction(self, time: float) -> None:
        debugLog(Debug.DEBUG, 'The workstation %d end day at %.2f' % (self.id, time))
        if self._product:
            self._product.stopProduction(time)
    
    def processProd(self) -> simpy.Process:
        try:
            # Check if I have enough items to work
            if(self._binItems == 0):
                with self._busBoy.request() as req:
                    debugLog(Debug.WARN, 'The workstation %d request restock at %.2f' % (self.id, self._env.now))
                    yield req 
                    # The resource is available
                    debugLog(Debug.DEBUG, 'The workstation %d request is being restocked at %.2f' % (self.id, self._env.now))
                    restock_time = abs(random.normalvariate(RESTOCK_TIME,1))
                    debugLog(Debug.DEBUG, "The workstation %d will take %.2f units of time to restock" % (self.id,restock_time))
                    yield self._env.timeout(restock_time)
                    self._binItems = MAX_RAW_BIN
                    debugLog(Debug.DEBUG, "The workstation %d was restocked at %.2f" % (self.id,self._env.now))
            # Check if there is the need to fix this work station
            if random.random() < self._errRate:
                debugLog(Debug.WARN, 'The workstation %d presented a failure at %.2f' % (self.id, self._env.now))
                fixing_time = abs(random.normalvariate(FIX_TIME,1))
                debugLog(Debug.DEBUG, "The workstation %d will take %.2f units of time to be fixed" % (self.id,fixing_time))
                yield self._env.timeout(fixing_time)
                debugLog(Debug.INFO, 'The workstation %d is back on line at %.2f' % (self.id, self._env.now))
            # Process the product
            self._binItems -= 1
            debugLog(Debug.DEBUG, 'The workstation %d starts processing product %06d at %.2f' % (self.id, self.product._id, self._env.now))
            working_time = abs(random.normalvariate(WORK_TIME,1))
            yield self._env.timeout(working_time)
            debugLog(Debug.DEBUG, 'The workstation %d is done processing prod %06d at %.2f' % (self.id, self.product._id, self._env.now))
        except simpy.Interrupt:
            debugLog(Debug.ERROR, "There was a catastrophic issue, %d at %.2f" % (self.id, self._env.now))
            self.product.status = ProductStatus.ABORT
        finally:
            self._product = None

class Factory(object):
    def __init__(self, env: simpy.Environment) -> None:
        self._env = env
        self._restockDevice = simpy.Resource(self._env, RESTOCK_UNITS)
        self._workstations = []
        self._storage = []
        self._status = FactoryStatus.OPEN
        # Create all the work stations
        for i in range(WRK_STATIONS):
            self._workstations.append(Workstation(self._env, self._restockDevice, i, WRK_STATION_RATES[i]))
            debugLog(Debug.DEBUG, "Ready %s" % self._workstations[i])
        self.action = self._env.process(self.produce())
        
    def __str__(self) -> str:
        output = "\n==========\nFactory %s" % (self._status)
        done = sum(1 for i in self._storage if i._status == ProductStatus.DONE)
        fail = sum(1 for i in self._storage if i._status == ProductStatus.FAIL)
        ordered = sum(1 for i in self._storage if i._status == ProductStatus.ORDERED)
        incomplete = sum(1 for i in self._storage if i._status == ProductStatus.INCOMPLETE)
        output += "\nTotal orders planned: %d" % (len(self._storage))
        output += "\nProduced %d items today, but %d failed quality inspection." % (done, fail)
        output += "\nOrders left planned: %d \tOrders left on floor: %d" % (ordered, incomplete)
        if(self._status == FactoryStatus.SHUTDOWN):
            abort = sum(1 for i in self._storage if i._status == ProductStatus.ABORT)
            output += "\nOrders aborted due shutdown: %d" % (abort)
        if(DEBUG_LEVEL.value == Debug.DEBUG):
            prod = sum(1 for i in self._storage if i._status == ProductStatus.PRODUCING)
            output += "\tErr: %d" % (prod)
            for prd in self._storage:
                if prd._status == ProductStatus.PRODUCING:
                    output += "\n%s" % str(prd)
        return output
    
    def getWorkstation(self, index : int) -> Workstation:
        return self._workstations[index]
    
    def orderProduct(self, id: int) -> simpy.Process:
        if(self._status == FactoryStatus.CLOSED):
            return
        prod = Product(id, self._env)
        self._storage.append(prod)
        while not prod.isDone:
            idx = prod.nextStation
            # Check the situation of parallel stations
            if(idx == 3):   # station 4
                if(not prod.wasProccessedBy(4) and self.getWorkstation(idx).unit.count > self.getWorkstation(idx+1).unit.count):
                    idx += 1
            debugLog(Debug.DEBUG, "Product %06d to be processed by WS %02d" % (prod._id, (idx+1)))
            station = self.getWorkstation(idx)
            with station.unit.request() as wrkProcess:
                yield wrkProcess
                station.product = prod
                station.action = yield self._env.process(station.processProd())
        if not prod.isAborted:
            if random.random() < REJECT_RATE:
                prod.status = ProductStatus.FAIL
            else:
                prod.status = ProductStatus.DONE
        
    def produce(self) -> simpy.Process:
        i = 0
        # for i in range(5):
        while True:
            self._env.process(self.orderProduct(i+1))
            yield self._env.timeout(0.1)
            i += 1
          
    def shutDown(self) -> None:
        if random.random() < CLOSE_RATE:
            closing_in = abs(random.normalvariate(12,1))
            debugLog(Debug.INFO, "Factory will close today in %d units." % closing_in)
            yield self._env.timeout(closing_in)
            # Interrupt all actions when catastrophic event triggers.
            map(lambda s: s.action.interrupt(), self._workstations)
            debugLog(Debug.ERROR, "Factory closed at %.2f." % self._env.now) 
            self._status = FactoryStatus.SHUTDOWN
            for prd in self._storage:
                if prd._status == ProductStatus.PRODUCING:
                    prd.status = ProductStatus.ABORT
        else:
            debugLog(Debug.INFO, "Factory will be accident free today.")
    
    def closeDown(self, time: float) -> None:
        if self._status != FactoryStatus.SHUTDOWN:
            self._status = FactoryStatus.CLOSED
            # map(lambda s: s.endProduction(time), self._workstations)
            [w.endProduction(time) for w in self._workstations]
            for prd in self._storage:
                    if prd._status == ProductStatus.PRODUCING:
                        prd.stopProduction(time)
            debugLog(Debug.INFO, "Factory closed at %.2f." % time) 


def main() -> None:
    env = simpy.Environment()
    factory = Factory(env)
    env.process(factory.shutDown())
    env.run(until=TICKS_PER_DAY)
    factory.closeDown(TICKS_PER_DAY)
    print(factory)
    
if __name__ == '__main__':
    main()