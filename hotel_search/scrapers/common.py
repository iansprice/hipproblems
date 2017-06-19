from tornado import gen
from itertools import chain
import simplejson as json
import os
from random import randint
from functools import reduce


class Scraper(object):

    provider = None

    @gen.coroutine
    def run(self):
        self.results = []

        # wait a bit
        yield gen.sleep(2)

        self.load_fake_results(xrange(1, 20, self.step))
        self.results.sort(key=lambda r: r['ecstasy'], reverse=True)

        raise gen.Return(self.results)

    def load_fake_results(self, range_iter):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/data.json') as data_file:
            dataset = json.load(data_file)
            data_keys = dataset.keys()

        for i in range_iter:
            data = dataset[data_keys[i]]
            data['provider'] = self.provider
            data['price'] = randint(50, 300)
            data['ecstasy'] = randint(1, 1000)
            self.results.append(data)


class GeneratorPipeline(object):
    '''
    Chain generators together into a single generator
    :param steps: 
    :return: 
    '''

    def __init__(self, generators):
        self.generators = generators

    @gen.coroutine
    def run(self):
        generator_list = [Generator() for Generator in self.generators]
        results = yield [gen.Task(generator.run)
                         for generator in generator_list]
        raise gen.Return(results)
