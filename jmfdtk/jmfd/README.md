# Modified version of Japanese Moral Foundation Dictionary (J-MFD)
[J-MFD](https://github.com/soramame0518/j-mfd) is a Japanese version of Moral Foundation Dictionary ([MFD](https://moralfoundations.org/)). JMFDTk uses the modified version of J-MFD. The modification was made to optimize for [MeCab](https://taku910.github.io/mecab/) with [IPAdic](https://ja.osdn.net/projects/ipadic/).


## Modifications
### J-MFD has word lists based on Moral Foundation and some of the words consist of their word stem followed by '\*'. Verbs, adjectives and adverbs in Japanese have some forms and a different form is used based on the context. As counting all the forms is a bit of trouble, JMFDTk tokenizes text into base forms and count them. Given what mentioned above, some words in the modified J-MFD are replaced with their base form followed by '\*'.

- 落ち着* -> 落ち着く*
- 思いや* -> 思いやる*
- 優し* -> 優しい*
- 傷つ* -> 傷つく*, 傷つける*
- 苦し* -> 苦しい*
- 滅び* -> 滅びる*
- 滅ぼ* -> 滅ぼす*
- 見捨て* -> 見捨てる*
- 損な* -> 損なう*
- 釣り合*	-> 釣り合う*, 釣り合い*
- 引き離* -> 引き離す*
- 締め出* -> 締め出す*
- 結びつ* -> 結びつける*, 結びつく*
- 裏切* -> 裏切る*
- 正し* -> 正しい*, 正しく*
- 重ん* -> 重んじる*
- 母親らし* -> 母親らしい*
- 侮り -> 侮る
- 気高* -> 気高い*
- 初々し* -> 初々しい*
- あどけな* -> あどけない*
- 真新し* -> 真新しい*
- むかつ* -> むかつく*
- 口汚* -> 口汚い*
- 弱々し* -> 弱々しい*

### '不公' is not a Japanese term and MeCab with IPAdic doesn't tokenize it. Instead, '不公平' and '不公正' are added.
- 不公* -> 不公平*, 不公正*
