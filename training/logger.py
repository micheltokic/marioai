"""
logger
"""
import os
import json


class Logger:

    def __init__(self, filename:str):
        path = os.path.dirname(os.path.realpath(__file__)) \
                + '/results/' + filename + '.json'

        while os.path.isfile(path):
            parts = filename.split('-')

            if len(parts) == 1:
                filename = filename + '-0'
            elif len(parts) == 2:

                assert parts[1].isnumeric(), \
                        "invalid filename, has to be *-{int}"

                number = int(parts[1])
                filename = parts[0] + '-' + str(number + 1)
            else:
                raise Exception()

            path = os.path.dirname(os.path.realpath(__file__)) \
                    + '/results/' + filename + '.json'

        self.path = path
        # self.filename = filename
        print('result will be stored in ', self.path)

        assert not os.path.isfile(self.path), \
            f"the file {self.path} already exists"

        self.data = { 
                'episodes':0,
                'rewards':[],
                'steps':[],
                'success':[]
                }

        # generate the empty file
        self.save()

    def append(self, reward:float, steps:int, success:bool):
        self.data['rewards'].append(reward)
        self.data['steps'].append(steps)
        self.data['success'].append(success)
        self.data['episodes'] += 1

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)


