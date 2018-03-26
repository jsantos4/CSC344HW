setup(12):-
	assert(block([12,1])),
	assert(block([12,2])),
	assert(block([12,3])),
	assert(block([12,4])),
	assert(block([12,5])),
	assert(block([12,6])),
	assert(block([12,7])),
	assert(block([12,8])),
	assert(block([12,9])),
        assert(block([12,10])),!.

setup(N) :-
	N1 is N + 1,
	assert(block([N, 1])),
	assert(block([N, 2])),
	assert(block([N, 3])),
	assert(block([N, 4])),
	assert(block([N, 5])),
	assert(block([N, 6])),
	assert(block([N, 7])),
	assert(block([N, 8])),
	assert(block([N, 9])),
	assert(block([N, 10])),
	setup(N1).

obstruct([]):-!.
obstruct([M|N]):-
	retract(block(M)),
	obstruct(N).

setObstacle([_,0,_],[]):-!.
setObstacle([X, Y, Width], Result) :-
	X1 is X + 1,
        Width1	is Width - 1,
	Y1 is 10 - Y + 1,
	between([X1, 10],[X1, Y1], Fill),
	append([[X1, 10]], Fill, Curr),
	setObstacle([X1, Width1, Y], Remaining),
	append(Curr, Remaining, Result).

createObstacles([],[]).
createObstacles([H|T],Obstacles):-
	setObstacle(H,A),
	createObstacles(T, Remaining),
	append(A, Remaining, Obstacles).

between([X, Y],[X,Y],[]):-!.
between([X, Y0], [X, Y1], Fill):-
	block([X, Y0]),
	block([X, Y1]),
	Y0 < Y1,
       	Y2 is Y0 + 1,
	between([X, Y2], [X, Y1], Remaining),
	append([[X, Y2]], Remaining, Fill).

between([X, Y0], [X, Y1], Fill):-
	block([X, Y0]),
	block([X, Y1]),
	Y0 > Y1,
	Y2 is Y0 - 1,
	between([X, Y2], [X, Y1], Remaining),
	append([[X, Y2]], Remaining, Fill).

between([X0, Y], [X1, Y], Fill):-
	block([X0, Y]),
	block([X1, Y]),
	X0 > X1,
	X2 is X0 + 1,
	between([X2, Y], [X1, Y], Remaining),
	append([[X2, Y]], Remaining, Fill).

between([X0, Y], [X1, Y], Fill):-
	block([X0, Y]),
	block([X1, Y]),
	X0 < X1,
	X2 is X0 - 1,
	between([X2, Y], [X1, Y], Remaining),
	append([[X2, Y]], Remaining, Fill).

path(south, [[X, Y, \]|[]], Path):- 
	X > 6,
       	X < 11,
       	between([X, Y], [12, Y], Path),!.

path(north, [[X, Y, /]|[[X, Y1, N]|M]], Path):-
	Y < Y1,
	between([X, Y], [X, Y1], Curr),
	path(east, [[X, Y1, N]|M], Frac),
	append(Curr, Frac, Path).

path(south, [[X, Y, /]|[[X, Y1, N]|M]], Path):-
	Y > Y1,
	between([X, Y], [X, Y1], Curr),
	path(north, [[X, Y1, N]|M], Frac),
	append(Curr, Frac, Path).

path(north, [[X, Y, \]|[[X, Y1, N]|M]], Path):-
	Y > Y1,
	between([X, Y], [X, Y1], Curr),
	path(east, [[X, Y1, N]|M], Frac),
	append(Curr, Frac, Path).

path(east, [[X, Y, /]|[[X1, Y, N]|M]], Path):-
	X < X1,
	between([X, Y], [X1, Y], Curr),
	path(north, [[X1, Y, N]|M], Frac),
	append(Curr, Frac, Path).

path(north, [[X, Y, \]|[[X1, Y, N]|M]], Path):-
	X < X1,
	between([X, Y], [X1, Y], Curr),
	path(north, [[X1, Y, N]|M], Frac),
	append(Curr, Frac, Path).


placeMirror(east, [X, Y, /],[X, Y1, /]):-
	block([X,Y1]),
	Y < Y1.

placeMirror(east, [X, Y, \], [X, Y1, \]):-
	block([X, Y1]),
	Y > Y1.

placeMirror(north, [X, Y, /], [X1, Y, /]):-
	block([X1, Y]),
	X > X1.

placeMirror(north, [X, Y, /], [X1, Y, \]):-
	block([X1, Y]),
	X < X1.

placeMirror(south, [X, Y, \], [X1, Y, \]):-
	block([X1, Y]),
	X < X1.

placeMirror(south, [X, Y, \], [X1, Y, /]):-
	block([X1, Y]),
	X > X1.

exempt(_, []):- !.
exempt(I, [M|N]):-
	I \= M,
	exempt(I,N).

valid([]):-!.
valid([M|N]):-
	obstacle(A),
	exempt(M, A),
	valid(N).

placeMirrors(H, _, []):- H > 6,!.
placeMirrors(H, Obstacles, [[X0, H, /],[X0, Y1, /], [X1, Y1, \], [X1, H, \]]):-
	setup(1),
	createObstacles(Obstacles, Obj),
	obstruct(Obj),
	block([X0, H]),
	X > 1, 
	X < 5,
	placeMirror(east, [X0, H, /], [X0, Y1, /]),
	Y1 > 6,
	placeMirror(north, [X0, Y1, /]),
	X1 > 6,
	X1 < 12,
	path(east, [[X0, H, /], [X0, Y1, /], [X1, Y1, \], [X1, H, \]], _).
