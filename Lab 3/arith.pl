% isnumber(X) is true if X is a isnumber

isnumber(0).
isnumber(s(X)) :- isnumber(X).

% plus(X,Y,Z) is true if X + Y = Z

plus(0,X,X) :- isnumber(X).
plus(s(X),Y,s(Z)) :- plus(X,Y,Z).

% minus(X,Y,Z) is true if X - Y =Z

minus(X,0,X) :- isnumber(X).
minus(s(X),s(Y),Z) :- minus(X,Y,Z).

% times(X,Y,Z) is true if X * Y = Z

times(X,0,0) :- isnumber(X).
times(X,s(Y),Z) :- times(X,Y,Z1), plus(X,Z1,Z).

% pow(X,Y,Z) is true if X^Y = Z

pow(X,0,s(0)) :- isnumber(X).
pow(X,s(Y),Z) :- pow(X,Y,Z1), times(X,Z1,Z).

% even(X) is true if X % 2 = 0

even(0).
even(s(s(X))) :- even(X).

% odd(X) is true if X % 2 != 0

odd(s(0)).
odd(s(s(X))) :- odd(X).

% div2(X, Y) is true if X / 2 = Y

div2(0, 0).
div2(s(s(X)), s(Y)) :- div2(X, Y).

% divi2(X, Y) is true if times(Y, 2, X) is true

divi2(X, Y) :- times(Y, s(s(0)), X).