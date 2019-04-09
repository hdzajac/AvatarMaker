import logging
import numpy as np
import json


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
        return {
            "random_parameter": np.random.randint(0, 100),
            "arm_scale": np.random.random() * 1.5 + 0.5
        }

    # write the specification for the next training step in a file that will be red by the academy and used
    def write_specification(self, specification_definition):
        with open("specification.json", "w") as outfile:
            json.dump(specification_definition, outfile)

    def finish(self):
        # todo change this shit
        file = open("tmp", "a+")
        file.write(str(self.lessons))
        file.close()

