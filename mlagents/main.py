import logging

from docopt import docopt
from mlagents.trainers.anha.controller import Controller
import time


def main():
    _USAGE = '''
    Usage:
      mlagents-learn <trainer-config-path> <main-config-path> [options]
      mlagents-learn --help

    Options:
      --env=<file>               Name of the Unity executable [default: None].
      --curriculum=<directory>   Curriculum json directory for environment [default: None].
      --keep-checkpoints=<n>     How many model checkpoints to keep [default: 5].
      --lesson=<n>               Start learning from this lesson [default: 0].
      --load                     Whether to load the model or randomly initialize [default: False].
      --run-id=<path>            The directory name for model and summary statistics [default: ppo].
      --save-freq=<n>            Frequency at which to save model [default: 50000].
      --train                    Whether to train model, or only run inference [default: False].
      --worker-id=<n>            Number to add to communication port (5005) [default: 0].
      --no-graphics              Whether to run the environment in no-graphics mode [default: False].
      --config=<file>            Configuration of the upper level Learning       
    '''

    logger = logging.getLogger("anha")

    error_handler = logging.FileHandler("../logs/" + time.strftime("%Y%m%d") + "-ERROR.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcname)s - %(message)s'))

    debug_handler = logging.FileHandler("../logs/" + time.strftime("%Y%m%d") + "-DEBUG.log")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcname)s - %(message)s'))

    info_handler = logging.FileHandler("../logs/" + time.strftime("%Y%m%d") + "-INFO.log")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcname)s - %(message)s'))

    logger.addHandler(error_handler)
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)

    options = docopt(_USAGE)
    controller = Controller(options)
    controller.start()


main()
