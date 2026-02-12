import simpy
import random
import typing

MIN_PATIENCE = 1.0
MAX_PATIENCE = 4.0
SERVICE_TIME = 5.0

customer_queue = []

class Customer:
    def __init__(self, env: simpy.Environment, id: int, 
                 teller: simpy.PreemptiveResource, chairs: simpy.Container):
        self._env = env
        self._id = id
        self._teller = teller
        self._chairs = chairs
        self._patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        self._action = self._env.process(self.run())
        vip = random.uniform(0,1)
        self._vip = vip > 0.5
        if self._vip:
            print(f"{self} is a VIP customer and will be served first!")
        customer_queue.append(self)
        self._meta = {
            "id": self._id,
            "vip": self._vip,
            "patience": self._patience,
            "arrival_time": None,
            "service_time": None,
            "departure_time": None,
            "heckled": False,
            "interrupted": False,
            "in_bank": True
        }

    def __str__(self) -> str:
        return f"Customer {self._id}"
    
    @property
    def life(self) -> simpy.Process:
        return self._action

    def run(self) -> typing.Generator:
        """Method that controls the waiting of the customer in the bank.
        """
        remain = False
        self._meta["arrival_time"] = self._env.now
        print(f"{self} arrived at {self._meta["arrival_time"]} he has a patience of {self._patience}")
        if self._chairs.level == 0:
            print(f"{self} found no chairs and leaves immediately at {self._env.now}  <===")
            customer_queue.pop(customer_queue.index(self))
            self._meta["in_bank"] = False
            return
        try:
            with self._teller.request(priority=0 if self._vip else 1) as request:
                yield self._chairs.get(1)
                result = yield request | self._env.timeout(self._patience)
                if request in result: # type: ignore
                    try:
                        customer_queue.pop(customer_queue.index(self))
                        yield self._chairs.put(1)
                        self._meta["service_time"] = self._env.now
                        print(f"{self} starts being served at {self._meta["service_time"]}")
                        yield env.timeout(SERVICE_TIME)
                        
                        self._meta["departure_time"] = self._env.now
                        print(f"{self} leaves at {self._meta["departure_time"]}")
                    except simpy.Interrupt:
                        self._meta["interrupted"] = True
                        self._meta["departure_time"] = self._env.now
                        print(f"{self} was interrupted while being served and leaves at {self._meta["departure_time"]}")
                else:
                    self._meta["departure_time"] = self._env.now
                    print(f"{self} was impatient and left at {self._meta["departure_time"]}  <===")
        except simpy.Interrupt:
            self._meta["heckled"] = True
            punching_chance = random.uniform(0,1)
            if(punching_chance < 0.2):
                print(f"{self} punches the heckler and remains in line.")
                remain = True
            else:
                self._meta["departure_time"] = self._env.now
                print(f"{self} leaves scared at {self._meta["departure_time"]}")
        try:
            customer_queue.pop(customer_queue.index(self))
            yield self._chairs.put(1)
        except ValueError:
            pass
        if remain:
            self.remain()

    def remain(self):
        customer_queue.append(self)
        self._action = self._env.process(self.run())


class Heckler:
    def __init__(self, env: simpy.Environment, id: int):
        self._env = env
        self._id = id
        self._yelling = abs(random.normalvariate(2))
        self._env.process(self.run())

    def __str__(self) -> str:
        return f"Heckler {self._id}"
    
    def run(self) -> typing.Generator:
        print(f"{self} arrived at {self._env.now} he will yell in {self._yelling}")
        yield env.timeout(self._yelling)
        if(len(customer_queue) > 0):
            rando_customer_idx = random.randrange(len(customer_queue))
            terrified_customer = customer_queue[rando_customer_idx]
            print(f"{self} yells ininteligible things and scares {terrified_customer}!")
            terrified_customer.life.interrupt()
            print(f"{self} leaves proud of himself.")
        else:
            print(f"{self} leaves sad of not scaring a soul!")

all_customers = []

def customer_creation(env: simpy.Environment, teller: simpy.PreemptiveResource, chairs: simpy.Container):
    customer_id = 0
    while True:
        customer = Customer(env, customer_id, teller, chairs)
        all_customers.append(customer)
        time_for_next = random.expovariate(1/4)
        print(f"Time until next customer: {time_for_next}")
        yield env.timeout(time_for_next)
        customer_id += 1

# Define a function that create hecklers. Appear every 5 units
def heckler_creation(env):
    heckler_id = 0
    while True:
        heckler_id += 1
        Heckler(env, heckler_id)
        yield env.timeout(5)

env = simpy.Environment()
tellers = simpy.PreemptiveResource(env, capacity=1)
chairs = simpy.Container(env, init=5, capacity=5)
env.process(customer_creation(env, tellers, chairs))

#env.process(heckler_creation(env))

env.run(until=60)

for customer in all_customers:
    print(customer._meta)