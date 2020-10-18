
ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
TRACK_CONTRIBUTION = 'track_contribution'
RECORDING = 'recording'
AWARD = 'award'
AWARD_HONOR = 'award_honor'
GENRE = 'genre'

AWARD_INFO_TYPE_AWARD = 'award'
AWARD_INFO_TYPE_AWARD_WON = 'award_won'
AWARD_INFO_TYPE_HONOR = 'award_honor'

INITIAL_PARSING = 'initial_parsing'
SECONDARY_PARSING = 'secondary_parsing'
TERTIARY_PARSING = 'tertiary_parsing'

STATE = [INITIAL_PARSING, SECONDARY_PARSING, TERTIARY_PARSING]

OUTPUT_FILE = 'output'

GENRE_MAPPER = {
    "/music/artist/genre": ARTIST,
    "/music/album/genre": ALBUM
}
