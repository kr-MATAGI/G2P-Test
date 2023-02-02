# G2P-Test
G2P-Test

### 참조 Repo

  1. [G2P 관련자료 모음](https://github.com/lifefeel/Grapheme-to-Phoneme)
  2. [SMART-G2P](https://github.com/SMART-TTS/SMART-G2P?fbclid=IwAR2EyuFnFOekhGn_LmVn8kW-QytRMRfwTVCq9pMQquF9ggQLDPvYxZRiwdM)
  3. [PORORO](https://github.com/kakaobrain/pororo)
  4. [KoG2Padvanced](https://github.com/seongmin-mun/KoG2Padvanced)
  5. [sigmorphon](https://github.com/sigmorphon/2021-task1)
  6. [g2pk](https://github.com/Kyubyong/g2pK)
  7. [phonemizer](https://github.com/bootphon/phonemizer)
  8. [DeepPhonemizer](https://github.com/as-ideas/DeepPhonemizer)
  9. [KoG2P](https://github.com/scarletcho/KoG2P)
  10. [G2PE](https://github.com/Kyubyong/g2p)
  11. [G2P-seq2seq](https://github.com/cmusphinx/g2p-seq2seq)
  12. [Zeroth](https://github.com/goodatlas/zeroth)
  13. [kospeech](https://github.com/sooftware/kospeech)
  
  * [IPA-to-Kr](https://ko.wiktionary.org/wiki/%EC%9C%84%ED%82%A4%EB%82%B1%EB%A7%90%EC%82%AC%EC%A0%84:%EA%B5%AD%EC%A0%9C_%EC%9D%8C%EC%84%B1_%EA%B8%B0%ED%98%B8)
  


### 논문
| 구분    | 언어 | 논문명 | 설명 | Open Source |
|:------:|:----:|:------|:---|:-----------|
|1     | Muti | [SIGMORPHON 2020](https://aclanthology.org/2020.sigmorphon-1.2.pdf) | - | [SIGMORPHON](https://github.com/sigmorphon) |
|2     | Muti | [SIGMORPHON 2021](https://aclanthology.org/2021.sigmorphon-1.13.pdf) | - | [SIGMORPHON](https://github.com/sigmorphon) |
|3     | KR | [한국어 발음 변환기(G2P)의 현황과 성능 향상에 대한 언어학적 제안](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002922160) | 한국어 G2P 라이브러리 개선 | [KoG2Padvanced](https://github.com/seongmin-mun/KoG2Padvanced) |
|5     | EN | [GRAPHEME-TO-PHONEME CONVERSION USING LONG SHORT-TERM MEMORY RECURRENT NEURAL NETWORKS](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7178767) | LSTM-RNN 이용, [Review](https://changjinhan.github.io/paper%20review/LSTM-G2P/) | ? |
|6     | EN | [Massively Multilingual Pronunciation Mining with WikiPron](https://aclanthology.org/2020.lrec-1.521.pdf) | WikiPron 논문 | [wikipron](https://github.com/kylebgorman/wikipron), [wikipron-modeling](https://github.com/CUNY-CL/wikipron-modeling) |
|7     | EN | [Neural Transition-based String Transduction for Limited-Resource Setting in Morphology](https://web.archive.org/web/20200213235925id_/https://www.zora.uzh.ch/id/eprint/162579/1/MakarovClematide2018.pdf) | 2018년 transduction | ? |
|8     | EN | [Transformer based Grapheme-to-Phoneme Conversion](https://arxiv.org/ftp/arxiv/papers/2004/2004.06338.pdf) | Transformer 이용 | [DeepPhonemizer](https://github.com/as-ideas/DeepPhonemizer) |
|9     | EN | [NEURAL GRAPHEME-TO-PHONEME CONVERSION WITH PRE-TRAINED GRAPHEME MODELS](https://arxiv.org/abs/2201.10716) | BERT, BERT-fused 이용 | [GraphemeBERT](https://github.com/ldong1111/GraphemeBERT) |
|10     | EN | [ByT5 model for massively multilingual grapheme-to-phoneme conversion](https://arxiv.org/pdf/2204.03067.pdf) | T5 이용 | [CharsiuG2P](https://github.com/lingjzhu/CharsiuG2P#) |
|11     | EN | [Token-Level Ensemble Distillation for Grapheme-to-Phoneme Conversion](https://arxiv.org/pdf/1904.03446.pdf) | 최근 MS 음성인식 모델에서 사용한 G2P, token-level ensemble distillation  | [g2p_kd](https://github.com/sigmeta/g2p-kd) |

### Datasets
  
  | 언어 | 이름 |설명|총|
  |:----:|:--------:|:----:|:----:|
  | KR | SIGMORPHON 2021 | Subtask 2(midium-resource), 10,000 words (train:8,000/ val: 1,000/ test: 1,000)|16,714|
  |    |CMUDict         |   6,714        |
  | EN | SIGMORPHON 2021 | Subtask 1(high-resource), 41,000 words (train: 33,344/ val:4,168/ test:4,168)|143,405|
  |    |CMUDict          | 102,405       |
  
### Eval
#### - Kr
|                                                          model                                                           |                      dataset                      |  WER  |  PER  |
|:------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------:|:-----:|:-----:|
|                               [CLUZH-4](https://aclanthology.org/2021.sigmorphon-1.17.pdf)                               |                  SIGMORPHON 2021                  | 16.2  |   -   |
|                                 [GBERT attention](https://arxiv.org/pdf/2201.10716.pdf)                                  |                  SIGMORPHON 2021                  | 17.94 | 3.16  |
| [SMART-G2p](https://github.com/SMART-TTS/SMART-G2P?fbclid=IwAR2EyuFnFOekhGn_LmVn8kW-QytRMRfwTVCq9pMQquF9ggQLDPvYxZRiwdM) |                  SIGMORPHON 2021                  |  24   | 4.64  |
|                             [KoG2Padvanced]( https://github.com/seongmin-mun/KoG2Padvanced)                              |                  SIGMORPHON 2021                  | 22.5  | 3.91  |
|                                       [KoG2P](https://github.com/scarletcho/KoG2P)                                       |                  SIGMORPHON 2021                  | 35.2  | 6.75s |
|                                         [g2pk](https://github.com/Kyubyong/g2pK)                                         |                  SIGMORPHON 2021                  |  4.7  | 0.74  |
|                                       [T5](https://github.com/lingjzhu/CharsiuG2P)                                       |            SIGMORPHON 2020 + ipa-dict             |   ?   |   ?   |

#### - En
| model | dataset | WER | PER|
|:----:|:----:|:----:|:----:|
| [Duakoad-1](https://aclanthology.org/2021.sigmorphon-1.16v2.pdf) | SIGMORPHON 2021 | 37.43 | - |
| [Transformer + Bi-LSTM + CNN](https://arxiv.org/pdf/1904.03446.pdf) | CMUDict + their internal dataset | 19.88 | 4.6 |
| [Transformer](https://arxiv.org/ftp/arxiv/papers/2004/2004.06338.pdf) | CMUDict | 22.1 | 5.23 |
| [g2p-seq2seq](https://github.com/cmusphinx/g2p-seq2seq) | CMUDict | 30.2 | - |
| [T5](https://github.com/lingjzhu/CharsiuG2P) | [ipa-dict](https://github.com/lingjzhu/CharsiuG2P/tree/main/data) + wikipron | 25.9 | 8.8 |
| [G2pE](https://github.com/Kyubyong/g2p) | CMUDict | ? | ? |
| [DeepPhonemizer](https://github.com/as-ideas/DeepPhonemizer) | CMUDict, wikipron | ? | ? |

### Dictionary
  
  1. CMU Pronouncing Dictionary
  2. UniMorph
  
### IPA->한글 발음열
#### - 자음

| 발음 |ㄱ|ㄴ|ㄷ|ㄹ|ㅁ|ㅂ|ㅅ|ㅇ|ㅈ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ|ㄲ|ㄸ|ㅃ|ㅆ|ㅉ|
|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
|IPA|ɡ, k̚, k|n, ɲ|d|ɭ, ɾ, ʎ|m|b, p̚, p|sʰ, ɕʰ, ʃʰ|ŋ|t͡ɕ͈, t͡ɕ, d͡ʑ|t͡ɕʰ|kx, kʰ|tʰ|pʰ|h, ɦ, β, ɸʷ, ɸ, x, ʝ, ɣ|k͈|t͈|p͈|s͈, ɕ͈|t͡ɕ͈|

#### - 모음

| 발음|ㅏ|ㅑ|ㅓ|ㅕ|ㅗ|ㅛ|ㅜ|ㅠ|ㅡ|ㅣ|ㅐ|ㅒ|ㅘ|ㅙ|ㅢ|ㅔ|ㅖ|ㅝ|ㅟ|ㅚ, ㅞ|
|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
|IPA|a̠|ja̠|ʌ̹, ɘ|jɘ, jʌ̹|o̞|jo ,o|u|ju|ɯ|i|ɛ|jɛ̝, jɛ|wa̠|wɛ|ɰi|e̞|je̞|wʌ̹, wɘ|ɥi|we̞|

