#!/usr/bin/env python3
"""
LangGraph Test Agent for Ollama Models
Python 3.12.11 compatible

This script demonstrates various LangGraph agent patterns with Ollama:
- ReAct agent with tools
- Multi-agent collaboration
- Memory and state management
- Error handling and retries
"""

import os
import json
import operator
from typing import Annotated, TypedDict, List, Literal
from datetime import datetime

try:
    from langchain_community.llms import Ollama
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.tools import tool
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolNode
    from langgraph.checkpoint.memory import MemorySaver
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with:")
    print("  pip install langchain langchain-community langgraph")
    exit(1)


# ============================================================================
# COLOR CODES FOR TERMINAL OUTPUT
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression as a string (e.g., "2 + 2", "10 * 5")
    
    Returns:
        The result of the calculation
    """
    try:
        # Safe evaluation - only allows basic math operations
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


@tool
def get_current_time() -> str:
    """
    Get the current date and time.
    
    Returns:
        Current timestamp as a formatted string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def check_docker_status() -> str:
    """
    Check if Docker is running (simulated).
    
    Returns:
        Docker status information
    """
    import subprocess
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            container_count = len(result.stdout.strip().split('\n')) - 1
            return f"Docker is running. {container_count} container(s) active."
        else:
            return "Docker is not running or not accessible."
    except Exception as e:
        return f"Cannot check Docker status: {str(e)}"


@tool
def search_documentation(query: str) -> str:
    """
    Search documentation for a given query (simulated).
    
    Args:
        query: The search query
    
    Returns:
        Relevant documentation snippets
    """
    docs = {
        "docker": "Docker is a platform for developing, shipping, and running applications in containers. Key commands: docker run, docker build, docker ps.",
        "ollama": "Ollama is a tool for running large language models locally. Use 'ollama pull' to download models and 'ollama run' to interact with them.",
        "langgraph": "LangGraph is a library for building stateful, multi-actor applications with LLMs. It uses graphs to define agent workflows.",
        "zscaler": "Zscaler is a cloud security platform. For Docker, add the Zscaler root certificate to the container's trust store."
    }

    query_lower = query.lower()
    for key, value in docs.items():
        if key in query_lower:
            return f"Documentation for '{key}': {value}"

    return "No documentation found for that query. Try: docker, ollama, langgraph, or zscaler."


@tool
def write_to_memory(key: str, value: str) -> str:
    """
    Write a key-value pair to memory for later retrieval.
    
    Args:
        key: The key to store
        value: The value to store
    
    Returns:
        Confirmation message
    """
    # In a real implementation, this would persist to a database
    # For now, we'll just confirm
    return f"Stored '{key}' = '{value}' in memory."


# List of all available tools
tools = [
    calculate,
    get_current_time,
    check_docker_status,
    search_documentation,
    write_to_memory
]


# ============================================================================
# AGENT STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """The state of the agent"""
    messages: Annotated[List[HumanMessage |
                             AIMessage | SystemMessage], operator.add]
    task: str
    result: str
    iterations: int
    max_iterations: int


# ============================================================================
# AGENT NODES
# ============================================================================

class OllamaAgent:
    """Main agent class using LangGraph and Ollama"""

    def __init__(
        self,
        model_name: str = "llama3.2",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_iterations: int = 5
    ):
        self.model_name = model_name
        self.max_iterations = max_iterations

        # Initialize Ollama LLM
        self.llm = Ollama(
            model=model_name,
            base_url=base_url,
            temperature=temperature
        )

        # Bind tools to the LLM
        self.llm_with_tools = self.llm.bind_tools(tools)

        # Create the agent graph
        self.graph = self._create_graph()

        # Memory for conversation
        self.memory = MemorySaver()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""

        # Define the graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", ToolNode(tools))

        # Set entry point
        workflow.set_entry_point("agent")

        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )

        # Tools always return to agent
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def _agent_node(self, state: AgentState) -> AgentState:
        """The main agent reasoning node"""
        messages = state["messages"]
        iterations = state.get("iterations", 0)

        # Check iteration limit
        if iterations >= self.max_iterations:
            return {
                **state,
                "result": "Maximum iterations reached.",
                "iterations": iterations
            }

        # Create system message with tool descriptions
        system_message = SystemMessage(content="""You are a helpful AI assistant with access to tools. 
When you need to use a tool, format your response to indicate which tool to use.
Always think step-by-step and use tools when appropriate.
After using tools, provide a clear final answer to the user.""")

        # Get response from LLM
        try:
            response = self.llm_with_tools.invoke([system_message] + messages)

            # Convert response to AIMessage if it's not already
            if isinstance(response, str):
                ai_message = AIMessage(content=response)
            else:
                ai_message = response

            return {
                **state,
                "messages": [ai_message],
                "iterations": iterations + 1
            }
        except Exception as e:
            error_message = AIMessage(content=f"Error: {str(e)}")
            return {
                **state,
                "messages": [error_message],
                "iterations": iterations + 1
            }

    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """Determine if we should continue to tools or end"""
        messages = state["messages"]
        last_message = messages[-1]

        # Check if we've reached max iterations
        if state.get("iterations", 0) >= self.max_iterations:
            return "end"

        # Check if the last message has tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"

        # Check if the message content suggests tool use
        if isinstance(last_message, AIMessage):
            content = last_message.content.lower()
            # Look for tool usage indicators
            tool_indicators = ["calculate", "time",
                               "docker", "search", "memory"]
            if any(indicator in content for indicator in tool_indicators):
                return "continue"

        return "end"

    def run(self, task: str, verbose: bool = True) -> str:
        """
        Run the agent on a given task
        
        Args:
            task: The task or question for the agent
            verbose: Whether to print detailed output
        
        Returns:
            The agent's final response
        """
        if verbose:
            print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
            print(
                f"{Colors.BOLD}{Colors.CYAN}Running Agent: {self.model_name}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
            print(f"\n{Colors.GREEN}Task:{Colors.END} {task}\n")

        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=task)],
            "task": task,
            "result": "",
            "iterations": 0,
            "max_iterations": self.max_iterations
        }

        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)

            # Extract the final message
            if final_state["messages"]:
                last_message = final_state["messages"][-1]
                result = last_message.content if hasattr(
                    last_message, 'content') else str(last_message)
            else:
                result = "No response generated."

            if verbose:
                print(f"{Colors.GREEN}Response:{Colors.END}")
                print("-" * 70)
                print(result)
                print("-" * 70)
                print(
                    f"{Colors.CYAN}Iterations: {final_state['iterations']}{Colors.END}\n")

            return result

        except Exception as e:
            error_msg = f"Error running agent: {str(e)}"
            if verbose:
                print(f"{Colors.RED}{error_msg}{Colors.END}")
            return error_msg


# ============================================================================
# SIMPLE REACT AGENT (Without Tools)
# ============================================================================

class SimpleReActAgent:
    """A simple ReAct agent without external tools"""

    def __init__(
        self,
        model_name: str = "llama3.2",
        base_url: str = "http://localhost:11434"
    ):
        self.llm = Ollama(model=model_name, base_url=base_url)

    def run(self, task: str, verbose: bool = True) -> str:
        """Run ReAct reasoning on a task"""

        if verbose:
            print(f"\n{Colors.BOLD}{Colors.BLUE}Simple ReAct Agent{Colors.END}")
            print(f"{Colors.GREEN}Task:{Colors.END} {task}\n")

        prompt = f"""Solve this task using ReAct (Reasoning + Acting) format:

Task: {task}

Use this format:
Thought: [Your reasoning about what to do next]
Action: [The action you would take]
Observation: [What you would observe from that action]
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: [Your final answer]

Begin:"""

        try:
            response = self.llm.invoke(prompt)

            if verbose:
                print(f"{Colors.GREEN}Response:{Colors.END}")
                print("-" * 70)
                print(response)
                print("-" * 70)

            return response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if verbose:
                print(f"{Colors.RED}{error_msg}{Colors.END}")
            return error_msg


# ============================================================================
# MULTI-AGENT COLLABORATION
# ============================================================================

class MultiAgentSystem:
    """System with multiple specialized agents"""

    def __init__(
        self,
        model_name: str = "llama3.2",
        base_url: str = "http://localhost:11434"
    ):
        self.llm = Ollama(model=model_name, base_url=base_url)

    def run_specialist(self, task: str, specialty: str, verbose: bool = True) -> str:
        """Run a specialist agent"""

        specialist_prompts = {
            "coder": "You are an expert Python programmer. Provide clean, efficient code with explanations.",
            "analyst": "You are a data analyst. Provide insights, patterns, and recommendations.",
            "debugger": "You are a debugging expert. Identify issues and provide solutions.",
            "architect": "You are a system architect. Design scalable, maintainable solutions."
        }

        system_prompt = specialist_prompts.get(
            specialty,
            "You are a helpful AI assistant."
        )

        full_prompt = f"{system_prompt}\n\nTask: {task}"

        if verbose:
            print(
                f"\n{Colors.BOLD}{Colors.YELLOW}Specialist: {specialty.upper()}{Colors.END}")
            print(f"{Colors.GREEN}Task:{Colors.END} {task}\n")

        try:
            response = self.llm.invoke(full_prompt)

            if verbose:
                print(f"{Colors.GREEN}Response:{Colors.END}")
                print("-" * 70)
                print(response)
                print("-" * 70)

            return response

        except Exception as e:
            return f"Error: {str(e)}"

    def collaborate(self, task: str, specialists: List[str], verbose: bool = True) -> dict:
        """Run multiple specialists on a task"""

        if verbose:
            print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
            print(
                f"{Colors.BOLD}{Colors.HEADER}Multi-Agent Collaboration{Colors.END}")
            print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")

        results = {}
        for specialist in specialists:
            results[specialist] = self.run_specialist(
                task, specialist, verbose)

        return results


# ============================================================================
# TEST SCENARIOS
# ============================================================================

def test_basic_agent(model_name: str = "llama3.2"):
    """Test basic agent functionality"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}TEST 1: Basic Agent with Tools{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")

    agent = OllamaAgent(model_name=model_name, max_iterations=3)

    tasks = [
        "What is 156 * 89? Calculate this for me.",
        "What is the current time?",
        "Search for documentation about Docker.",
    ]

    for task in tasks:
        agent.run(task)


def test_react_agent(model_name: str = "llama3.2"):
    """Test ReAct reasoning agent"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}TEST 2: ReAct Reasoning Agent{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")

    agent = SimpleReActAgent(model_name=model_name)

    task = "A farmer has 17 sheep. All but 9 die. How many sheep does the farmer have left?"
    agent.run(task)


def test_multi_agent(model_name: str = "llama3.2"):
    """Test multi-agent collaboration"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}TEST 3: Multi-Agent Collaboration{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")

    system = MultiAgentSystem(model_name=model_name)

    task = "Design a Python function to check if a string is a palindrome."
    specialists = ["coder", "debugger"]

    results = system.collaborate(task, specialists)

    # Summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}Collaboration Summary:{Colors.END}")
    print("="*70)
    for specialist, response in results.items():
        print(f"\n{Colors.BOLD}{specialist.upper()}:{Colors.END}")
        print(response[:200] + "..." if len(response) > 200 else response)


def test_complex_reasoning(model_name: str = "llama3.2"):
    """Test complex multi-step reasoning"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}TEST 4: Complex Reasoning with Multiple Tools{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")

    agent = OllamaAgent(model_name=model_name, max_iterations=5)

    task = """I need to troubleshoot a Docker container that can't pull images. 
First, check if Docker is running. Then search for documentation about this issue. 
Finally, calculate how many hours of downtime we've had if the issue started 3.5 hours ago."""

    agent.run(task)


def run_all_tests(model_name: str = "llama3.2"):
    """Run all test scenarios"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("="*70)
    print("  LANGGRAPH OLLAMA AGENT TEST SUITE")
    print(f"  Model: {model_name}")
    print("="*70)
    print(f"{Colors.END}")

    tests = [
        ("Basic Agent with Tools", test_basic_agent),
        ("ReAct Reasoning", test_react_agent),
        ("Multi-Agent Collaboration", test_multi_agent),
        ("Complex Reasoning", test_complex_reasoning),
    ]

    for i, (name, test_func) in enumerate(tests, 1):
        try:
            test_func(model_name)
        except Exception as e:
            print(f"{Colors.RED}Error in test '{name}': {str(e)}{Colors.END}")

        if i < len(tests):
            input(
                f"\n{Colors.YELLOW}Press Enter to continue to next test...{Colors.END}")

    print(f"\n{Colors.BOLD}{Colors.GREEN}All tests completed!{Colors.END}\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function"""
    import sys

    model_name = sys.argv[1] if len(sys.argv) > 1 else "llama3.2"

    print(f"{Colors.BOLD}{Colors.CYAN}LangGraph + Ollama Agent Test Script{Colors.END}")
    print(f"Model: {model_name}\n")

    print("Available tests:")
    print("  1. Basic Agent with Tools")
    print("  2. ReAct Reasoning Agent")
    print("  3. Multi-Agent Collaboration")
    print("  4. Complex Reasoning")
    print("  5. Run All Tests")
    print("  6. Custom Task")
    print()

    try:
        choice = input("Select test (1-6): ").strip()

        if choice == "1":
            test_basic_agent(model_name)
        elif choice == "2":
            test_react_agent(model_name)
        elif choice == "3":
            test_multi_agent(model_name)
        elif choice == "4":
            test_complex_reasoning(model_name)
        elif choice == "5":
            run_all_tests(model_name)
        elif choice == "6":
            task = input("\nEnter your task: ").strip()
            agent_type = input(
                "Agent type (basic/react/multi): ").strip().lower()

            if agent_type == "react":
                agent = SimpleReActAgent(model_name=model_name)
                agent.run(task)
            elif agent_type == "multi":
                system = MultiAgentSystem(model_name=model_name)
                specialists = input(
                    "Specialists (comma-separated, e.g., coder,debugger): ").strip().split(',')
                specialists = [s.strip() for s in specialists]
                system.collaborate(task, specialists)
            else:
                agent = OllamaAgent(model_name=model_name)
                agent.run(task)
        else:
            print("Invalid choice")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")


if __name__ == "__main__":
    main()
