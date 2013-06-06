plen: {0, 6, 8, 10, 12} // value of the shortest permitted password
psets: {1, 2, 3, 4} // number of symbol sets that must be used
pdict: {1, 0}  // are passwords checked whether they match a dictionary
phist: {0, 1, 2, 3}  // history check of passwords resp. none, minimum (1 past password, exact match), strict (2 past passwords, string distance of 2), extreme (4 past passwords, string distance of 5)
prenew: {0, 1, 2, 3} // when the system asks users to renew passwords: never, annually, quarterly, monthly
pattempts: {1, 0} // is there a limit on wrong password attempts
pautorecover: {1, 0} // are forgotten passwords restored automatically(1), or is there human support(0)


****run: create sprks DB, run "code_get_post.py" in any IDE, run "http://localhost:8080/" in browser (if needed uncomment lines creating and populating the table),
**result: after checking if ID exists, all corresponding values for ID=1 will be preloaded by reading from DB through server
**alternative result: On preload, the system checks if requested ID exists, if Not -> alert to user and reset the form fields

***hit: "Confirm button" to write user data to DB, 
**result: DB entry is created if no such ID is found, user redirected to "http://localhost:8080/add" page, 
* DB entries can be created/updated by applying any changes and hitting the Confirm btn again

**alternative result: DB entry is updated for given ID if such ID is found
* DB entries can be created/updated by applying any changes and hitting the Confirm btn again

**all the data exchange is done through the server*/




