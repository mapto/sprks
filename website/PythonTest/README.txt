plen: {0, 6, 8, 10, 12} // value of the shortest permitted password
psets: {1, 2, 3, 4} // number of symbol sets that must be used
pdict: {1, 0}  // are passwords checked whether they match a dictionary
phist: {0, 1, 2, 3}  // history check of passwords resp. none, minimum (1 past password, exact match), strict (2 past passwords, string distance of 2), extreme (4 past passwords, string distance of 5)
prenew: {0, 1, 2, 3} // when the system asks users to renew passwords: never, annually, quarterly, monthly
pattempts: {1, 0} // is there a limit on wrong password attempts
pautorecover: {1, 0} // are forgotten passwords restored automatically(1), or is there human support(0)


/**** db queries used to create table *****/
*****depending on the data above - 
*****used in pw_policy index.html&code_get_post.py 
******/
CREATE dbtest
USE dbtest
CREATE TABLE pw_policy (id VARCHAR(20), plen INT, psets INT, pdict BOOL, phist INT, prenew INT, pattempts BOOL, pautorecover BOOL)
INSERT INTO pw_policy VALUES('test', 8,3,False,2,1,False,True)
/*****/



