import random
import simpy
from simulation.config import *
from assets.status import Status
from assets.customer import Customer
from assets.monitored_resource import MonitoredResource


class SimSystem:
    """ A class used to represent a simulation system.

        It will hold all the information regarding the simulation. This is where we implement the model

        Attributes
        ----------
        _name : str
            The name of the simulation
        env : simpy.Environment
            The simulation environment created by simpy
        customers : list
            A list of the entities participating in the simulation

        Methods
        -------
        log_event(MonitoredResource, Customer) -> None
            Logs an event in the customer object and the series of queues
        source(int, int, MonitoredResource) -> simpy.Process
            Generates customers randomly
        gen_customer(int, MonitoredResource, float) -> simpy.Process
            This is the method that models the interaction of the gen_customer with the system.
        run() -> (list, MonitoredResource, float)
            Executes the simulation
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self.env = simpy.Environment()  # Create the simpy Environment that will run the whole simulation
        self.customers = []             # The list of the customers in the system

    def log_event(self, res: MonitoredResource, customer: Customer) -> None:
        """ Log to the output the information regarding the state of the system in a given event.

            This is where we are capturing all the information that we will later analyze.

            Parameters
            ----------
            res : simpy.Resource
                The resource that we are using
            customer : Customer
                The gen_customer object
        """
        # Flag to show either queue or event information. Right now it is either of them, not both.
        step_step = True
        time = self.env.now
        msg = '%8.4f %s | ' % (time, customer)
        if customer.status == Status.WAIT:
            if customer.wait == -1:  # When the gen_customer just arrives
                customer.arrive = time
                msg += 'Arrived  - Here I am'
                res.enqueue(time, customer)
            else:  # When the gen_customer is ready to be served
                customer.serve = time
                msg += 'Serving now. Waited %6.3f' % customer.wait
                res.give_service(time, customer)
        elif customer.status == Status.SUCCESS:  # When the gen_customer was successfully served
            customer.leave = time
            msg += 'Finished - Bye!'
            res.dequeue(time, customer)
        elif customer.status == Status.RENEGED:  # When the gen_customer leaves without being served
            customer.leave = time
            msg += 'RENEGED after %5.3f' % customer.wait
            res.dequeue(time, customer)
        if REPORT_STEP_BY_STEP:
            print(msg)
        if REPORT_QUEUE:
            # This is the actual resource queue. Print only for debug purposes
            # print('%8.4f %s | %s' % (time, gen_customer, res.print_stats()))
            print('%8.4f %s | %s' % (time, customer, res))

    def source(self, number: int, interval: int, m_res: MonitoredResource) -> simpy.Process:
        """Generates customers randomly

            Parameters
            ----------
            number : int
                The number of customers that will be created
            interval : int
                The average interval of new gen_customer creation
            m_res : MonitoredResource
                The resource that represents the serving employee(s)

            Returns
            -------
            simpy.Process
                A gen_customer object that will be processed by the environment
        """
        for i in range(number):
            c = self.gen_customer(i, m_res, TIME_IN_BANK)
            self.env.process(c)
            # Time between gen_customer arrival
            t = random.expovariate(1.0 / interval)
            yield self.env.timeout(t)

    def gen_customer(self, name: int, m_res: MonitoredResource, time_in_bank: float) -> simpy.Process:
        """Customer arrives, is served and leaves.

            This is the method that models the interaction of the gen_customer with the system. This is also
            where we log all the information we will use later to analyze.

            Parameters
            ----------
            name : int
                The number of gen_customer that will be created
            m_res : MonitoredResource
                The resource that represents the serving employee(s)
            time_in_bank : float
                The maximum length of any service

            Returns
            -------
            simpy.Process
                A gen_customer object that will be processed by the environment
        """
        c = Customer(name)
        self.customers.append(c)

        with m_res.get_resource().request() as req:
            self.log_event(m_res, c)
            # Wait for the counter or abort at the end of our tether
            results = yield req | self.env.timeout(c.patience)
            c.wait = self.env.now - c.arrive

            if req in results:
                # We got to the counter
                self.log_event(m_res, c)
                # random value for service time
                tib = random.expovariate(1.0 / time_in_bank)
                yield self.env.timeout(tib)
                c.status = Status.SUCCESS
            else:
                # We reneged
                c.status = Status.RENEGED
        self.log_event(m_res, c)

    def run(self) -> (list, MonitoredResource, float):
        """Prepares and executes the simulation.

            Returns
            -------
            list
                The list of the customers in the system
            MonitoredResource
                The resource that represents the queues in the system
            float
                The total time of the simulation
        """
        # Setup and start the simulation
        print(self._name)
        if RANDOM_SEED != -1:
            random.seed(RANDOM_SEED)  # Set the seed for the randomness in the simulation
        else:
            random.seed()

        # Start processes and run
        start_time = self.env.now
        counter = MonitoredResource('counter', simpy.Resource(self.env, CAPACITY))
        self.env.process(self.source(NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
        self.env.run()
        end_time = self.env.now
        print('Total simulation time: %8.3f' % (end_time - start_time))
        return self.customers, counter, end_time - start_time
