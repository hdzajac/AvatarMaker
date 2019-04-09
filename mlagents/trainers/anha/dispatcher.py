import logging
from multiprocessing import Pipe, Queue, Process

import win32con
import yaml
import numpy as np

from mlagents.envs import UnityEnvironmentException
from mlagents.trainers.anha.brain.thinker import Thinker
from mlagents.trainers.learn import run_training


class Dispatcher:
    def __init__(self, run_options):
        self.options = run_options
        self.logger = logging.getLogger("anha")
        self.training_instances = {}

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

        self.thinker = Thinker(self.trainer_config)
        return

    # use random seed 0 - 10 000
    def start(self):
        concurrent_runs = self.trainer_config['concurrent_runs']
        max_runs = self.trainer_config['max_runs']

        # todo save the state every now and them -> in thinker
        for j in range(max_runs):
            for i in range(concurrent_runs):
                specification = self.thinker.get_specification()
                self.thinker.write_specification(specification)
                receiver, sender = Pipe()
                # todo: do something with the specification
                run_seed = np.random.randint(0, 10000)
                p = Process(target=run_training, args=(i, run_seed, self.options, sender))
                self.training_instances[i] = {"specification": specification, "receiver": receiver, "process": p}
                p.start()
                # Wait for signal that environment has successfully launched
                while receiver.recv() is not True:
                    continue
                self.logger.info("Dispatched process {}, run: {}".format(i, j))
                self.logger.debug("Dispatched process {}, run: {}\nParameters: \n{}".format(i, j, str(specification)))

            for i in range(concurrent_runs):
                training = self.training_instances[i]
                results = training["receiver"].recv()
                specification = training["specification"]

                self.logger.info("Received results from {}, run: {}".format(i, j))
                self.logger.debug("Received results from {}, run: {}\nParameters: \n{}".format(i, j, str(results)))

                self.thinker.add_result(specification, results)
                training["process"].join()
        self.thinker.finish()


    def _win_handler(self, event):
        """
        This function gets triggered after ctrl-c or ctrl-break is pressed
        under Windows platform.
        """
        if event in (win32con.CTRL_C_EVENT, win32con.CTRL_BREAK_EVENT):
            self.thinker.finish()
            return True
        return False




