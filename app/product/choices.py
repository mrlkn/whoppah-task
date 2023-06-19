DRAFT = 'draft'
NEW = 'new'
REJECTED = 'rejected'
BANNED = 'banned'
ACCEPTED = 'accepted'

STATES = [DRAFT, NEW, REJECTED, BANNED, ACCEPTED]


STATE_CHOICES = [
    (DRAFT, 'Draft'),
    (NEW, 'New'),
    (REJECTED, 'Rejected'),
    (BANNED, 'Banned'),
    (ACCEPTED, 'Accepted')
]
