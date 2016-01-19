##Getting Started

###Build the Bitiverse from Scratch
python generator.py

###Transfer a pixel space to a Bitcoin address
>> python
>> import pixelwriter as p
>> from_address = "YOUR SENDING BITCOIN ADDRESS THAT ALREADY OWNS PIXELS"
>> coords_set = [[100, 200], [150, 250]] # the edge coords of the rectangle within which you transfer pixels that you already own
>> destination = "SOME RECEIVING BITCOIN ADDRESS"
>> private_key = "The Sender's private key"
>> predecessor_inputs = {'output': 'TXHASH:TXINDEX', value: '900'} # UNSPENT OUTPUTS THAT OWN PIXELS
that are the senders.
>> p.write_transfer_tx(from_address, coords_set, destination, private_key,
                      predecessor_inputs, push=True, sign=True):

###Publish Contents in your pixel space
- Create a content instructions file.  Put it on the web somewhere.  Call that url the CONTENT_URL.
    - To create a valid content file run the following code, content_file_name can be anything:
      ```
      import python
      import content
      content.create_content_file(image_url, link_url, content_file_name)
      ```
    - Post this file on the web, its url is the CONTENT URL.

- Pick an image of the appropriate dimensions to go in your pixelspace.  Call its url the IMAGE URL.

- Pick a destination url that your pixel space links to, eg, "my-sweet-blog.com".
  If someone clicks on your designated pixelspace, they will be linked to that URL.

- Create and broadcast a 'publishing' transaction.  This creates a 'content pointer' in the blockchain
that others will use to populate your part of the pixelspace.  Note that this can be created at
any time.  But it will only be in effect when the pixels are properly owned by the publishing address.
```
>> python
import pixelwriter as p
from_address = "YOUR PUBLISHING BITCOIN ADDRESS THAT OWNS PIXELSPACE"

coords_set = [[40, 600], [90, 670]]
# THE Coordinates of the edge points of a rectangle.  
Within this rectangle any pixels that you also own will be populated according to the
instructions of your content-pointer.  The published image in the content instructions file
will be STRETCHED to the dimensions of this rectangle, even if you do not own all pixels.
It will not be written onto non-owned pixels of course.

avoid_inputs = ['txhash1', 'txhash2']
# TXHASHES that you do not want sent in a publishing transaction.
  This only pertains to specially marked ownership outputs which should not be used in a publishing
  transaction.  XXX TODO come up with a cleaner/easier solution for this.

private_key = "THE PRIVATE KEY OF THE OWNER ADDRESS"

p.content_tx(from_address, coords_set, content_url, private_key, avoid_inputs=[], push=True)
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
