"""
logger
"""
import os
import json
import pickle


class Logger:

    def __init__(self, filename:str, load_existing=False):
        self.parent_dir = os.path.dirname(os.path.realpath(__file__))
        self.result_dir = os.path.join(self.parent_dir, 'results')
        self.model_dir = os.path.join(self.parent_dir, 'models')

        if load_existing:
            self.filename = filename
        else:
            self.filename = self.find_unused_filename(filename)

        self.log_path = os.path.join(self.result_dir, self.filename + '.json')
        self.model_path = os.path.join(self.model_dir, self.filename + '.p')

        self.data = { 
                'episodes':0,
                'rewards':[],
                'steps':[],
                'success':[]
                }

        if load_existing:
            self.load()
            print('loaded results from ', self.log_path)
        else:
            assert not os.path.isfile(self.log_path), \
                f"the file {self.log_path} already exists"
            print('result will be stored in ', self.log_path)
            self.save()

    def find_unused_filename(self, filename):
        while os.path.isfile(os.path.join(self.result_dir, filename + '.json')):
            parts = filename.split('-')

            if len(parts) == 1:
                filename = filename + '-0'
            elif len(parts) > 1:
                suffix = parts[-1]
                assert suffix.isnumeric(), "invalid filename, has to be *-{int}"
                number = int(suffix)
                filename = '-'.join(parts[:-1]) + '-' + str(number + 1)
            else:
                raise Exception()

        return filename

    def append(self, reward:float, steps:int, success:bool):
        self.data['rewards'].append(reward)
        self.data['steps'].append(steps)
        self.data['success'].append(success)
        self.data['episodes'] += 1

    def save(self):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, 'w') as f:
            json.dump(self.data, f)

    def load(self):
        with open(self.log_path, 'r') as f:
            self.data = json.load(f) 

    def save_model(self, model):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        pickle.dump(model, open(self.model_path, 'wb'))

    def load_model(self):
        return pickle.load(open(self.model_path, 'rb'))
