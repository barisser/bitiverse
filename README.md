##Getting Started

###
```
pip install bitiverse
```

###Generate the Bitiverse Web Page.
```
import bitiverse.generator as g

g.make()  # this creates the page from the blockchain in a /static folder.
```
###Transfer Pixelspace
```
import bitiverse.pixelwriter as p
sender = 'a bitcoin address that owns pixelspace'
coords_set = [[300, 400], [500, 800]] # a pair of (x,y) coordinates representing far corners of a box
                                      # anything the sender owns will be transferred.  
                                      # Ownership need not perfectly match rectangle.
recipient = 'a bitcoin address receiving pixelspace'
sender_priv = 'the private key of the sender'
fee = 'a bitcoin transaction fee in Satoshi'

# if push = False the raw tx hex is returned instead of the hash

txhash = p.transfer(sender, coords_set, recipient, sender_priv, fee=15000, push=True)
```

###Publish content within a Pixelspace
```
import bitiverse.pixelwriter as p
from_address = 'a bitcoin address owning pixelspace within the coordinates_set'
coords_set = [[300, 400], [500, 800]] # a pair of xy coordinates representing far corners of a box
                                      # image will be stretched to these dimensions regardless of actual ownership
                                      # non-owned sections within box will not be affected (of course).
content_url = 'some url here' #this url should be created via content.py.  This describes the content of the pixelspace.
private_key = 'private key of publishing address'
# is push = False the raw tx hex is returned instead of the txhash
# the fee is in Satoshi.
txhash = p.publish(from_address, coords_set, content_url, private_key, push=True, fee=15000)
```

##Description

A finite space has been defined and will be governed on the Bitcoin Blockchain.
The pixels can be owned and transacted via Bitcoin private keys.  Ownership is
cryptographically self-evident as it is with bitcoins.  Pixels may be owned and
transacted freely and without censorship.

The owner of pixels within the Bitiverse may publish content at any time.  They
may point a content link at their pixels using a 'Content Transaction'.  This
publishes a URL to the blockchain from an address that owns pixels.  The content
at this URL indicates what lives in these pixels, within certain constraints.

Pixels are transacted via 'Transfer Transactions'.  These are also Bitcoin
transactions that signal the transfer of pixels within a certain zone.  Naturally
one may only transmit pixels that one already owns; this is verifiable from
the Blockchain history.

The Bitiverse is defined as a 1920x1080 pixel grid.  It shall remain so for all
time, with no expansion or diminishment.

The contents of the Bitiverse are whatever the protocol defines it as from the
Blockchain record.  The underlying content cannot be censored, even as its
expression may be censored by whichever medium carries it.  

PROTOCOL RULES

Pixels are tied to particular unspent Bitcoin outputs.  If these are transmitted
accidentally as part of normal Bitcoin transactions, the pixels are not destroyed, but
their ownership is transplanted wholly to the new bitcoins' owner.

TRANSFER Transactions

CONTENT Transactions

1920x1080

Each pixel is for sale all the time
pixels are owned by addresses through blockchain tokens
pixel contents are described via opreturn statements

selling pixels
atomic transaction between addresses
exchange tokens for bitcoins
opreturn statement says
  - pixel coordinates


defining content of pixels
  - pixel coordinates
  - hash of link contents
  - link with contents for behavior (rendered html)
