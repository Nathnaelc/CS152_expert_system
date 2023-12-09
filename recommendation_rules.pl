% Facts about sports facilities
% The structure is -> facility(Name, SportsOffered, Address, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, Accessibility)


% importing the sports_facilities.pl file as knowledge base
:- include('sports_facilities.pl').

% Rule to recommend a facility based on sport, location, and budget
recommend_facility(Sport, Location, Budget, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, _, Budget, _, _, _, _, _),
    (SportsOffered = Sport ; SportsOffered = various_sports).

% Rule to include time availability
recommend_facility(Sport, Location, Budget, Time, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, Time, Budget, _, _, _, _, _),
    (SportsOffered = Sport ; SportsOffered = various_sports).

% Rule to factor in indoor/outdoor preference
recommend_facility(Sport, Location, Budget, Time, Indoor_Outdoor, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, Time, Budget, Indoor_Outdoor, _, _, _, _),
    (SportsOffered = Sport ; SportsOffered = various_sports).

% Rule to consider group or individual activity preference
recommend_facility(Sport, Location, Budget, Time, Indoor_Outdoor, Group_Individual, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, Time, Budget, Indoor_Outdoor, Group_Individual, _, _, _),
    (SportsOffered = Sport ; SportsOffered = various_sports).

% Rule to include competitive or recreational preference
recommend_facility(Sport, Location, Budget, Time, Indoor_Outdoor, Group_Individual, Comp_Recreational, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, _, _),
    (SportsOffered = Sport ; SportsOffered = various_sports).

% Rule to consider special equipment needs
recommend_facility(Sport, Location, Budget, Time, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, _),
    (SportsOffered = Sport ; SportsOffered = various_sports).

% Rule to factor in accessibility requirements
recommend_facility(Sport, Location, Budget, Time, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, Accessibility, RecommendedFacility) :-
    facility(RecommendedFacility, SportsOffered, _, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, Accessibility),
    (SportsOffered = Sport ; SportsOffered = various_sports).
