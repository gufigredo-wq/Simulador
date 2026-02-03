
import simpy
import config

class Task:
    def __init__(self, task_id, task_type):
        self.task_id = task_id
        self.name = task_type['name']
       
        self.cpu_req = task_type['cpu'] 
        self.mem_req = task_type['mem']  
        self.duration = task_type['duration']

    def __repr__(self):
        return f"[Task {self.task_id} ({self.name})]"

class Node:
    def __init__(self, env, node_id):
        self.env = env
        self.node_id = node_id
        
       
        self.cpu = simpy.Container(env, capacity=config.NODE_MAX_CPU, init=config.NODE_MAX_CPU)
        self.mem = simpy.Container(env, capacity=config.NODE_MAX_MEM, init=config.NODE_MAX_MEM)
        
        self.jobs_running = 0

    
    
    def run_task(self, task):

        arrival_time = self.env.now
        print(f"[{self.env.now}] {task} CHEGOU na fila do Node {self.node_id}")
        
        
        yield self.cpu.get(task.cpu_req)
        yield self.mem.get(task.mem_req)
        
        
        wait_time = self.env.now - arrival_time
        self.jobs_running += 1
        print(f"   >>> [{self.env.now}] Node {self.node_id} INICIOU {task} (Esperou: {wait_time}s)")
        
       
        yield self.env.timeout(task.duration)
        
        
        yield self.cpu.put(task.cpu_req)
        yield self.mem.put(task.mem_req)
        
        self.jobs_running -= 1
        print(f"       [{self.env.now}] Node {self.node_id} FINALIZOU {task}")

class Cluster:
    def __init__(self, env, num_nodes):
        self.nodes = [Node(env, i) for i in range(num_nodes)]

    def get_nodes(self):
        return self.nodes
    
class LoadBalancer:
    def __init__(self, cluster):
        self.cluster = cluster

    def get_best_node(self):
        nodes = self.cluster.get_nodes()

        best_node = sorted(nodes, key=lambda n: len(n.cpu.queue))[0]
        return best_node