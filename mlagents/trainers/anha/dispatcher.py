import logging
import yaml
import numpy as np

from mlagents.envs import UnityEnvironmentException
from mlagents.trainers.anha.brain.thinker import Thinker
from mlagents.trainers.anha.training_wrapper import TrainingWrapper


class Dispatcher:
    def __init__(self, run_options):
        self.options = run_options
        self.logger = logging.getLogger("anha")
        self.training_instances = {}
        self.thinker = Thinker()

        if run_options["<main-config-path>"] == 'None':
            self.logger.error("Not received path to global config file")
            raise Exception()

        config_path = run_options["<main-config-path>"]

        try:
            with open(config_path) as data_file:
                self.trainer_config = yaml.load(data_file)
        except IOError:
            message = 'Parameter file could not be found at {}.'.format(config_path)
            self.logger.error(message)
            raise UnityEnvironmentException(message)
        except UnicodeDecodeError:
            message = 'There was an error decoding Global Config from this path : {}'.format(config_path)
            self.logger.error(message)
            raise UnityEnvironmentException(message)

        return

    # use random seed 0 - 10 000
    def start(self):
        concurrent_runs = self.trainer_config['concurrent_runs']
        max_runs = self.trainer_config['max_runs']

        for j in range(max_runs):
            for i in range(concurrent_runs):

                self.training_instances[i] = TrainingWrapper()
                run_seed = np.random.randint(0, 10000)







        options = self.options
        jobs = []
        # run_seed =



            # for i in range(num_runs):
            #     if seed == -1:
            #         run_seed = np.random.randint(0, 10000)
            #     process_queue = Queue()
            #     p = Process(target=run_training, args=(i, run_seed, options, process_queue))
            #     jobs.append(p)
            #     p.start()
            #     # Wait for signal that environment has successfully launched
            #     while process_queue.get() is not True:
            #         continue


        # self.single_runner.run_training(0, 2 , self.run_options, self.precess_queue)

