import simpy
import random

class Runner(object):
    def __init__(self, _env: simpy.Environment, _id: int) -> None:
        self.total_distance = 0.0
        self.total_boost = 0.0
        self.total_rest = 0.0
        self.id = _id
        self.env = _env
        self.env.process(self.run())

    def run(self) -> None:
        while True:
            print('The runner %d started running at %.2f' % (self.id, self.env.now))
            energy_boost = abs(random.normalvariate(5))
            # print("boost: %.2f" % energy_boost)
            self.total_boost += energy_boost
            yield self.env.timeout(energy_boost)
            self.total_distance += energy_boost * 600
            
            print('The runner %d got tired and now is waking at %.2f' % (self.id, self.env.now))
            recovery_time = abs(random.normalvariate(2))
            # print("recovery: %.2f" % recovery_time)
            self.total_rest += recovery_time
            yield self.env.timeout(recovery_time)
            self.total_distance += recovery_time * 100
        
env = simpy.Environment()
runner1 = Runner(env, 1)
runner2 = Runner(env, 2)
env.run(until=20)
print("The runner %d went for %.2f meters" % (runner1.id, runner1.total_distance))
print("The runner %d went for %.2f meters" % (runner2.id, runner2.total_distance))
# print("Total boost: %.2f, Total rest %.2f" % (runner.total_boost, runner.total_rest))