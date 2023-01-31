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


### 논문
| 구분    | 언어 | 논문명 | 설명 | Open Source |
|:------:|:----:|:------|:---|:-----------|
|1     | Muti | [SIGMORPHON 2020](https://aclanthology.org/2020.sigmorphon-1.2.pdf) | - | [SIGMORPHON](https://github.com/sigmorphon) |
|2     | Muti | [SIGMORPHON 2021](https://aclanthology.org/2021.sigmorphon-1.13.pdf) | - | [SIGMORPHON](https://github.com/sigmorphon) |
|3     | KR | [한국어 발음 변환기(G2P)의 현황과 성능 향상에 대한 언어학적 제안](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002922160) | 한국어 G2P 라이브러리 개선 | [KoG2Padvanced](https://github.com/seongmin-mun/KoG2Padvanced) |
|4     | KR | [Korean speech recognition based on grapheme](https://www.jask.or.kr/articles/xml/bQA1/) | 문자소 기반 | ? |
|5     | KR | [GRAPHEME-TO-PHONEME CONVERSION USING LONG SHORT-TERM MEMORY RECURRENT NEURAL NETWORKS](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7178767) | LSTM-RNN 이용, [Review](https://changjinhan.github.io/paper%20review/LSTM-G2P/) | ? |
|6     | EN | [Massively Multilingual Pronunciation Mining with WikiPron](https://aclanthology.org/2020.lrec-1.521.pdf) | WikiPron 논문 | [wikipron](https://github.com/kylebgorman/wikipron), [wikipron-modeling](https://github.com/CUNY-CL/wikipron-modeling) |
|7     | EN | [Neural Transition-based String Transduction for Limited-Resource Setting in Morphology](https://web.archive.org/web/20200213235925id_/https://www.zora.uzh.ch/id/eprint/162579/1/MakarovClematide2018.pdf) | 2018년 transduction | ? |
|8     | EN | [Transformer based Grapheme-to-Phoneme Conversion](https://arxiv.org/ftp/arxiv/papers/2004/2004.06338.pdf) | Transformer 이용 | [DeepPhonemizer](https://github.com/as-ideas/DeepPhonemizer) |
|9     | EN | [NEURAL GRAPHEME-TO-PHONEME CONVERSION WITH PRE-TRAINED GRAPHEME MODELS](https://arxiv.org/abs/2201.10716) | BERT, BERT-fused 이용 | [GraphemeBERT](https://github.com/ldong1111/GraphemeBERT) |
|10     | EN | [ByT5 model for massively multilingual grapheme-to-phoneme conversion](https://arxiv.org/pdf/2204.03067.pdf) | T5 이용 | [CharsiuG2P](https://github.com/lingjzhu/CharsiuG2P#) |
|11     | EN | [Token-Level Ensemble Distillation for Grapheme-to-Phoneme Conversion](https://arxiv.org/pdf/1904.03446.pdf) | 최근 MS 음성인식 모델에서 사용한 G2P, token-level ensemble distillation  | [g2p_kd](https://github.com/sigmeta/g2p-kd) |

### Datasets
  
  | 언어 | 이름 |설명|
  |:----:|:--------:|:----:|
  | KR | SIGMORPHON 2021 | Subtask 2(midium-resource), 10,000 words|
  |    |ipa-dict         | 62,676 (중복 제거 해야 함)               |
  | EN | SIGMORPHON 2021 | Subtask 1(high-resource), 41,000 words (train/val/test=8:1:1)|
  |    |ipa-dict         | 125,927 (중복 제거 해야 함)              |
  |    |CMUDict          | 125,074 (중복 제거, 대문자->소문자)       |

### Dictionary
  
  1. CMU Pronouncing Dictionary
  2. UniMorph
