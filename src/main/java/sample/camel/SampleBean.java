package sample.camel;

import java.util.StringTokenizer;

import org.springframework.stereotype.Component;
import org.apache.camel.Body;
import org.apache.camel.Header;

@Component("sampleBean")
public class SampleBean {

    // -----------------------------------------------------------------
    // Translates a sentence of words into Pig Latin.
    // -----------------------------------------------------------------
    public String translate(@Body String phrase) {
        String result = "";

        String sentence = phrase.toLowerCase();
        StringTokenizer tokenizer = new StringTokenizer(sentence);

        while (tokenizer.hasMoreTokens()) {
            result += translateWord(tokenizer.nextToken());
            result += " ";
        }

        return "{\"translatedPhrase\":\"" + result + "\"}";
    }

    // -----------------------------------------------------------------
    // Translates one word into Pig Latin. If the word begins with a
    // vowel, the suffix "yay" is appended to the word. Otherwise,
    // the first letter or two are moved to the end of the word,
    // and "ay" is appended.
    // -----------------------------------------------------------------
    private String translateWord(String word) {
        String result = "";

        if (beginsWithVowel(word))
            result = word + "yay";
        else if (beginsWithBlend(word))
            result = word.substring(2) + word.substring(0, 2) + "ay";
        else
            result = word.substring(1) + word.charAt(0) + "ay";

        return result;
    }

    // -----------------------------------------------------------------
    // Determines if the specified word begins with a vowel.
    // -----------------------------------------------------------------
    private boolean beginsWithVowel(String word) {
        String vowels = "aeiou";

        char letter = word.charAt(0);

        return (vowels.indexOf(letter) != -1);
    }

    // -----------------------------------------------------------------
    // Determines if the specified word begins with a particular
    // two-character consonant blend.
    // -----------------------------------------------------------------
    private boolean beginsWithBlend(String word) {
        return (word.startsWith("bl") || word.startsWith("sc") || word.startsWith("br") || word.startsWith("sh")
                || word.startsWith("ch") || word.startsWith("sk") || word.startsWith("cl") || word.startsWith("sl")
                || word.startsWith("cr") || word.startsWith("sn") || word.startsWith("dr") || word.startsWith("sm")
                || word.startsWith("dw") || word.startsWith("sp") || word.startsWith("fl") || word.startsWith("sq")
                || word.startsWith("fr") || word.startsWith("st") || word.startsWith("gl") || word.startsWith("sw")
                || word.startsWith("gr") || word.startsWith("th") || word.startsWith("kl") || word.startsWith("tr")
                || word.startsWith("ph") || word.startsWith("tw") || word.startsWith("pl") || word.startsWith("wh")
                || word.startsWith("pr") || word.startsWith("wr"));
    }

}
