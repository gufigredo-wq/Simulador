
TOTAL_TICKS = 1000
NUM_NODES = 3

NODE_MAX_CPU = 100   
NODE_MAX_MEM = 1000  

CHANCE_NEW_TASK = 0.8  

TASK_TYPES = [
    {"name": "heavy_cpu", "cpu": 60, "mem": 100, "min_dur": 6, "max_dur": 10},
    {"name": "heavy_mem", "cpu": 10, "mem": 500, "min_dur": 4, "max_dur": 8},
    {"name": "light",     "cpu": 5,  "mem": 50,  "min_dur": 2, "max_dur": 5},

]