# # Unity ML-Agents Toolkit

from typing import Optional

import yaml
import logging

from mlagents.envs import UnityEnvironment
from mlagents.envs.exception import UnityEnvironmentException
from mlagents.trainers import MetaCurriculumError, MetaCurriculum
from mlagents.trainers.trainer_controller import TrainerController


class TrainingExecutor:
    def __init__(self):
        self.logger = logging.getLogger("anha")

    def run_training(self, sub_id: int, run_seed: int, run_options, process_queue):
        """
        Launches training session.
        :param process_queue: Queue used to send signal back to main.
        :param sub_id: Unique id for training session.
        :param run_seed: Random seed used for training.
        :param run_options: Command line arguments for training.
        """

        # General parameters
        env_path = (run_options['--env']
                    if run_options['--env'] != 'None' else None)
        run_id = run_options['--run-id']
        load_model = run_options['--load']
        train_model = run_options['--train']
        save_freq = int(run_options['--save-freq'])
        keep_checkpoints = int(run_options['--keep-checkpoints'])
        worker_id = int(run_options['--worker-id'])
        curriculum_folder = (run_options['--curriculum']
                             if run_options['--curriculum'] != 'None' else None)
        lesson = int(run_options['--lesson'])
        no_graphics = run_options['--no-graphics']
        trainer_config_path = run_options['<trainer-config-path>']

        model_path = './models/{run_id}'.format(run_id=run_id)
        summaries_dir = './summaries'

        trainer_config = self.load_config(trainer_config_path)
        env = self.init_environment(env_path, no_graphics, worker_id + sub_id, run_seed)

        self.logger.info("Initialised Environment [" + run_id + "]")

        maybe_meta_curriculum = self.try_create_meta_curriculum(curriculum_folder, env)

        external_brains = {}
        for brain_name in env.external_brain_names:
            external_brains[brain_name] = env.brains[brain_name]

        # Create controller and begin training.
        tc = TrainerController(model_path, summaries_dir, run_id + '-' + str(sub_id),
                               save_freq, maybe_meta_curriculum,
                               load_model, train_model,
                               keep_checkpoints, lesson, external_brains, run_seed)

        # Signal that environment has been launched.
        process_queue.put(True)

        # Begin training
        tc.start_learning(env, trainer_config)

    @staticmethod
    def try_create_meta_curriculum(curriculum_folder: Optional[str], env: UnityEnvironment) -> Optional[MetaCurriculum]:
        if curriculum_folder is None:
            return None
        else:
            meta_curriculum = MetaCurriculum(curriculum_folder, env._resetParameters)
            if meta_curriculum:
                for brain_name in meta_curriculum.brains_to_curriculums.keys():
                    if brain_name not in env.external_brain_names:
                        raise MetaCurriculumError('One of the curricula '
                                                  'defined in ' +
                                                  curriculum_folder + ' '
                                                                      'does not have a corresponding '
                                                                      'Brain. Check that the '
                                                                      'curriculum file has the same '
                                                                      'name as the Brain '
                                                                      'whose curriculum it defines.')
            return meta_curriculum

    @staticmethod
    def load_config(trainer_config_path):
        try:
            with open(trainer_config_path) as data_file:
                trainer_config = yaml.load(data_file)
                return trainer_config
        except IOError:
            raise UnityEnvironmentException('Parameter file could not be found '
                                            'at {}.'
                                            .format(trainer_config_path))
        except UnicodeDecodeError:
            raise UnityEnvironmentException('There was an error decoding '
                                            'Trainer Config from this path : {}'
                                            .format(trainer_config_path))

    @staticmethod
    def init_environment(env_path, no_graphics, worker_id, seed):
        if env_path is not None:
            # Strip out executable extensions if passed
            env_path = (env_path.strip()
                        .replace('.app', '')
                        .replace('.exe', '')
                        .replace('.x86_64', '')
                        .replace('.x86', ''))
        return UnityEnvironment(
            file_name=env_path,
            worker_id=worker_id,
            seed=seed,
            no_graphics=no_graphics
        )
