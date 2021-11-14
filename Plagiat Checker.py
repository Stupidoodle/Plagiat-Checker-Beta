import nltk
import pypandoc
from googlesearch import search
import sys as sus
import re
import mechanize
from html2text import html2text
from fuzzywuzzy import fuzz

def clean_html(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.

    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def main():   
    parameter = str(sus.argv[1]);

    #Check if it is a docx file

    output = pypandoc.convert_file(parameter, "plain", outputfile="temp.txt");
    assert output == ""

    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle");
    fp = open("temp.txt");
    data = fp.read();
    full_text = tokenizer.tokenize(data);

    new_full_text = [];

    for i in full_text:
        new_full_text.append(i.replace("\n", ""));

    for i in new_full_text:
        print(i);

    for query in new_full_text:
        print("\n---------");
        print(query);
        print("---------");
        for i in search(query, tld="com", num=10, stop=10, pause=2):
            print("Looking on page: " + i + " For the given term\n");
            url = i;
            br = mechanize.Browser();
            br.set_handle_robots(False);
            br.addheaders = [("User-agent", "Firefox")];
            html = br.open(url).read().decode("utf-8");
            cleanhtml = clean_html(html);
            text = html2text(cleanhtml);
            #print(text)
            split_text = tokenizer.tokenize(text);
            new_split_text = [];

            for i in split_text:
                new_split_text.append(i.replace("\n", ""));

            for i in new_split_text:
                print(str(fuzz.ratio(query.lower(), i)) + " : " + i);
            


if __name__ == '__main__':
    main()