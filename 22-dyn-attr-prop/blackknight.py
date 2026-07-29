"""
本类的灵感来自电影《巨蟒与圣杯》（Monty Python and the Holy Grail）中的
「黑骑士」一幕：亚瑟王与黑骑士搏斗，砍掉了他的双臂双腿，
但黑骑士拒绝认输。

# tag::BLACK_KNIGHT_DEMO[]
    >>> knight = BlackKnight()
    >>> knight.member
    next member is:
    'an arm'
    >>> del knight.member
    BLACK KNIGHT (loses an arm) -- 'Tis but a scratch.
    >>> del knight.member
    BLACK KNIGHT (loses another arm) -- It's just a flesh wound.
    >>> del knight.member
    BLACK KNIGHT (loses a leg) -- I'm invincible!
    >>> del knight.member
    BLACK KNIGHT (loses another leg) -- All right, we'll call it a draw.

# end::BLACK_KNIGHT_DEMO[]
"""

# tag::BLACK_KNIGHT[]
class BlackKnight:

    def __init__(self):
        self.phrases = [
            ('an arm', "'Tis but a scratch."),
            ('another arm', "It's just a flesh wound."),
            ('a leg', "I'm invincible!"),
            ('another leg', "All right, we'll call it a draw.")
        ]

    @property
    def member(self):
        print('next member is:')
        return self.phrases[0][0]

    @member.deleter
    def member(self):
        member, text = self.phrases.pop(0)
        print(f'BLACK KNIGHT (loses {member}) -- {text}')
# end::BLACK_KNIGHT[]
