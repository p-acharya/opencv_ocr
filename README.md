# Kannada-English dictionary OCR 

I have a pdf of an excellent Kannada-English etymological dictionary, a gem to any linguist or student studying Kannada. Unfortunately, the pdf is corrupted and therefore cannot be searched. For an Indian American trying to improve my Kannada in the year 2020, this was unacceptable! What good is an unsearchable dictionary? Surely, I couldn't be expected to scroll to the letter everytime I wanted to find a word! And thus, this project to OCR the entire dictionary was born! 



<figure align="left">
   <img src="demo/pg64_excerpt.png" width="45%" height="80%"/> 
    <figcaption> <i>An excerpt page from the dictionary (Upper left region of pg. 188)</i> </figcaption>
</figure> 


### Challenges

At first, I tried to reconstruct the corrupted font table but quickly saw this was infeasible (if a pdf has multiple fonts, like this 1200 page pdf does, means you have to reconstruct the font table for potentially hundereds of fonts, made even more difficult by the prescence of Latin, extended Latin, and Kannada characters). 


My next best bet was OCR'ing the dictionary. And while this may sound like a trivial and easy task when the document only has one script on it, mixed language text recognition is a whole other beast altogether! 
As an example, let's look at a single dictionary entry:

<img src="demo/all.png" width="70%" height="60%">

Here we see there is adjacent Kannada (U+0C80-U+0CFF), Kannada Transliteration (ISO 15919), IPA (International Phonetic Alphabet - uses many different unicode blocks), and  English text (Basic Latin). That's four different adjacent scripts in one dictionary entry! This is truly a difficult problem to solve.

### Approach

I decided to use Google Vision to ocr, as it is probably the most state of the art mixed language text recognition at this point, and works even for languages often neglected in OCR (such as Kannada). 

When I tried to OCR the above dictionary entry (ಅನಾಯಕತ್ವ), without providing any language hints, here was the output:
```python
//without language hints
"'o SD o anāyakatva [əne:jakatve] n. [pol.)] 1\nleaderless state, utter lack of leadership 2 chaos,\nan-\narchy [Sk.].\n'"

```
As we can see here, it hyperrecognizes Latin text (which is to be expected). 
Next, I tried providing only Kannada as a language hint:

```python
//with Kannada language hint
"'OJO AJIF3, anāyakatva [ǝne:jəkətve] n. (pol.) 1\nleaderless state, utter lack of leadership 2 chaos,\narchy [Sk.]\nan-\n'"
```

Not looking too good, even with the language hint. What could be going wrong for it to fail the Kannada text recognition so miserably? So I tried recognizing a simpler text with just Kannada and English (basic latin), meaning no ipa (or transliteration). 

<figure align="left">
   <img src="demo/alternate_text.PNG" width="50%" height="80%"/> 
    <figcaption> <i>mixed text with Kannada in one column and English in the other</i> </figcaption>
</figure> 

I tried the above excerpt with Kannada language hint added (no language hint failed miserably), and the results are reproduced below (I just added in the columnar formatting for easier reading).

| Left (Kannada) | Right (text) |
| ------------- | ------------- |
|ಮನೋಜ್ : ನೀವು ಬೆಳಿಗ್ಗೆ ಎಷ್ಟು | At what time do you get up in the  |
| ಗಂಟೆಗೆ ಏಳೀರಿ ?  | morning ?  |
|ಮೋಹನ್ : ಆರು ಗಂಟೆಗೆ ಏಳೀನಿ. | I get up at six o'clock.  |
| ಮನೋಜ್ : ಎದ್ದು ಏನು ಮಾಡ್ತೀರಿ ?  | After getting up, what do you do?  |
|ಮೋಹನ್ : ಎದ್ದು ವಾಕಿಂಗ್| I go for a walk. After the walk, I  |
| ಹೋಗ್ತಿನಿ. ವಾಕಿಂಗ್ | brush my teeth and I drink coffee. |
|ಹೋಗಿ ಬಂದು ಹಲ್ಲು| |
| ಉಜ್ಜಿಕೊಳ್ಳಿನಿ. ಹಲ್ಲು ||
|ಉಜ್ಜಿ ಕೊಂಡು ಕಾಫಿ| |
| ಕುಡೀತೀನಿ.| |

So it works quite well without the IPA! It must that which is screwing up my recognition!
Fortunately for me, all the IPA text in the dictionary is contained within brackets (bracket notation is used to represent narrow transcription in Phonetics). Which means that a simple regex expression can be used to remove the IPA text for each dictionary entry.

<figure align="left">
   <img src="demo/removed_ipa.png" width="50%" height="80%"/> 
    <figcaption> <i>The same entry with the IPA text removed</i> </figcaption>
</figure> 

After OCR'ing the above image (with Kannada language hint):

```python
"n.\n೧ಅನಾಯಕತ್ವ anayakatva\n(pol.) 1\nleaderless state, utter lack of leadership 2 chaos,\narchy [Sk.]\nan-\n"
```

The Kannada transliteration is not as much of a problem due to the relatively limited number of accented latin characters used in the Kannada Transliteration Standard. And if the Kannada text is read correctly, then the Transliteration can simply be generated from that. 

But not all challenges are out of the way yet:

<figure>
   <img src="demo/pg191_excerpt.png" width="50%" height="80%"/> 
</figure> 

Because this is an etymological dictionary, it contains words from old Kannada, which includes letters that are no longer used in the modern Kannada alphabet. From wikipedia, 

> Kannada literary works employed the letters ಱ (transliterated 'ṟ' or 'rh') and ೞ (transliterated 'ḻ', 'lh' or 'zh'), whose manner of articulation most plausibly could be   > akin to those in present-day Malayalam and Tamil. The letters dropped out of use in the 12th and 18th centuries, respectively. Later Kannada works replaced 'rh' and 'lh' with > ರ (ra) and ಳ (la) respectively.[13]

Since google vision presumambly is trained on data from modern Kannada, it cannot recognize ಱ or ೞ! 
When I tried the above excerpt, words where the second letter is ೞ, GCP failed miserably. 

```python
"wego\n?weg 3 erata\n? ಎಬಿವು' eravu\nn. [move) pulling (C. (Kitt.)) [Ka.\nD504(a)]\nn. (move] 1 pulling, dragging\n2 spasm, cramp (My. (Kitt.)) [Ka. D504(a)].\n•ಎಬಿವು' eravu\n283) vt. (move] 1 to rub;\nto rub off or out; to smear gently 2 to stroke gently\n[Ka. D505].\n"
```
Obviously something for google to improve on! 
But for now, I have decided to try and use Tesseract to train a neaural net to recognize the IPA and Obsolete Kannada letters. This page will be updated as I go along. 
