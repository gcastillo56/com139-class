"""
Bank renege example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""
import random
import simpy
from Single_Server.assets.status import Status
from Single_Server.assets.customer import Customer
from Single_Server.assets.monitored_resource import MonitoredResource
from Single_Server.config import *
from Single_Server.analysis.analyzer import *

customers = []              # The list of the customers in the system


def log_event(env: simpy.Environment, res: MonitoredResource, customer: Customer) -> None:
    """ Log to the output the information regarding the state of the system in a given event.

        This is where we are capturing all the information that we will later analyze.

        Parameters
        ----------
        env : simpy.Environment
            The environment holding the simulation's information
        res : simpy.Resource
            The resource that we are using
        customer : Customer
            The gen_customer object
    """
    # Flag to show either queue or event information. Right now it is either of them, not both.
    step_step = True
    time = env.now
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
    if step_step:
        print(msg)
    else:
        # This is the actual resource queue. Print only for debug purposes
        # print('%8.4f %s | %s' % (time, gen_customer, res.print_stats()))
        print('%8.4f %s | %s' % (time, customer, res))


def source(env: simpy.Environment, number: int, interval: int, m_res: MonitoredResource) -> simpy.Process:
    """Source generates customers randomly

        Parameters
        ----------
        env : simpy.Environment
            The environment holding the simulation's information
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
        c = gen_customer(env, i, m_res, TIME_IN_BANK)
        env.process(c)
        # Time between gen_customer arrival
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def gen_customer(env: simpy.Environment, name: int, m_res: MonitoredResource, time_in_bank: float) -> simpy.Process:
    """Customer arrives, is served and leaves.

        This is the method that models the interaction of the gen_customer with the system. This is also
        where we log all the information we will use later to analyze.

        Parameters
        ----------
        env : simpy.Environment
            The environment holding the simulation's information
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
    customers.append(c)

    with m_res.get_resource().request() as req:
        log_event(env, m_res, c)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(c.patience)
        c.wait = env.now - c.arrive

        if req in results:
            # We got to the counter
            log_event(env, m_res, c)
            # random value for service time
            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            c.status = Status.SUCCESS
        else:
            # We reneged
            c.status = Status.RENEGED
    log_event(env, m_res, c)


# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)  # Set the seed for the randomness in the simulation
env = simpy.Environment()  # Create the simpy Environment that will run the whole simulation

# Start processes and run
start_time = env.now
counter = MonitoredResource('counter', simpy.Resource(env, CAPACITY))
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
end_time = env.now
print('Total simulation time: %8.3f' % (end_time - start_time))

report_customers = True
# Report all the values of the customers
if report_customers:
    print_obj_list(customers, 'report')
    print('Max wait: %5.3f' % get_max_obj(customers, 'wait'))
    print('Mean wait: %5.3f' % get_mean_obj(customers, 'wait'))
    print('Median wait: %5.3f' % get_median_obj(customers, 'wait'))
    print('Mode wait: %5.3f' % get_mode_obj(customers, 'wait'))
    print('Stdev wait: %5.3f' % get_stdev_obj(customers, 'wait'))
    print('Variance wait: %5.3f' % get_variance_obj(customers, 'wait'))
    max_time = get_max_obj(customers, 'total_time')
    min_time = get_min_obj(customers, 'total_time')
    print('Max time: %5.3f by %s' % (max_time, objects_as_str(get_matching_value_obj(customers, 'total_time', max_time))))
    print('Min time: %5.3f by %s' % (min_time, objects_as_str(get_matching_value_obj(customers, 'total_time', min_time))))

report_ts = False
# Report the events in the queue
if report_ts:
    print_ts(counter.in_service_event, "Service")
    print_ts(counter.queue_event, "Queue")
    print('Min queue: %4.3f' % get_min_ts(counter.queue_event))
    print('Max queue: %4.3f' % get_max_ts(counter.queue_event))

