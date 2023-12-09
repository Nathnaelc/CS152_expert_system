:- consult('recommendation_rules.pl').

print_facilities(Sport, Location) :-
    recommend_facility(Sport, Location, _, _, Facility),
    print(Facility), nl, fail.
print_facilities(_, _).
