#!/usr/bin/env python3
"""
Comprehensive Llama3 Test Prompts
Tests various capabilities: reasoning, coding, analysis, creativity, and instruction-following
"""

import ollama
import time
from typing import Dict, List

# Color codes for terminal output


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class LlamaTestSuite:
    """Test suite for evaluating Llama3 performance"""

    def __init__(self, model: str = 'llama3.2', host: str = 'http://localhost:11434'):
        self.model = model
        self.client = ollama.Client(host=host)
        self.results = []

    def run_test(self, category: str, prompt: str, description: str) -> Dict:
        """Run a single test and collect results"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}Category: {category}{Colors.END}")
        print(f"{Colors.YELLOW}Test: {description}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"\n{Colors.GREEN}Prompt:{Colors.END} {prompt}\n")
        print(f"{Colors.GREEN}Response:{Colors.END}")
        print("-" * 70)

        start_time = time.time()

        try:
            response = ""
            for chunk in self.client.generate(model=self.model, prompt=prompt, stream=True):
                content = chunk.get('response', '')
                print(content, end='', flush=True)
                response += content

            elapsed_time = time.time() - start_time
            print(f"\n{'-'*70}")
            print(
                f"{Colors.CYAN}⏱ Completed in {elapsed_time:.2f} seconds{Colors.END}")

            result = {
                'category': category,
                'description': description,
                'prompt': prompt,
                'response': response,
                'time': elapsed_time,
                'success': True
            }

        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
            result = {
                'category': category,
                'description': description,
                'prompt': prompt,
                'response': None,
                'time': elapsed_time,
                'success': False,
                'error': str(e)
            }

        self.results.append(result)
        return result

    def run_all_tests(self):
        """Run all test prompts"""

        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("="*70)
        print("  LLAMA3 COMPREHENSIVE TEST SUITE")
        print("="*70)
        print(f"{Colors.END}\n")

        # Test 1: Reasoning & Logic
        self.run_test(
            category="Reasoning & Logic",
            description="Multi-step reasoning problem",
            prompt="""A farmer has 17 sheep. All but 9 die. How many sheep does the farmer have left?

Think through this step-by-step and explain your reasoning."""
        )

        # Test 2: Coding - Python
        self.run_test(
            category="Coding",
            description="Write a Python function",
            prompt="""Write a Python function that finds the longest palindromic substring in a given string. 
Include docstring, type hints, and handle edge cases. Make it efficient."""
        )

        # Test 3: Data Analysis
        self.run_test(
            category="Analysis",
            description="Analyze data patterns",
            prompt="""Given this data:
Sales Q1: $120K (up 15% from last year)
Sales Q2: $95K (down 8% from last year)
Sales Q3: $180K (up 42% from last year)
Sales Q4: $150K (up 22% from last year)

Analyze the trends, identify potential causes, and provide 3 actionable recommendations."""
        )

        # Test 4: Creative Writing
        self.run_test(
            category="Creativity",
            description="Creative writing with constraints",
            prompt="""Write a 4-sentence story about AI that:
1. Uses exactly 4 sentences
2. Each sentence starts with a different letter: A, I, N, S
3. Includes a plot twist
4. Ends on a hopeful note"""
        )

        # Test 5: Technical Explanation
        self.run_test(
            category="Technical Explanation",
            description="ELI5 complex concept",
            prompt="""Explain how Docker containers work using only analogies that a 10-year-old would understand. 
No technical jargon allowed."""
        )

        # Test 6: Code Review
        self.run_test(
            category="Coding",
            description="Code review and improvement",
            prompt="""Review this Python code and suggest improvements:

def calc(x, y, op):
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y

List: 1) bugs, 2) style issues, 3) improved version"""
        )

        # Test 7: Problem Solving
        self.run_test(
            category="Problem Solving",
            description="Algorithm design",
            prompt="""Design an algorithm to detect if a meeting room is available given:
- A list of booked time slots: [(9,10), (11,13), (14,15)]
- New meeting request: (13, 14)

Explain your approach and provide pseudocode."""
        )

        # Test 8: Context Following
        self.run_test(
            category="Instruction Following",
            description="Follow specific format",
            prompt="""List 5 benefits of containerization in this EXACT format:
BENEFIT: [name]
WHY: [one sentence explanation]
EXAMPLE: [specific use case]

(Repeat 5 times, numbered)"""
        )

        # Test 9: Edge Case Thinking
        self.run_test(
            category="Critical Thinking",
            description="Identify edge cases",
            prompt="""I'm building a function to calculate age from birthdate. 
List 7 edge cases I should handle, ordered from most to least critical."""
        )

        # Test 10: Practical Application
        self.run_test(
            category="Practical Application",
            description="Zscaler certificate troubleshooting",
            prompt="""A Docker container can't pull images due to Zscaler proxy. 
The error is: "x509: certificate signed by unknown authority"

Provide:
1. Root cause (1 sentence)
2. Quick fix (3 steps)
3. Proper solution (with example code)"""
        )

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print(f"\n\n{Colors.BOLD}{Colors.HEADER}")
        print("="*70)
        print("  TEST SUMMARY")
        print("="*70)
        print(f"{Colors.END}\n")

        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        total_time = sum(r['time'] for r in self.results)

        print(f"{Colors.BOLD}Total Tests:{Colors.END} {total_tests}")
        print(f"{Colors.GREEN}Successful:{Colors.END} {successful_tests}")
        print(f"{Colors.RED}Failed:{Colors.END} {total_tests - successful_tests}")
        print(f"{Colors.CYAN}Total Time:{Colors.END} {total_time:.2f} seconds")
        print(
            f"{Colors.CYAN}Average Time:{Colors.END} {total_time/total_tests:.2f} seconds per test")

        print(f"\n{Colors.BOLD}Results by Category:{Colors.END}")
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'success': 0, 'total': 0, 'time': 0}
            categories[cat]['total'] += 1
            categories[cat]['time'] += result['time']
            if result['success']:
                categories[cat]['success'] += 1

        for cat, stats in categories.items():
            success_rate = (stats['success'] / stats['total']) * 100
            avg_time = stats['time'] / stats['total']
            status = f"{Colors.GREEN}✓{Colors.END}" if success_rate == 100 else f"{Colors.RED}✗{Colors.END}"
            print(
                f"  {status} {cat}: {stats['success']}/{stats['total']} ({success_rate:.0f}%) - avg {avg_time:.2f}s")

        print(f"\n{Colors.BOLD}{Colors.GREEN}Testing complete!{Colors.END}\n")


# Quick single tests for rapid validation
QUICK_TESTS = {
    "hello_world": {
        "prompt": "Say 'Hello, World!' and explain what Docker containers are in exactly 2 sentences.",
        "description": "Basic response test"
    },

    "reasoning": {
        "prompt": "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
        "description": "Quick reasoning check"
    },

    "code": {
        "prompt": "Write a Python one-liner to reverse a string.",
        "description": "Simple coding test"
    },

    "math": {
        "prompt": "Calculate: (15 * 8) + (120 / 4) - 17. Show your work.",
        "description": "Basic math operations"
    },

    "instruction": {
        "prompt": "List exactly 3 Docker commands. Format: COMMAND - DESCRIPTION. No extra text.",
        "description": "Instruction following"
    }
}


def run_quick_test(test_name: str, model: str = 'llama3.2'):
    """Run a single quick test"""
    if test_name not in QUICK_TESTS:
        print(f"Unknown test: {test_name}")
        print(f"Available tests: {', '.join(QUICK_TESTS.keys())}")
        return

    test = QUICK_TESTS[test_name]
    suite = LlamaTestSuite(model=model)
    suite.run_test(
        category="Quick Test",
        description=test['description'],
        prompt=test['prompt']
    )


def main():
    """Main function"""
    import sys

    print(f"{Colors.BOLD}{Colors.CYAN}Llama3 Test Suite{Colors.END}\n")

    # Check if model is available
    try:
        client = ollama.Client(host='http://localhost:11434')
        models = client.list()
        print(
            f"Available models: {', '.join([m['name'] for m in models.get('models', [])])}\n")
    except Exception as e:
        print(f"{Colors.RED}Error connecting to Ollama: {e}{Colors.END}")
        print("Make sure Ollama is running: docker compose up -d")
        return

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'quick':
            test_name = sys.argv[2] if len(sys.argv) > 2 else 'hello_world'
            run_quick_test(test_name)
        elif sys.argv[1] == 'list':
            print("Available quick tests:")
            for name, test in QUICK_TESTS.items():
                print(f"  - {name}: {test['description']}")
        else:
            print("Usage:")
            print("  python test_prompts.py              # Run full test suite")
            print("  python test_prompts.py quick        # Run quick hello_world test")
            print(
                "  python test_prompts.py quick [name] # Run specific quick test")
            print("  python test_prompts.py list         # List available quick tests")
    else:
        # Run full test suite
        suite = LlamaTestSuite(model='llama3.2')
        suite.run_all_tests()


if __name__ == "__main__":
    main()
