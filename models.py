# class BaseModel:
#     id: str
#     name: str #type.object.name

#     def __init__(self, id):
#         self.id = id

class Track:
    artist: str #music.recording.artist
    tracks: str 

    def __init__(self, id):
        self.id = id

class TrackContribution:
    contributor: str
    role: str
    track: str

    def __init__(self, id):
        self.id = id

# <http://rdf.freebase.com/ns/type.object.type>   <http://rdf.freebase.com/ns/music.recording>
class Recording:
    artists = [] # <http://rdf.freebase.com/ns/music.recording.artist> (v strede), v pravo je potom ID
    tracks = [] # <http://rdf.freebase.com/ns/music.recording.tracks> (v strede), v pravo je ID pre tracks
    length = int # <http://rdf.freebase.com/ns/music.recording.length> (v strede), v  pravo je potom value
    awards_won = [] # <http://rdf.freebase.com/ns/m.014brgq>  <http://rdf.freebase.com/ns/award.award_winning_work.awards_won>        <http://rdf.freebase.com/ns/m.0jzl1zk>
    awards_nominated = [] # <http://rdf.freebase.com/ns/m.014brgq>  <http://rdf.freebase.com/ns/award.award_nominated_work.award_nominations>      <http://rdf.freebase.com/ns/m.0k0c_tx>

    # song ??????? <http://rdf.freebase.com/ns/g.11b6t7wc6p>       <http://rdf.freebase.com/ns/music.recording.song>       <http://rdf.freebase.com/ns/m.05cmg8>
# <http://rdf.freebase.com/ns/type.object.type>   <http://rdf.freebase.com/ns/music.release_track>

    def __init__(self, id):
        self.id = id
        self.artists = []
        self.tracks = []
        self.awards_won = []
        self.awards_nominated = []

class ReleaseTrack:
    track_number: int # <http://rdf.freebase.com/ns/music.release_track.track_number> (v strede), vpravo je potom value
    disc_number: int # <http://rdf.freebase.com/ns/music.release_track.disc_number> (v strede), vpravo je potom value
    release: str # <http://rdf.freebase.com/ns/music.release_track.release> (v strede), vpravo je potom ID
    recording: str # <http://rdf.freebase.com/ns/music.release_track.recording> (v strede), vpravo je potom ID

    def __init__(self, id):
        self.id = id
# <http://rdf.freebase.com/ns/m.014brgq>  <http://rdf.freebase.com/ns/award.award_nominated_work.award_nominations>      <http://rdf.freebase.com/ns/m.0k0c_tx>

class Album:
    artists = [] # <http://rdf.freebase.com/ns/g.112yfy2xr>        <http://rdf.freebase.com/ns/music.album.artist> <http://rdf.freebase.com/ns/m.0nb89sw>
    release_date: str # <http://rdf.freebase.com/ns/g.112yfy2xr>        <http://rdf.freebase.com/ns/music.album.release_date>   "2009"^^<http://www.w3.org/2001/XMLSchema#gYear>
    description: str # <http://rdf.freebase.com/ns/g.112yfy2xr>        <http://rdf.freebase.com/ns/common.topic.description>   "Guilty Pleasures Love is a solo album from Scott Murphy."@en
    release_type: str # '<http://rdf.freebase.com/ns/g.112yfy2xr>\t<http://rdf.freebase.com/ns/music.album.release_type>\t<http://rdf.freebase.com/ns/m.02lx2r>\t.\n'
    awards_nominated = []

    def __init__(self, id):
        self.id = id
        self.artists = []
        self.awards_nominated = []


# <http://rdf.freebase.com/ns/type.object.type>   <http://rdf.freebase.com/ns/music.artist>
# <http://rdf.freebase.com/ns/kg.object_profile.prominent_type>   <http://rdf.freebase.com/ns/music.artist>
# <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>       <http://rdf.freebase.com/ns/music.artist>
class Artist:
    name: str # <http://rdf.freebase.com/ns/g.12148s8q> <http://rdf.freebase.com/ns/type.object.name>   "Marco Berrini"@en      .
    active_start: str # <http://rdf.freebase.com/ns/music.artist.active_start>    "1990"^^<http://www.w3.org/2001/XMLSchema#gYear>
    active_end: str # <http://rdf.freebase.com/ns/music.artist.active_end>    "1990"^^<http://www.w3.org/2001/XMLSchema#gYear>
    origin: str # <http://rdf.freebase.com/ns/g.119pgq6k0>        <http://rdf.freebase.com/ns/music.artist.origin>        <http://rdf.freebase.com/ns/m.049d1>
    genre: str # <http://rdf.freebase.com/ns/g.119pgq6k0>        <http://rdf.freebase.com/ns/music.artist.genre> <http://rdf.freebase.com/ns/m.05m3yc>
    date_of_birth: str # <http://rdf.freebase.com/ns/g.12129y07> <http://rdf.freebase.com/ns/people.person.date_of_birth>        "1954-03-04"^^<http://www.w3.org/2001/XMLSchema#date>

    tracks = [] # <http://rdf.freebase.com/ns/music.artist.track> (v strede), vpravo je potom ID
    albums = [] # <http://rdf.freebase.com/ns/music.artist.album> (v strede), vpravo je potom ID
    track_contributions = [] #<http://rdf.freebase.com/ns/g.112yfxf28>  <http://rdf.freebase.com/ns/music.artist.track_contributions>   <http://rdf.freebase.com/ns/m.01103pc7>
    award_nominations = [] #<http://rdf.freebase.com/ns/g.11b6dv1czb>       <http://rdf.freebase.com/ns/award.award_nominee.award_nominations>     <http://rdf.freebase.com/ns/m.0_q_xky>
    awards_won = [] # <http://rdf.freebase.com/ns/m.029dy9>	<http://rdf.freebase.com/ns/award.award_winner.awards_won>	<http://rdf.freebase.com/ns/m.0_r27zk>	.

    # music_group_members = [] # <http://rdf.freebase.com/ns/g.11b6dv1czb>       <http://rdf.freebase.com/ns/music.musical_group.member> <http://rdf.freebase.com/ns/m.0_q__qv>

    # is_person: bool = False # <http://rdf.freebase.com/ns/type.object.type>   <http://rdf.freebase.com/ns/people.person>
    # is_music_group: bool = False # <http://rdf.freebase.com/ns/g.11b6dv1czb>       <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>       <http://rdf.freebase.com/ns/music.musical_group>
    # is_music_writer: bool = False # <http://rdf.freebase.com/ns/g.12129y07> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>       <http://rdf.freebase.com/ns/music.writer>
    # is_music_composer: bool = False # <http://rdf.freebase.com/ns/g.12129y07> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>       <http://rdf.freebase.com/ns/music.composer>

    def __init__(self, id):
        self.id = id
        self.tracks = []
        self.albums = []
        self.track_contributions = []
        self.award_nominations = []
        self.music_group_members = []

class AwardNomination:
    id: int
    nomination_type: str
    # artist: any

    def __init__(self, id):
        self.id = id

class Award:
    id: int
    name: str
    detail_reference: str # <http://rdf.freebase.com/ns/award.award_honor.award>	<http://rdf.freebase.com/ns/m.0y7pmzv>

    def __init__(self, id: int):
        self.id = id

# <http://rdf.freebase.com/ns/m.029dy9>	<http://rdf.freebase.com/ns/award.award_winner.awards_won>	<http://rdf.freebase.com/ns/m.0_r27zk>	.
# <http://rdf.freebase.com/ns/m.0_r27zk>	<http://rdf.freebase.com/ns/award.award_honor.award>	<http://rdf.freebase.com/ns/m.0y7pmzv>	.
# <http://rdf.freebase.com/ns/m.0y7pmzv>	<http://rdf.freebase.com/ns/type.object.name>	"World Music Award for World’s Best Selling Irish Artist"@en	.

# \<http:\/\/rdf\.freebase\.com\/ns\/m\.0v1_lyv\>

# m\.014brgq

# <http://rdf.freebase.com/ns/m.01czfhb>       <http://rdf.freebase.com/ns/music.artist.track> <http://rdf.freebase.com/ns/g.11b6dv1czb>