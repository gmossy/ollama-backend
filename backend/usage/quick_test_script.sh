#!/bin/bash

# Quick test script for Llama3 in Ollama
# Usage: ./quick_test.sh [test_name] [model]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

MODEL=${2:-llama3.2}
CONTAINER="zscaler-ollama"

# Check if Ollama is running
check_ollama() {
    if ! docker ps | grep -q "$CONTAINER"; then
        echo -e "${RED}Error: Ollama container is not running${NC}"
        echo "Start it with: docker compose up -d"
        exit 1
    fi
    
    if ! curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        echo -e "${RED}Error: Cannot connect to Ollama API${NC}"
        exit 1
    fi
}

# Run a test
run_test() {
    local test_name=$1
    local prompt=$2
    local description=$3
    
    # Create a line of 70 '=' characters
    EQUAL_LINE=$(printf '%*s' 70 | tr ' ' '=')

    echo -e "\n${BOLD}${BLUE}${EQUAL_LINE}${NC}"
    echo -e "${BOLD}${CYAN}Test: $test_name${NC}"
    echo -e "${YELLOW}Description: $description${NC}"
    echo -e "${BOLD}${BLUE}${EQUAL_LINE}${NC}"
    echo -e "\n${GREEN}Prompt:${NC} $prompt\n"
    echo -e "${GREEN}Response:${NC}"
    echo "----------------------------------------------------------------------"
    
    START=$(date +%s)
    
    # Use `echo` and pipe to ensure prompt is sent with EOF,
    # and environment variables for insecure modes
    echo "$prompt" | docker exec -i "$CONTAINER" bash -c "export OLLAMA_INSECURE=true && export SSL_CERT_FILE=/dev/null && export GIT_SSL_NO_VERIFY=true && export CURL_CA_BUNDLE=/dev/null && ollama run \"$MODEL\""
    
    END=$(date +%s)
    ELAPSED=$((END - START))
    
    echo "----------------------------------------------------------------------"
    echo -e "${CYAN}⏱  Completed in ${ELAPSED} seconds${NC}\n"
}

# Test definitions
test_hello() {
    run_test "Hello World" \
        "Say 'Hello, World!' and explain what Docker containers are in exactly 2 sentences." \
        "Basic connectivity and response test"
}

test_reasoning() {
    run_test "Reasoning" \
        "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?" \
        "Quick reasoning check"
}

test_code() {
    run_test "Simple Code" \
        "Write a Python one-liner to reverse a string." \
        "Basic coding ability"
}

test_math() {
    run_test "Math" \
        "Calculate: (15 * 8) + (120 / 4) - 17. Show your work." \
        "Arithmetic operations"
}

test_instruction() {
    run_test "Instruction Following" \
        "List exactly 3 Docker commands. Format: COMMAND - DESCRIPTION. No extra text." \
        "Format adherence"
}

test_sheep() {
    run_test "Logic Puzzle" \
        "A farmer has 17 sheep. All but 9 die. How many sheep does the farmer have left? Think through this step-by-step." \
        "Multi-step reasoning"
}

test_palindrome() {
    run_test "Python Coding" \
        "Write a Python function that finds the longest palindromic substring in a given string. Include docstring, type hints, and handle edge cases." \
        "Code generation with best practices"
}

test_analysis() {
    run_test "Data Analysis" \
        "Given sales data: Q1: \$120K (up 15%), Q2: \$95K (down 8%), Q3: \$180K (up 42%), Q4: \$150K (up 22%). Analyze trends and provide 3 recommendations." \
        "Pattern recognition and business insight"
}

test_creative() {
    run_test "Creative Writing" \
        "Write a 4-sentence story about AI. Each sentence must start with: A, I, N, S. Include a plot twist and end hopefully." \
        "Creativity with constraints"
}

test_eli5() {
    run_test "ELI5" \
        "Explain how Docker containers work using only analogies that a 10-year-old would understand. No technical jargon." \
        "Simplification and analogy"
}

test_review() {
    run_test "Code Review" \
        "Review this code and suggest improvements:

def calc(x, y, op):
    if op == '+': return x + y
    elif op == '-': return x - y
    elif op == '*': return x * y
    elif op == '/': return x / y

List bugs, style issues, and provide improved version." \
        "Critical analysis"
}

test_algorithm() {
    run_test "Algorithm Design" \
        "Design an algorithm to check if a meeting room is available. Booked slots: [(9,10), (11,13), (14,15)]. New request: (13,14). Explain approach and provide pseudocode." \
        "Problem-solving and algorithmic thinking"
}

test_zscaler() {
    run_test "Practical Troubleshooting" \
        "Docker container can't pull images. Error: 'x509: certificate signed by unknown authority'. Provide: 1) Root cause, 2) Quick fix (3 steps), 3) Proper solution with code." \
        "Technical troubleshooting"
}

test_custom() {
    echo -e "${YELLOW}Enter your prompt (press Ctrl+D when done):${NC}"
    PROMPT=$(cat)
    run_test "Custom Prompt" "$PROMPT" "User-defined test"
}

# Show help
show_help() {
    echo -e "${BOLD}${CYAN}Llama3 Quick Test Script${NC}\n"
    echo "Usage: ./quick_test.sh [test_name] [model]"
    echo ""
    echo "Available tests:"
    echo "  hello       - Hello World (basic connectivity)"
    echo "  reasoning   - Logic puzzle"
    echo "  code        - Simple Python code"
    echo "  math        - Arithmetic calculation"
    echo "  instruction - Format following"
    echo "  sheep       - Reasoning puzzle (farmer's sheep)"
    echo "  palindrome  - Python function with best practices"
    echo "  analysis    - Data analysis and recommendations"
    echo "  creative    - Creative writing with constraints"
    echo "  eli5        - Explain Docker in simple terms"
    echo "  review      - Code review and improvement"
    echo "  algorithm   - Algorithm design"
    echo "  zscaler     - Zscaler certificate troubleshooting"
    echo "  custom      - Enter your own prompt"
    echo "  all         - Run all quick tests (5 tests)"
    echo "  full        - Run comprehensive suite (13 tests)"
    echo ""
    echo "Examples:"
    echo "  ./quick_test.sh hello"
    echo "  ./quick_test.sh code mistral"
    echo "  ./quick_test.sh custom"
    echo ""
    echo "Default model: llama3.2"
}

# Run all quick tests
test_all() {
    echo -e "${BOLD}${CYAN}Running Quick Test Suite${NC}"
    echo -e "Model: $MODEL\n"
    
    test_hello
    test_reasoning
    test_code
    test_math
    test_instruction
    
    echo -e "\n${BOLD}${GREEN}Quick test suite completed!${NC}"
}

# Run full test suite
test_full() {
    echo -e "${BOLD}${CYAN}Running Full Test Suite${NC}"
    echo -e "Model: $MODEL\n"
    echo -e "${YELLOW}This will take several minutes...${NC}\n"
    
    test_hello
    test_reasoning
    test_sheep
    test_code
    test_palindrome
    test_math
    test_analysis
    test_creative
    test_eli5
    test_review
    test_algorithm
    test_instruction
    test_zscaler
    
    echo -e "\n${BOLD}${GREEN}Full test suite completed!${NC}"
}

# Main
main() {
    check_ollama
    
    TEST_NAME=${1:-help}
    
    case $TEST_NAME in
        hello)       test_hello ;;
        reasoning)   test_reasoning ;;
        code)        test_code ;;
        math)        test_math ;;
        instruction) test_instruction ;;
        sheep)       test_sheep ;;
        palindrome)  test_palindrome ;;
        analysis)    test_analysis ;;
        creative)    test_creative ;;
        eli5)        test_eli5 ;;
        review)      test_review ;;
        algorithm)   test_algorithm ;;
        zscaler)     test_zscaler ;;
        custom)      test_custom ;;
        all)         test_all ;;
        full)        test_full ;;
        help|--help|-h) show_help ;;
        *)
            echo -e "${RED}Unknown test: $TEST_NAME${NC}"
            echo "Run './quick_test.sh help' for available tests"
            exit 1
            ;;
    esac
}

main "$@"
