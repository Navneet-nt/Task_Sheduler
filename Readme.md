# A* Task Scheduler

## Overview
This project implements an A* search algorithm for task scheduling and compares it with a greedy scheduling approach. It supports dynamic task input, dependency-based task scheduling, and provides a Gantt chart visualization to compare the results.

## Features
- **Dynamic Task Input:** Add tasks with their names and durations.
- **Scheduling Algorithms:**  
  - **A\* Search:** Minimizes total scheduling time using a heuristic that estimates the remaining task durations.
  - **Greedy Approach:** Selects the first available task without global optimization.
- **Gantt Chart Visualization:** Visualize the scheduled tasks on a Gantt chart.
- **Dependency-based Task Scheduling:** Tasks are automatically assigned dependencies based on their input order.

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
