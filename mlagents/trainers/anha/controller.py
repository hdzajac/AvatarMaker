import logging


# todo: Think of multiple runs at once
class Controller:
    def __init__(self, run_options):
        self.options = run_options
        self.logger = logging.getLogger("anha")
        return

    # todo accept only with environment - no unity learning :c
    # if options['--env'] == 'None' and num_runs > 1:
    #     raise TrainerError('It is not possible to launch more than one concurrent training session '
    #                        'when training from the editor.')


    def start(self):
        options = self.options
        num_runs = int(options['--num-runs'])
        seed = int(options['--seed'])
        jobs = []
        run_seed = seed

        if num_runs == 1:
            if seed == -1:
                run_seed = np.random.randint(0, 10000)
            run_training(0, run_seed, options, Queue())
        else:
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

