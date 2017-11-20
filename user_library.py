def x(email):
    library = {'morgan@nerdwallet.com': 23470}
    if email in library.keys():
        GH_id = library[email]
        return GH_id
    else: 
        return None
