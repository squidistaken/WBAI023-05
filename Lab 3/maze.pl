% All open paths in the maze
open(a,b).
open(b,a).
open(b,f).
open(f,b).
open(c,d).
open(d,c).
open(c,g).
open(g,c).
open(d,h).
open(h,d).
open(e,f).
open(f,e).
open(f,j).
open(j,f).
open(g,k).
open(k,g).
open(h,l).
open(l,h).
open(i,m).
open(m,i).
open(j,k).
open(k,j).
open(m,n).
open(n,m).
open(n,o).
open(o,n).
open(l,p).
open(p,l).

% Path predicate
path(X, Y) :- path(X, Y, []).

% Scenario where there is a direct path where the cells are next to each other with an opening
path(X, Y, _) :- open(X, Y).

% Recursively find the path between X to Y via cells Z
path(X, Y, Visited) :- open(X, Z), Z \= Y, \+ member(Z, Visited), path(Z, Y, [X | Visited]).
