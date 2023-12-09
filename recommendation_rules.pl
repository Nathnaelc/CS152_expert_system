% Facts about sports facilities
% The structure is -> facility(Name, SportsOffered, Address, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, Accessibility)


% importing the sports_facilities.pl file as knowledge base
:- include('sports_facilities.pl').

% Normalize sport names to handle variability in user input
normalize_sport('Soccer', soccer).
normalize_sport('soccer', soccer).
normalize_sport('Tennis', tennis).
normalize_sport('tennis', tennis).
normalize_sport('Rugby', rugby).
normalize_sport('rugby', rugby).
normalize_sport('Polo', polo).
normalize_sport('polo', polo).
normalize_sport('Equestrian', equestrian).
normalize_sport('equestrian', equestrian).
% Add similar rules for other sports

% Rule to recommend a facility based on sport, location, budget, and skill level
recommend_facility(Sport, Location, Budget, SkillLevel, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, _, Budget, _, _, _, _, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

% Rule to include time availability
recommend_facility(Sport, Location, Budget, SkillLevel, Time, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, Time, Budget, _, _, _, _, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

% Rule to factor in indoor/outdoor preference
recommend_facility(Sport, Location, Budget, SkillLevel, Time, Indoor_Outdoor, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, Time, Budget, Indoor_Outdoor, _, _, _, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

% Rule to consider group or individual activity preference
recommend_facility(Sport, Location, Budget, SkillLevel, Time, Indoor_Outdoor, Group_Individual, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, Time, Budget, Indoor_Outdoor, Group_Individual, _, _, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

% Rule to include competitive or recreational preference
recommend_facility(Sport, Location, Budget, SkillLevel, Time, Indoor_Outdoor, Group_Individual, Comp_Recreational, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, _, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

% Rule to consider special equipment needs
recommend_facility(Sport, Location, Budget, SkillLevel, Time, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

% Rule to factor in accessibility requirements
recommend_facility(Sport, Location, Budget, SkillLevel, Time, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, Accessibility, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, SkillLevel, Location, Time, Budget, Indoor_Outdoor, Group_Individual, Comp_Recreational, Equipment, Accessibility),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).

recommend_facility(Sport, Location, Budget, RecommendedFacility) :-
    normalize_sport(Sport, NormalizedSport),
    facility(RecommendedFacility, SportsOffered, _, Location, _, Budget, _, _, _, _, _),
    (SportsOffered = NormalizedSport ; SportsOffered = various_sports).
    

% Interactive User Interface Predicate
ask_preferences_and_recommend :-
    write('Enter preferred sport (e.g., Soccer): '), read(Sport),
    normalize_sport(Sport, NormalizedSport),
    write('Enter preferred location (e.g., Palermo): '), read(Location),
    write('Enter your budget (e.g., moderate): '), read(Budget),
    write('Enter your skill level (e.g., all_levels): '), read(SkillLevel),
    recommend_facility(NormalizedSport, Location, Budget, SkillLevel, Facility),
    ( Facility \= '' ->
        write('Recommended facility is: '), write(Facility), nl;
        write('No matching facility found.'), nl
    ).
