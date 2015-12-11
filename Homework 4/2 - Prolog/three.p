same(X,[X|_],Y,[Y|_]).
same(X,[_|Xs],Y,[_|Ys]) :- same(X,Xs,Y,Ys). 

next_to(X,[X|_],Y,[_,Y|_]).
next_to(X,[_,X|_],Y,[Y|_]).
next_to(X,[_|Xs],Y,[_|Ys]) :- next_to(X,Xs,Y,Ys).

right(X,[_,X|_],Y,[Y|_]).
right(X,[_|Xs],Y,[_|Ys]) :- right(X,Xs,Y,Ys).
	
house(C,D,N,S,P) :-
	C = [_, _, _, _, _],
	D = [_, _, _, _, _],
	N = [_, _, _, _, _],
	S = [_, _, _, _, _],
	P = [_, _, _, _, _],
	
	N = [norwegian|_],
	D = [_,_,milk,_,_],
	same(english,N,red,C),
	same(spanish,N,dog,P),
	same(kools,S,yellow,C),
	next_to(chesterfields,S,fox,P),
	next_to(norwegian,N,blue,C),
	same(old_gold,S,snails,P),
	same(lucky_strike,S,orange,D),
	same(ukranian,N,tea,D),
	same(japanese,N,parliaments,S),
	next_to(kools,S,horse,P),
	same(coffee,D,green,C),
	right(green,C,ivory,C),
	
	same(DrinksWater,N,water,D),
	write(DrinksWater), writeln(' drinks water.'),
	same(KeepsZebra,N,zebra,P),
	write(KeepsZebra), writeln(' keeps zebra.').
	
solve :- house(C,D,N,S,P).