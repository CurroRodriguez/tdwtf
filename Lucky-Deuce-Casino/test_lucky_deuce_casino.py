import unittest
import lucky_deuce_casino as ldc

import random


class TestApparentlyRandomPolicy(unittest.TestCase):

    def setUp(self):
        self.generator = RandomModuleMock()
        self.policy = ldc.ApparentlyRandomPolicy(self.generator)
        return super(TestApparentlyRandomPolicy, self).setUp()

    def test_initializes_generator_to_random_module_if_none_specified(self):
        policy = ldc.ApparentlyRandomPolicy()
        self.assertIs(policy.generator, random)


    def test_initializes_generator_to_specified_object(self):
        self.assertIs(self.policy.generator, self.generator)


    def test_returns_new_number_from_generator(self):
        self.generator.sequence = [1]
        generated = self.policy.next_number()
        self.assertEqual(generated, 1)


    def test_number_range_requested_is_between_zero_and_range_stop(self):
        self.generator.sequence = [1]
        self.policy.next_number()
        self.assertEqual(self.generator.start, 0)
        self.assertEqual(self.generator.stop, ldc.RANGE_STOP)


    def test_skips_number_if_appears_more_three_or_more_times(self):
        self.generator.sequence = [1, 1, 1, 2]
        self.assertEqual(self.policy.next_number(), 1)
        self.assertEqual(self.policy.next_number(), 1)
        self.assertEqual(self.policy.next_number(), 2)


class TestPelayosPolicy(unittest.TestCase):

    def test_the_first_number_is_random(self):
        self.policy = ldc.PelayosPolicy()
        number = self.policy.next_number()
        self.assertTrue(number >= 0)
        self.assertTrue(number <= ldc.RANGE_STOP)

    def test_numbers_follow_policy_generation(self):
        self.policy = ldc.PelayosPolicy()
        first_num = self.policy.next_number()
        second_num = self.policy.next_number()
        predictable = self.policy.next_number()
        expected = ((first_num * second_num) + ldc.INCREMENT) % ldc.RANGE_STOP
        self.assertEqual(predictable, expected)





class RandomModuleMock(object):

    def __init__(self):
        self.current_index = 0
        self._sequence = []


    @property
    def sequence(self):
        return self._sequence


    @sequence.setter
    def sequence(self, value):
        self._sequence = value
        self.current_index = 0


    def randrange(self, stop):
        self.range_stop = stop


    def randint(self, start, stop):
        self.start = start
        self.stop = stop
        next = self._sequence[self.current_index]
        self.current_index += 1
        return next



class TestRoulette(unittest.TestCase):

    def test_can_spin(self):
        roulette = ldc.Roulette()
        number = roulette.spin()
        self.assertIsInstance(number, int)


    def test_policy_can_be_changed(self):
        roulette = ldc.Roulette()
        policy_mock = GeneratorPolicyMock()
        roulette.generator_policy = policy_mock
        roulette.spin()
        self.assertTrue(policy_mock.invoked)




class GeneratorPolicyMock(object):

    def next_number(self):
        self.invoked = True



