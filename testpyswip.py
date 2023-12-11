import os
from pyswip import Prolog


def main():
    prolog = Prolog()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    prolog_file = os.path.join(dir_path, "recommendation_rules.pl")
    prolog.consult(prolog_file)

    # Test Query
    query_string = f"recommend_facility('soccer', 'la_paternal', 'moderate', 'all_levels', Facility)"
    print(f"Querying Prolog with: {query_string}")
    try:
        results = list(prolog.query(query_string))
        print(f"Results: {results}")
    except Exception as e:
        print(f"Error during Prolog query: {e}")


if __name__ == "__main__":
    main()
