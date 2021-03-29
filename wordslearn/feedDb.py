from wordslearn.models import WordEng
from wordslearn.models import WordPol

import feedData

WordEng.objects.all().delete()
WordPol.objects.all().delete()

feedData.main()