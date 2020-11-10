# ARTIST
PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ARTIST_TRACK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track\>\t+\<.*\/(?P<object_id>[gm].*)\>'
# PATTERN_ARTIST_TRACK_CONTRIBUTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track_contributions\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_ALBUM = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.album\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_ACTIVE_START = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t+\"(?P<date>[0-9-]*)\"'
PATTERN_ARTIST_ACTIVE_END = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t+\"(?P<date>[0-9-]*)\"'
PATTERN_ARTIST_ORIGIN = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.origin\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.genre\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t+\"(?P<date>[0-9-]*)\"'
# PATTERN_ARTIST_AWARD_NOMINATION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominee\.award_nominations\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_AWARDS_WON = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_winner\.awards_won\>\t+\<.*\/(?P<object_id>[gm].*)\>'

# ALBUM
PATTERN_ALBUM = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.album\>|\<.*music\.album.*\>\s+\<.*\>)'
PATTERN_ALBUM_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.artist\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ALBUM_RELEASE_DATE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.release_date\>\t+\"(?P<date>[0-9-]*)\"'


# AWARD
PATTERN_AWARD_HONOR_AWARD = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_AWARD_HONOR_AWARD_WINNER = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award_winner\>\t+\<.*\/(?P<object_id>[gm].*)\>'

# RECORDING
PATTERN_RECORDING = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.recording\>|\<.*music\.recording.*\>\s+\<.*\>)'
PATTERN_RECORDING_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.artist\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_RECORDING_LENGTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.length\>\t+(?P<length>[0-9]*)'

# GENRE
PATTERN_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.predicate\>\t+\"\/music\/(?P<type>artist|album)\/genre\"'
PATTERN_GENRE_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.display_name\>\t+\"(?P<name>.*)\"@en'

# GENERAL
# Matching patterns
PATTERN_OBJECT_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t+\"(?P<name>.*)\"@en'
PATTERN_OBJECT_DESCRIPTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t+\"(?P<description>.*)\"@en'
# PATTERN_AWARD_NOMINATED_WORK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominated_work\.award_nominations\>.*'

# Value retrieval patterns
PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)\>\t\<'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'