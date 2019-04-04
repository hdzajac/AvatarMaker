import logging
import numpy as np


class Thinker:
    def __init__(self, specification_definition):
        self.lessons = []
        # todo do something about this specification
        self.specification_definition = specification_definition
        self.envs = specification_definition['concurrent_runs']
        self.logger = logging.getLogger("anha")
        return

    def add_result(self, specification, result):
        record = {"specification": specification, "result": result}
        self.logger.debug("Adding results: {}".format(record))
        self.lessons.append(record)
        return

    # todo Come up with new specification based on the definition and previous iterations
    def get_specification(self):
        return {"random parameter": np.random.randint(0, 100)}

    def finish(self):
        # todo change this shit
        file = open("tmp", "a+")
        file.write(str(self.lessons))
        file.close()
