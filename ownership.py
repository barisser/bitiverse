import csv
import db
import pixelwriter as p
import reader as r

def process_all():
    grid = db.load_grid()
    owners = db.load_owners()
    cont = True
    while cont:
        grid, owners, i = process(grid, owners)
        if i == 0:
            cont = False
    db.save_grid(grid)
    return grid, owners

def process(grid, owners):
    iterations = 0
    print "Searching through known owners."
    for owner in owners:
        print "Investigating owner: %s --- %s." % (owner[1], owner[2])
        txhash = owner[1].split(':')[0]
        output_n = int(owner[1].split(':')[1])
        next_output = r.where_was_output_spent(txhash, output_n)
        if not next_output is None: # THIS OUTPUT WAS SPENT hence continue iterating
            iterations += 1
            print "Processing txhash: %s." % str(next_output)
            grid, owners = read(next_output, grid, owners)
    return grid, owners, iterations

def read(txhash, grid, owners):
    data, _, inputs_array, block = r.read_tx(txhash)
    if len(data) > 2 and not data[0] == "C":
        grid, owners = read_transfer(txhash, data, inputs_array, grid, owners, block)
    return grid, owners

def adjust_ownership(grid, coords, new_owner, inputs_array, owners, change_recipient, block):
    """
    first output is always new recipient of space in coords (inclusive).  Second output
    is always change receipt.  So ownership must also be adjusted to this new output.
    """
    unspents = [x[1] for x in inputs_array]
    print "Applying new ownership to %s." % new_owner

    owners_info = dict([x[1], list(x)] for x in owners)
    owners_amts = dict([x[1], x[5]] for x in owners)

    if not new_owner in owners_amts.keys(): #both these checks can probably be removed since they are always true
        owners_amts[new_owner] = 0
    if not change_recipient in owners_amts.keys():
        ownerlist[change_recipient] = 0

    for x in range(coords[0][0], coords[1][0]+1): #this is also horrible
        for y in range(coords[0][1], coords[1][1]+1):  #inclusive always
            if grid[x][y][0] in unspents: #is authentically owned
                owners_amts[grid[x][y][0]] -= 1
                grid[x][y] = [new_owner, None] #link is is reset to null on change
                owners_amts[new_owner] += 1

    for x in range(0, p.universe_width):  #yes this is even more horrible I know
        for y in range(0, p.universe_height):
            if grid[x][y][0] in unspents: #is owned by inputs of tx
            #send them to change output
                owners_amts[grid[x][y][0]] -= 1
                grid[x][y][0] = change_recipient  #link id is unchanged for change
                owners_amts[change_recipient] += 1

    for owner in owners_amts.keys():
        amt = owners_amts[owner]
        assert amt >= 0
        if amt == 0:
            db.expire_owner(owner, block)

    return owners, ownerlist

def read_transfer(txhash, data, inputs_array, grid, owners, block):
    coords = p.decompress_coords(int(data))

    assert len(coords) == 2
    recipient = txhash + ":0"  #receiver should always be first output
    change_recipient = txhash + ":1" #second output should always receive change
    grid, owners = adjust_ownership(grid, coords, recipient, inputs_array, owners, change_recipient, block)
    return grid, owners
