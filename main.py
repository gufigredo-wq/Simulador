import simpy
import random
import config
from entidades import Cluster, Task

def traffic_generator(env, cluster):
    task_count = 0
    while True:
       
        yield env.timeout(1) 
        
        if random.random() < config.CHANCE_NEW_TASK:
            task_count += 1
            
            chosen = random.choice(config.TASK_TYPES)
         
            params = chosen.copy()
            params['duration'] = random.randint(chosen['min_dur'], chosen['max_dur'])
            
            task = Task(task_count, params)
              
            target_node = random.choice(cluster.get_nodes())  

            latencia = random.uniform(0.01,0.1)

            yield env.timeout(latencia)
           
            env.process(target_node.run_task(task))

def run_simulation():
    print("--- Simulação SimPy Iniciada ---")
    
    env = simpy.Environment()
    
    cluster = Cluster(env, config.NUM_NODES)
   
    env.process(traffic_generator(env, cluster))
    
    env.run(until=config.TOTAL_TICKS)
    print("--- Fim ---")

if __name__ == "__main__":
    run_simulation()

def monitor(env, cluster, history_list):
    """Espião que anota o estado dos nós a cada 1 segundo."""
    while True:
        for node in cluster.get_nodes():
            history_list.append({
                "tick": env.now,
                "node_id": f"Node {node.node_id}",
                # No SimPy, .level é quanto está SENDO USADO
                "cpu_usage": node.cpu.level,
                "mem_usage": node.mem.level,
                # .queue é a lista interna de quem está esperando no yield
                "queue_size": len(node.cpu.queue)
            })
        yield env.timeout(1) # Espera 1 segundo para medir de novo