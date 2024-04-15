import simpy
import random

class Runner(object):
    def __init__(self, _env: simpy.Environment, resource: simpy.Resource, _id: int) -> None:
        self.total_distance = 0.0
        self.total_boost = 0.0
        self.total_rest = 0.0
        self.id = _id
        self.env = _env
        self.res = resource
        self.action = self.env.process(self.run())

    def run(self) -> None:
        while True:
            try:
                with self.res.request() as req:
                    print('The runner %d request boost at %.2f' % (self.id, self.env.now))
                    result = yield req | self.env.timeout(0.1)
                    if req in result:
                        print('The runner %d started running at %.2f' % (self.id, self.env.now))
                        energy_boost = abs(random.normalvariate(5,1))
                        # print("boost: %.2f" % energy_boost)
                        self.total_boost += energy_boost
                        yield self.env.timeout(energy_boost)
                        if random.random() < 0.3:
                            self.total_distance += energy_boost * 300
                        else:
                            self.total_distance += energy_boost * 600
                    else:
                        print("Runner %d got no boost this time" % self.id)
                print('The runner %d is walking at %.2f' % (self.id, self.env.now))
                recovery_time = abs(random.normalvariate(2,1))
                self.total_rest += recovery_time
                yield self.env.timeout(recovery_time)
                self.total_distance += recovery_time * 100
            except simpy.Interrupt:
                print("Runner %d got a cramp at %.2f" % (self.id, self.env.now))
                return

def crampGenerator(env: simpy.Environment, runner: Runner) -> None:
    if random.random() < 0.5:
        print("Runner %d will get a cramp" % runner.id)
        yield env.timeout(abs(random.normalvariate(12,1)))
        runner.action.interrupt()


env = simpy.Environment()
resource = simpy.Resource(env)
runner1 = Runner(env, resource, 1)
runner2 = Runner(env, resource, 2)
env.process(crampGenerator(env, runner1))
env.process(crampGenerator(env, runner2))
env.run(until=20)
print("The runner %d went for %.2f meters" % (runner1.id, runner1.total_distance))
print("The runner %d went for %.2f meters" % (runner2.id, runner2.total_distance))
# print("Total boost: %.2f, Total rest %.2f" % (runner.total_boost, runner.total_rest))