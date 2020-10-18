# ARTIST
# Matching patterns
# PATTERN_ARTIST = r'\<.*\>\s+(\<.*ns#type\>|\<.*type\.object\.type\>)\s+\<.*ns\/music\.artist\>'
PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ARTIST_TRACK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track\>\t+\<.*\>'
PATTERN_ARTIST_TRACK_CONTRIBUTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track_contributions\>\t+\<.*\>'
PATTERN_ARTIST_ALBUM = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.album\>\t+\<.*\>'
PATTERN_ARTIST_ACTIVE_START = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>.*'
PATTERN_ARTIST_ACTIVE_END = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>.*'
PATTERN_ARTIST_ORIGIN = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.origin\>\t+\<.*\>'
PATTERN_ARTIST_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.genre\>\t+\<.*\>'
PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>.*'
PATTERN_ARTIST_AWARD_NOMINATION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominee\.award_nominations\>.*'
PATTERN_ARTIST_AWARDS_WON = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_winner\.awards_won\>.*'
# Value retrieval patterns
PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE = r'(?<!not )((?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t\")|(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t\"))([0-9-]*)'
PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t\")([0-9-]*)'


# ALBUM
# Matching patterns
PATTERN_ALBUM = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.album\>|\<.*music\.album.*\>\s+\<.*\>)'
PATTERN_ALBUM_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.artist\>\t+\<.*\>'
PATTERN_ALBUM_RELEASE_DATE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.release_date\>.*'
# Value retrieval patterns
PATTERN_RETRIEVE_ALBUM_RELEASE_DATE = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.release_date\>\t\")([0-9-]*)'


# AWARD
# Matching patterns
PATTERN_AWARD_HONOR_AWARD = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award\>\t+\<.*\>'
PATTERN_AWARD_HONOR_AWARD_WINNER = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award_winner\>\t+\<.*\>'

# RECORDING
# Matching patterns
PATTERN_RECORDING = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.recording\>|\<.*music\.recording.*\>\s+\<.*\>)'
PATTERN_RECORDING_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.artist\>\t+\<.*\>'
PATTERN_RECORDING_LENGTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.length\>\t+\<.*\>'
# Value retrieval patterns
PATTERN_RETRIEVE_RECORDING_LENGTH = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.length\>\t\")([0-9]*)'

# GENRE
# Matching patterns
PATTERN_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.predicate\>\t+\"\/music\/(artist|album)\/genre\"'
PATTERN_GENRE_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.display_name\>\t+\".*\"@en'
# Value retrieval patterns
PATTERN_RETRIEVE_GENRE = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.predicate\>\t\")([^"]*)'
PATTERN_RETRIEVE_GENRE_NAME = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.display_name\>\t\")([^"]*)'


# GENERAL
# Matching patterns
PATTERN_OBJECT_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t+\".*\"@en'
PATTERN_OBJECT_DESCRIPTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t+\".*\"@en'
PATTERN_AWARD_NOMINATED_WORK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominated_work\.award_nominations\>.*'

# Value retrieval patterns
PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)\>\t\<'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'

PATTERN_RETRIEVE_OBJECT_NAME = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t\")([^"]*)'
PATTERN_RETRIEVE_OBJECT_DESCRIPTION = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t\")([^"]*)'

# PATTERN_RETRIEVE_OBJECT_NAME = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t\")([\sa-zA-z]*)'
# PATTERN_RETRIEVE_OBJECT_DESCRIPTION = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t\")([\sa-zA-z]*)'