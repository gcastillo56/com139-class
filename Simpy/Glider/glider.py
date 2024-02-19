import simpy
import random

class Glider(object):
    def __init__(self, id: int, env: simpy.Environment, boost: simpy.Resource) -> None:
        self.env = env
        self.fly_distance = 0.0
        self.id = id
        self.boost = boost
        
        self.action = self.env.process(self.glide())


    def glide(self) -> None:
        while True:
            try:
                print('I am gliding (Glider %d) starting at %.2f' % (self.id, self.env.now))
                gliding_time = abs(random.normalvariate(4))
                print("Will glide (Glider %d): %.2f" % (self.id, gliding_time))
                factor = 1
                if gliding_time >= 3:
                    with self.boost.request() as req:
                        yes = yield req | self.env.timeout(0.01)
                        if req in yes:
                            print("***** Boost (Glider %d) *****" % self.id)
                            factor = 1.2
                        else:
                            print("+++++ No Boost (Glider %d) +++++" % self.id)
                        yield self.env.timeout(gliding_time)
                else:
                    yield self.env.timeout(gliding_time)
                self.fly_distance += (gliding_time * factor)

                # print('Wind is gone at %.2f' % self.env.now)
                no_wind_time = abs(random.normalvariate())
                print("No wind (Glider %d): %.2f" % (self.id, no_wind_time))
                yield self.env.timeout(no_wind_time)
            except simpy.Interrupt:
                print("----- Glider %d down at %.2f ------" % (self.id, self.env.now))
                return

def netShooter(env: simpy.Environment, glider: Glider):
    shoot_time = abs(random.normalvariate(15))
    print('>>>>  Shooting in %.2f  <<<<' % shoot_time)
    yield env.timeout(shoot_time)
    glider.action.interrupt()


env = simpy.Environment()
booster = simpy.Resource(env, 1)
glider1 = Glider(1, env, booster)
glider2 = Glider(2, env, booster)
env.process(netShooter(env, glider1))
env.process(netShooter(env, glider2))
env.run(until=20)
print('1: I flew for %.2f miles' % (glider1.fly_distance*10.0))
print('2: I flew for %.2f miles' % (glider2.fly_distance*10.0))