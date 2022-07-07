import MeCab
import unidic

tagger = MeCab.Tagger("")  # 「tagger = MeCab.Tagger('-d ' + unidic.DICDIR)」
sample_txt = 'こんにちは、おはよう。あれ、今何をしようとしてたっけ？'
result = tagger.parse(sample_txt)
print(result)