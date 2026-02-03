import random
import config
from entidades import Task

class TrafficGenerator:
    def __init__(self):
        self.request_count = 0

    def generate(self):
        if random.random() < config.CHANCE_NEW_TASK:
            self.request_count += 1
            chosen_type = random.choice(config.TASK_TYPES)
            
            # Cria params com duração aleatória
            params = chosen_type.copy()
            params['duration'] = random.randint(chosen_type['min_dur'], chosen_type['max_dur'])
            
            return Task(self.request_count, params)
        return None

class AllocationPolicy:
    @staticmethod
    def allocate(task, cluster):
        nodes = cluster.get_nodes()
        
        best_node = sorted(nodes, key=lambda n: len(n.queue))[0]

        best_node.add_to_queue(task)
        
        best_node.try_process_queue()

        return True
        