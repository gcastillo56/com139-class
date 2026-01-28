import simpy
from .customer import Customer


class MonitoredResource:
    """ A wrapper class used to gather information on the resources used.

        It will hold readable information regarding the status of the resource.
        It will also hold information regarding the analysis of the object overtime.

        Attributes
        ----------
        _name : str
            The name of the resource
        _res : simpy.Resource
            The simpy resource that interacts with the simpy library
        in_service : list
            The list that will represent the resource being in use
        queue : list
            The list that will represent the waiting queue in the system.py
        in_service_event : list
            The list of the events occurring in the in_service list. The elements will have event time and size of queue
        queue_event : list
            The list of the events occurring in the queue list . The elements will have event time and size of queue

        Methods
        -------
        get_resource() -> simpy.Resource
            Returns the simpy Resource object related to this resource
        print_stats() -> str
            Returns a string with the string representation of the current status of the simpy.Resource object
        enqueue(mr_cust: Customer) -> None
            Adds a new customer to the queue or to the service if it is available
        give_service(mr_cust: Customer) -> None
            Sets the customer as the next to be served
        dequeue(mr_cust: Customer) -> None
            Removes the customer from all queues
        report_event(time: float, lst: list) -> dict
            Will create the record of the moment an event occurs in any of our lists
   """

    def __init__(self, name: str, res: simpy.Resource) -> None:
        """ Creates a new Monitored Resource object.

            This is just a wrapper for the simpy resource object for reporting and debugging purposes

            Parameters
            -------
            name : str
                The name of the resource to differentiate between them
            res : simpy.Resource
                The actual simpy resource we will be monitoring
        """
        self._name = name
        self._res = res
        self.in_service = []
        self.queue = []
        self.in_service_event = []
        self.queue_event = []

    def __str__(self) -> str:
        """ Print the status of the parallel queues structures

            Returns
            -------
            str
                A string with the data of the mirror lists we use to represent the state of the queues
        """
        queues = lambda x: str(x)
        return ('%s | %d of %d slots are allocated. | Users: %s  | Queued events: %s'
                % (self._name, len(self.in_service), self._res.capacity,
                   list(map(queues, self.in_service)), list(map(queues, self.queue))))

    def get_resource(self) -> simpy.Resource:
        """ Returns the simpy resource object

            Returns
            -------
            simpy.Resource
                The actual simpy resource object
        """
        return self._res

    def print_stats(self) -> str:
        """ Print the status of the actual resource object

            Returns
            -------
            str
                The information of the status of the Resource queues
        """
        return ('%d of %d slots are allocated. | Users: %s  | Queued events: %s'
                % (self._res.count, self._res.capacity, str(self._res.users), str(self._res.queue)))

    def enqueue(self, time: float, mr_cust: Customer) -> None:
        """ Add to a queue, either to the service one if available or to the queue

            Parameters
            ----------
            time: float
                The time the event is occurring
            mr_cust : Customer
                The gen_customer object
        """
        if len(self.in_service) < self._res.capacity:  # If can service right away, do so
            self.give_service(time, mr_cust)
        elif mr_cust not in self.queue:  # If can't service, enqueue
            self.queue.append(mr_cust)
            self.queue_event.append(self.report_event(time, self.queue))

    def give_service(self, time: float, mr_cust: Customer) -> None:
        """ Assign the gen_customer to the in_service list

            Parameters
            ----------
            time: float
                The time the event is occurring
            mr_cust : Customer
                The gen_customer object
        """
        if mr_cust in self.queue:  # If waiting, remove from queue
            self.queue.remove(mr_cust)
            self.queue_event.append(self.report_event(time, self.queue))
        if mr_cust not in self.in_service:
            self.in_service.append(mr_cust)
            self.in_service_event.append(self.report_event(time, self.in_service))

    def dequeue(self, time: float, mr_cust: Customer) -> None:
        """ Remove from all the queues, either by success or renege

            Parameters
            ----------
            time: float
                The time the event is occurring
            mr_cust : Customer
                The gen_customer object
        """
        if mr_cust in self.in_service:  # Successful execution
            self.in_service.remove(mr_cust)
            self.in_service_event.append(self.report_event(time, self.in_service))
        elif mr_cust in self.queue:  # Renege after timing out
            self.queue.remove(mr_cust)
            self.queue_event.append(self.report_event(time, self.queue))

    def report_event(self, time: float, lst: list) -> dict:
        """ Creates the entry for the event recording

            Parameters
            ----------
            time: float
                The time the event is occurring
            lst: list
                The list whose change will be recorded

            Returns
            -------
            dict
                A dictionary with the values required to record the event
        """
        return {'time': time, 'value': len(lst)}
