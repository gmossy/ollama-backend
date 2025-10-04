#!/usr/bin/env python3
"""
LangGraph + Ollama Example Scenarios
Practical examples for different use cases
"""

from langgraph_agent import OllamaAgent, SimpleReActAgent, MultiAgentSystem, Colors


# ============================================================================
# EXAMPLE 1: Technical Troubleshooting
# ============================================================================

def example_docker_troubleshooting():
    """Example: Troubleshoot Docker issues using agent with tools"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 1: Docker Troubleshooting Agent{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = OllamaAgent(max_iterations=5)

    task = """
    I'm having issues with my Docker setup. Can you help?

    1. First, check if Docker is running
    2. Search for documentation about common Docker issues
    3. Tell me what time this troubleshooting session started
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent used multiple tools to help troubleshoot Docker issues.")
    print("It checked Docker status, searched docs, and provided timestamp.")


# ============================================================================
# EXAMPLE 2: Data Analysis Assistant
# ============================================================================

def example_data_analysis():
    """Example: Analyze data using calculation tools"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 2: Data Analysis Assistant{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = OllamaAgent(max_iterations=4)

    task = """
    I have quarterly sales data:
    - Q1: $125,000
    - Q2: $98,000
    - Q3: $187,000
    - Q4: $156,000

    Calculate:
    1. Total annual sales: 125000 + 98000 + 187000 + 156000
    2. Average quarterly sales (divide total by 4)
    3. Growth from Q1 to Q4 as percentage

    Show all calculations.
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent performed multiple calculations and analyzed the data.")


# ============================================================================
# EXAMPLE 3: Code Development with Multiple Specialists
# ============================================================================

def example_code_development():
    """Example: Develop code with coder and debugger collaboration"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 3: Collaborative Code Development{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    system = MultiAgentSystem()

    task = """
    Create a Python function that:
    1. Takes a list of numbers
    2. Removes duplicates
    3. Returns sorted list in descending order

    Requirements:
    - Include type hints
    - Add docstring
    - Handle edge cases (empty list, None)
    - Make it efficient
    """

    results = system.collaborate(
        task,
        specialists=["coder", "debugger"]
    )

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("Two specialists collaborated:")
    print("- Coder: Created the initial implementation")
    print("- Debugger: Reviewed for bugs and improvements")


# ============================================================================
# EXAMPLE 4: ReAct Reasoning for Logic Puzzles
# ============================================================================

def example_logic_puzzle():
    """Example: Solve logic puzzle using ReAct reasoning"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 4: Logic Puzzle with ReAct{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = SimpleReActAgent()

    task = """
    Three friends - Alice, Bob, and Carol - each have a different pet.

    Clues:
    1. Alice doesn't have a dog
    2. Bob doesn't have a cat
    3. Carol has a bird

    Who has which pet? (dog, cat, bird)
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent used ReAct (Reasoning + Acting) to solve step-by-step.")


# ============================================================================
# EXAMPLE 5: System Design with Architect
# ============================================================================

def example_system_design():
    """Example: Design system architecture"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 5: System Architecture Design{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    system = MultiAgentSystem()

    task = """
    Design a simple URL shortener service.

    Include:
    1. Main components (API, database, cache)
    2. Data flow
    3. Database schema
    4. Key considerations (scaling, security)
    """

    result = system.run_specialist(task, "architect")

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The architect specialist provided a comprehensive system design.")


# ============================================================================
# EXAMPLE 6: Research Assistant
# ============================================================================

def example_research_assistant():
    """Example: Research assistant that searches documentation"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 6: Research Assistant{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = OllamaAgent(max_iterations=4)

    task = """
    I'm learning about containerization. Can you help me understand:

    1. Search for documentation about Docker
    2. Search for documentation about Ollama
    3. Compare them and tell me how they relate to each other
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent searched multiple documentation sources and synthesized findings.")


# ============================================================================
# EXAMPLE 7: Math Tutor
# ============================================================================

def example_math_tutor():
    """Example: Math tutor that shows work"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 7: Math Tutor{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = OllamaAgent(max_iterations=3)

    task = """
    Help me solve this problem and show all steps:

    If a car travels at 65 mph for 3.5 hours, how far does it travel?

    Calculate: 65 * 3.5
    Then explain what this means in the context of the problem.
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent used the calculator tool and explained the solution.")


# ============================================================================
# EXAMPLE 8: Code Refactoring Team
# ============================================================================

def example_code_refactoring():
    """Example: Team of specialists refactor code"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 8: Code Refactoring Team{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    system = MultiAgentSystem()

    code = """
def get_user_data(id):
    result = db.query("SELECT * FROM users WHERE id=" + str(id))
    return result
    """

    task = f"""
    This code has security and style issues:

    {code}

    Identify problems and provide improved version.
    """

    results = system.collaborate(
        task,
        specialists=["coder", "debugger"]
    )

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("Multiple specialists identified:")
    print("- SQL injection vulnerability")
    print("- Missing error handling")
    print("- No type hints")
    print("- And provided secure, improved version")


# ============================================================================
# EXAMPLE 9: Sequential Task Execution
# ============================================================================

def example_sequential_tasks():
    """Example: Execute multiple tasks in sequence"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 9: Sequential Task Execution{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = OllamaAgent(max_iterations=6)

    task = """
    I need to complete several tasks in order:

    1. Get the current time
    2. Calculate how many hours until 5 PM (assume current time is in result from step 1)
    3. Search documentation for Docker
    4. Check if Docker is running
    5. Store in memory: "last_check" = current time

    Execute all steps and provide a summary.
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent executed multiple tools in sequence to complete all tasks.")


# ============================================================================
# EXAMPLE 10: Error Recovery
# ============================================================================

def example_error_recovery():
    """Example: Agent handles errors gracefully"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Example 10: Error Recovery{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

    agent = OllamaAgent(max_iterations=3)

    task = """
    Try to calculate this: 10 / 0

    When you encounter an error, explain what went wrong and provide an alternative approach.
    """

    result = agent.run(task)

    print(f"\n{Colors.GREEN}Summary:{Colors.END}")
    print("The agent detected the division by zero error and explained it properly.")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main menu for examples"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADE
