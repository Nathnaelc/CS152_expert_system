import subprocess


def run_prolog_query(sport, location):
    # Command to run Prolog script with arguments
    command = ["swipl", "-s", "run_query.pl", "-g",
               f"print_facilities({sport},{location}),halt"]

    # Running the command and capturing output
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def query_prolog_and_display_results(sport, location):
    results = run_prolog_query(sport, location)
    print("Recommended facilities:\n", results)


# Example usage
if __name__ == "__main__":
    query_prolog_and_display_results('soccer', 'palermo')
