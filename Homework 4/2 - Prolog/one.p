% getMove(+MissionaryCount,+CannibalCount): Missionaries are not outnumbered in transit.
getMove(2, 0).
getMove(0, 2).
getMove(1, 0).
getMove(0, 1).
getMove(1, 1).

% valid(+MissionaryCount, +CannibalCount): Missionaries are not outnumbered on land.
valid(0, C) :- validAmount(C).
valid(M, C) :- M >= C, validAmount(M), validAmount(C).
% validAmount(+PersonCount): There are [0,3] people.
validAmount(X) :- X >= 0, X =< 3.

% newMove(+InitialState, -FinalState, -Move): Generate a new move.
% Boat is on the left
newMove((Mi,Ci,left), (Mf,Cf,right), (M,C,right)) :-
	getMove(M, C),
	Mf is Mi - M, Cf is Ci - C, valid(Mf, Cf), % Valid final state on left coast
	Mo is 3 - Mf, Co is 3 - Cf, valid(Mo, Co). % Valid final state on right coast
% Boat is on the right
newMove((Mi,Ci,right), (Mf,Cf,left), (M,C,left)) :-
	getMove(M, C),
	Mf is Mi + M, Cf is Ci + C, valid(Mf, Cf), % Valid final state on left coast
	Mo is 3 - Mf, Co is 3 - Cf, valid(Mo, Co). % Valid final state on right coast

% visited(+TestState, +VisitedStates): TestState is in VisitedStates.
visited(X, [X|_]).
visited(X, [_|Y]) :- visited(X, Y).

% mc(+CurrentState,+VisitedStates,-Moves): Generate Moves to get from CurrentState to
% the final state (everyone crossed the river), without repeating VisitedStates.
% A state is (MissionaryCount,CannibalCount,BoatLocation), describing the left coast.
mc((0,0,right), _, []).
mc(Current, Visited, [Move|RestMoves]) :-
	newMove(Current, Next, Move),
	\+visited(Next, Visited),
	mc(Next, [Next|Visited], RestMoves).

% Solve the Missionaries and Cannibals problem, and output the simplest schedule of moves.
solve :-
	setof(Moves, mc((3,3,left), [(3,3,left)], Moves), MovesSet),
	shortestSublist(MovesSet, _, SimplestMoves),
	writeln('Moves Required:'),
	print(SimplestMoves).

% len(+List, -Length): Returns number of elements in List.
len([], 0).
len([_|T], N+1) :- len(T, N).

% shortestSublist(+Lists, -Length, -ShortestList): Find the shortest list in a list of lists.
shortestSublist([L], N, L) :- len(L, N). % Only one sublist
shortestSublist([H|T], N, L) :-
	shortestSublist(T, N_T, L_T), len(H, N_H),
	(N_H < N_T ->
		N = N_H, L = H;
		N = N_T, L = L_T).

% print(+Moves): print all moves in the list
print([]).	
print([X|Y]) :-
	printMove(X),
	print(Y).
% printMove(+(MissionaryCount,CannibalCount,BoatDirection))
printMove((X,Y,Z)) :- write('M'),write(X),write(' '),write('C'),write(Y),write(' '),writeln(Z).
