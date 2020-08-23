# metaheuristics

Problem 3-partition dotyczy uporządkowania skończonego zbioru liczb naturalnych na trzy podzbiory (lub w innej wersji - uporządkowania zbioru na wielokrtotność trójek), 
które mają tę samą sumę.

Problem jest NP-zupełny co oznacza, że trudno go rozwiązać, ale łatwo sprawdzić poprawność przedstawionego rozwiązania.
W rozwiązywanym przeze mnie przypadku wystarczy obliczyć sumę danych wejściowych podzielonych przez 3 oraz sumę poszczególnych, podzielonych trójek,
a następnie za pomocą instrukcji warunkowej sprawdzić, czy wartości są sobie równe.

Przykład:

DANE WEJŚCIOWE:
1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 10, 12, 15, 18, 19, 21

DANE WYJŚCIOWE:
(1, 6, 9, 12, 15, 18), 61
(4, 7, 10, 19, 21), 61
(1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10), 61

Podczas semestru zajęć dotyczących metaheurystyk udało mi się nauczyć podstaw pythona, stworzyć metodę siłową oraz wspinaczkową.
