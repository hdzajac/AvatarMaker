import logging


# todo: Think of multiple runs at once
import yaml

from mlagents.envs import UnityEnvironmentException


class Controller:
    def __init__(self, run_options):
        self.options = run_options
        self.logger = logging.getLogger("anha")

        if run_options["<main-config-path>"] == 'None':
            self.logger.error("Not received path to global config file")
            raise Exception()

        config_path = run_options["<main-config-path>"]

        try:
            with open(config_path) as data_file:
                self.trainer_config = yaml.load(data_file)
        except IOError:
            raise UnityEnvironmentException('Parameter file could not be found '
                                            'at {}.'
                                            .format(config_path))
        except UnicodeDecodeError:
            raise UnityEnvironmentException('There was an error decoding '
                                            'Global Config from this path : {}'
                                            .format(config_path))

        return

    # use random seed 0 - 10 000
    def start(self):
        options = self.options
        jobs = []
        run_seed =



            for i in range(num_runs):
                if seed == -1:
                    run_seed = np.random.randint(0, 10000)
                process_queue = Queue()
                p = Process(target=run_training, args=(i, run_seed, options, process_queue))
                jobs.append(p)
                p.start()
                # Wait for signal that environment has successfully launched
                while process_queue.get() is not True:
                    continue


        # self.single_runner.run_training(0, 2 , self.run_options, self.precess_queue)

