# DempsterShafer
Implementation in Python for Dempster-Shafer algorythm

Algorithm will be explained with examples, including movie genre prediction from reviews(aka observations)


The main concept of Dempster-Shafer is that it is some sort of extension of probabilities, but instead of one value, it uses intervals. Lower limit of an interval - is the BELIEF that something can happen, upper limit of an interval - plausibility, which is calculated as: Pl(A)=1-Bel(non A)
A and non A values are calculated INDEPENDENTLY. The summ of beliefs for A and non A can be different from 1. Both values could be 0. If there is no information about A and non A, the interval would be [0,1] (0 belief and 1 plausibility). When more information is available, interval will become smaller, but it will respect this rule:  Bel(A)<=P(A)<=Pl(A)
If probability is known exactly, interval becomes: Bel(A)=P(A)=Pl(A)

Functionality is splitted in functions: combination, get_mass, get_beliefs, get_plausibility, filter_results, get_final_result

Algorithm is applying iteratively DS rule
'' is considered as alias for union for union of all possible elements and should be used where needed

Algorithm is implemented by guidance of this book
Inteligenta Artificiala: rationament probabilistic, tehnici de clasificare

Let's imagine that there is a site/resource which collects reviews about movies watched by users. Each user can vote for a specific genre or a set of genres with some confidence (let's say that a review for some movie can look like this: western 60%, action 30%, war 20%)
This algorithm can help merge all reviews in order to get some final result.

#TODO: add doi of book
#TODO: add link to wiki
#TODO: use words splitted by dot for reviews, this can make the algorithm more general
