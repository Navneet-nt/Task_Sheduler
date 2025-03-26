import heapq
from typing import List, Dict, Tuple, Set

class Task:
    def __init__(self, name: str, duration: int, dependencies: List[str] = None):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies or []
        self.start_time = 0
        self.end_time = 0

class AStarTaskScheduler:
    def __init__(self, tasks: List[Task]):
        self.tasks = {task.name: task for task in tasks}
        self.dependency_graph = self._build_dependency_graph()
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build a comprehensive dependency graph."""
        graph = {task_name: [] for task_name in self.tasks}
        for task_name, task in self.tasks.items():
            for dep in task.dependencies:
                graph[dep].append(task_name)
        return graph
    
    def _calculate_total_remaining_time(self, scheduled_tasks: Set[str]) -> int:
        """
        Advanced heuristic calculation:
        1. Estimate total remaining task time
        2. Consider critical path
        3. Penalize unscheduled dependent tasks
        """
        unscheduled_tasks = set(self.tasks.keys()) - scheduled_tasks
        
        # Calculate remaining time
        remaining_time = sum(
            self.tasks[task].duration 
            for task in unscheduled_tasks
        )
        
        # Critical path estimation
        max_dependent_depth = 0
        for task in unscheduled_tasks:
            # Check depth of task dependencies
            current_depth = self._calculate_dependency_depth(task, scheduled_tasks)
            max_dependent_depth = max(max_dependent_depth, current_depth)
        
        return remaining_time + max_dependent_depth
    
    def _calculate_dependency_depth(self, task: str, scheduled_tasks: Set[str], depth: int = 0) -> int:
        """
        Recursively calculate the depth of unscheduled dependencies
        to estimate the critical path.
        """
        task_obj = self.tasks[task]
        
        # If all dependencies are scheduled, return current depth
        if all(dep in scheduled_tasks for dep in task_obj.dependencies):
            return depth
        
        # Find unscheduled dependencies and calculate their depth
        max_dep_depth = depth
        for dep in task_obj.dependencies:
            if dep not in scheduled_tasks:
                dep_depth = self._calculate_dependency_depth(dep, scheduled_tasks, depth + 1)
                max_dep_depth = max(max_dep_depth, dep_depth)
        
        return max_dep_depth
    
    def a_star_schedule(self) -> List[Tuple[str, int, int]]:
        """
        A* scheduling algorithm with advanced heuristic:
        1. Uses priority queue for task selection
        2. Considers dependencies
        3. Minimizes total scheduling time
        """
        scheduled_tasks = set()
        schedule = []
        current_time = 0
        
        # Priority queue to store tasks with their priority
        task_queue = []
        
        while len(scheduled_tasks) < len(self.tasks):
            # Find tasks ready to be scheduled
            available_tasks = [
                task_name 
                for task_name, task in self.tasks.items() 
                if task_name not in scheduled_tasks and 
                all(dep in scheduled_tasks for dep in task.dependencies)
            ]
            
            if not available_tasks:
                raise ValueError("Circular dependency or scheduling impossible")
            
            # Clear previous queue
            task_queue.clear()
            
            # Evaluate and prioritize available tasks
            for task_name in available_tasks:
                # Calculate A* score
                task = self.tasks[task_name]
                
                # F(n) = G(n) + H(n)
                # G(n): Current time to start task
                # H(n): Estimated remaining time with heuristic
                g_score = current_time
                h_score = self._calculate_total_remaining_time(scheduled_tasks | {task_name})
                f_score = g_score + h_score + task.duration
                
                # Lower score means higher priority
                heapq.heappush(task_queue, (f_score, task_name))
            
            # Select the task with lowest A* score
            _, best_task = heapq.heappop(task_queue)
            task = self.tasks[best_task]
            
            # Schedule the task
            task.start_time = current_time
            task.end_time = current_time + task.duration
            
            schedule.append((task.name, task.start_time, task.end_time))
            scheduled_tasks.add(best_task)
            
            # Update current time
            current_time = task.end_time
        
        return schedule

# Example task creation function
def create_example_tasks():
    return [
        Task("Design", 3, []),  # Starting task with no dependencies
        Task("Frontend", 4, ["Design"]),
        Task("Backend", 5, ["Design"]),
        Task("Database", 3, ["Backend"]),
        Task("Testing", 2, ["Frontend", "Backend", "Database"])
    ]