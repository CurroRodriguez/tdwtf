# The Requirements
# ================
#
# The first requirement is pretty normal. You're supposed to write a module that generates random numbers like a
# double-zero roulette wheel. They don't specify how the random numbers are generated, but that's basically a single
# line of code. Super easy.
#
# It's the second requirement that makes you groan with frustration. They don't want the numbers to be really random.
# "In a true random sequence," the write, "the same number may appear many times in a row, just do[sic] to random
# chance. While that is actually random, it doesn't feel random to our players." They want you to track a history of
# the random numbers generated, and make something that "feels" random: numbers that have appeared recently are less
# like to appear. "Runs", where the same number appears 3 times in a row, should never happen.
#
# "Alright," you say to yourself, "I can do that." But you can do one better. In addition to implementing their
# requirements, you decide to add in your own. You're going to write in a "cheat" function- something that lets you
# either enter in some sort of cheat code, or in some other fashion makes the output of the roulette wheel predictable.
# Be careful, though, you don't want to get caught! You'll need to get creative to make sure nobody stumbles on your
# secret- millions of people are going to gamble with this program.
"""

"""
import collections
import random
import sys

RANGE_STOP = 37
INCREMENT = 13





class ApparentlyRandomPolicy(object):

    def __init__(self, generator=None):
        self.generator = generator or random
        self.recent_numbers = collections.deque([], 10)


    def next_number(self):
        while True:
            number = self.generator.randint(0, RANGE_STOP)
            if self._appears_random(number):
                self._push(number)
                return number


    def _appears_random(self, number):
        return self.recent_numbers.count(number) < 2


    def _push(self, number):
        self.recent_numbers.append(number)



class PelayosPolicy(object):
    """
    Famous roulette cheater Gonzalo Garcia-Pelayo: http://www.onlinerouletter.com/gonzalo-garcia-pelayo.html
    """

    def __init__(self):
        self.values = list(range(RANGE_STOP + 1))
        self.first_num = random.randint(0, RANGE_STOP)
        self.second_num = random.randint(0, RANGE_STOP)
        self.recent_numbers = collections.deque([], 20)


    def next_number(self):
        number = ((self.first_num * self.second_num) + INCREMENT) % RANGE_STOP
        if number in self.recent_numbers:
            number += 1
        self.first_num, self.second_num = self.second_num, number
        self.recent_numbers.append(number)
        return number




class Roulette(object):

    def __init__(self):
        self.generator_policy = ApparentlyRandomPolicy()


    def spin(self):
        return self.generator_policy.next_number()




class RouletteGame(object):

    def __init__(self):
        self.roulette = Roulette()


    def run(self):
        while True:
            command = raw_input('Press <Enter> to spin or type "exit" to end: ')
            lc_command = command.lower()
            if lc_command == 'exit':
                return
            elif lc_command == 'pelayo':
                self.roulette.generator_policy = PelayosPolicy()
            elif lc_command == 'reset':
                self.roulette.generator_policy = ApparentlyRandomPolicy()
            else:
                number = self.roulette.spin()
                if number == 37:
                    number = '00'
                print "- Number: ", number




if __name__=='__main__':
    game = RouletteGame()
    game.run()
    sys.exit(0)
