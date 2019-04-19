import logging
import json


class ConfigParameters:
    Low_Twist_Limits = -20
    High_Twist_Limits = 70
    Swing_Limit1 = 40
    Swing_Limit2 = 40
    ScaleY = [1, 1.25, 1.5, 1.75, 2]

class Thinker:
    def __init__(self, specification_definition):
        self.lessons = []
        # todo do something about this specification
        self.specification_definition = specification_definition
        self.envs = specification_definition['concurrent_runs']
        self.logger = logging.getLogger("anha")
        return

    def add_result(self, specification, result,i):

        record = {"specification": specification, "result": result}
        with open("results.json", "a") as outfile:
            json.dump(i, outfile)
            json.dump(' ', outfile)
            json.dump(result, outfile)
            outfile.write('\n')
        self.logger.debug("Adding results: {}".format(record))
        self.lessons.append(record)
        return

    # todo Come up with new specification based on the definition and previous iterations
    def get_specification(self, i):
        return {"LeftArm": self.get_ArmSpecification("LeftArm", i),
                "RightArm": self.get_ArmSpecification("RightArm", i)}


    # write the specification for the next training step in a file that will be red by the academy and used
    def write_specification(self, specification_definition):
        with open("specification.json", "w") as outfile:
            json.dump(specification_definition, outfile)

    def finish(self):
        # todo change this shit
        file = open("tmp", "a+")
        file.write(str(self.lessons))
        file.close()

    def get_ArmSpecification(self, name, i):
        return {
            "Name": name,
            "ScaleX": 1,
            "ScaleY":  ConfigParameters.ScaleY[i],  # np.random.random() * 2 + 1,  # float between 1 and 2
            "ScaleZ": 1,
            "LowTwistLimit": ConfigParameters.Low_Twist_Limits,
            "HighTwistLimit": ConfigParameters.High_Twist_Limits,
            "SwingLimit1": ConfigParameters.Swing_Limit1,
            "SwingLimit2": ConfigParameters.Swing_Limit2,
        }

