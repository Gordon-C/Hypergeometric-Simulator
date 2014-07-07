from random import shuffle, sample as sample_without_replacement
import time
from threading import *

#-----------------Class Definitions-----------------
class Experiment:
	def __init__(self, sample, population, successes):
		self.sample = sample
		self.population = population
		self.successes = successes
		self.results = []
		assert sample <= population, 'Sample must be less than or equal to population'
		assert successes <= population, 'Successes must be less than or equal to population'


	def perform(self, num_trials):
		self.results = [hypergeometric_pull(self.sample, self.population, self.successes) for trial in range(num_trials)] #.extend for caching mechanism

	def __eq__(self, other):
		return self.sample == other.sample and self.population == other.population and self.successes == other.successes

	def __str__(self):
		return str(self.results)

class Hypergeometric_Pull_Thread(Thread):
	def __init__(self, notify_window):
		Thread.__init__(self)
		self._notify_window = notify_window
		self._want_abort = 0
		self.start()

	def run(self):
		pass

#---------------------Helpers--------------------------
def hypergeometric_pull(sample, population, successes):
	'''returns list of [successes, fails] pulled from a @population with number of @successes and @sample size without replacement'''
	bucket = [True] * successes + [False] * (population - successes)
	shuffle(bucket)
	pulled = sample_without_replacement(bucket, sample)
	num_successes = sum(pulled)
	num_fails = sample - num_successes
	return (num_successes, num_fails)
