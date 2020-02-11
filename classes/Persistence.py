import os
import pickle
from .Migration import Source, Migration

class Persistence():

    def __init__(self, obj_list, file_path):
        if isinstance(obj_list, list) and isinstance(file_path, str):
            self.obj_list = obj_list
            self.file_path = file_path
        else:
            raise ValueError

    def create(self, obj_list):

        workload_list = {'source': [], 'migration': []}
        obj = []
        
        if isinstance(obj_list, list):
            
            obj = self.obj_list

            for o in obj:
                if isinstance(o, Source):
                    workload_list['source'].append(o.get_ip)
                elif isinstance(o, Migration):
                    workload_list['migration'].append(o.source.ip)

            for value in workload_list.values():

                if len(set(value)) != len(value):
                    raise ValueError

            with open(self.file_path, 'wb') as dumpFile:
                pickle.dump(obj, dumpFile)

    def read(self):
        with open(self.file_path, 'rb') as readFile:
            self.obj_list = pickle.load(readFile)
        return self.obj_list

    def update(self):
        saved_objects = self.read()
        new_objects = self.obj_list[:]

        for obj in saved_objects:
            if obj not in new_objects:
                new_objects.append(obj)

        self.create(new_objects)

    def delete(self):
        os.remove(self.file_path)
