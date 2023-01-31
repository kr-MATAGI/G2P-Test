from DeepPhonemizer.dp.phonemizer import Phonemizer

### Main ###
if __name__ == '__main__':
    phonemizer = Phonemizer.from_checkpoint('DeepPhonemizer/en_us_cmudict_ipa_forward.pt')
    print(phonemizer('abe', lang='en_us'))