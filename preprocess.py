import bs4
from bs4 import BeautifulSoup
import re

def load_html_body(filename: str) -> bs4.element.Tag:
    '''Load a html file, parse it with bs4 and return its body'''
    with open(filename, 'r') as f:
        body = BeautifulSoup(f, "html.parser").find("body")
    return body


def clean_html_body(body: bs4.element.Tag) -> bs4.element.Tag:
    '''Clean a html-body using a set of specific rules'''
    # Remove all spans, including footnotes
    for span in body.findAll("span"):
        span.decompose()

    # Remove all signatures
    for signature in body.findAll("p", attrs={"class": "signature"}):
        signature.decompose()

    # Remaining paragraphs are replaced with their childen
    for p in body.findAll("p"):
        p.replaceWithChildren()

    # Remove pictures
    for img in body.findAll("img"):
        img.decompose()

    # Remove links
    for a in body.findAll("a"):
        a.decompose()

    # Replace italics with children
    for i in body.findAll("i"):
        i.replaceWithChildren()

    # Replace boldface with children
    for b in body.findAll("b"):
        b.replaceWithChildren()

    return body


def find_letter_beginnings(body: bs4.element.Tag) -> [int]:
    '''Find indices where letters begin'''
    # Find h3 tags, as one of them is at the beginning of every letter
    h3_tags = body.find_all("h3")

    # Get text of them, stripping leading whitespaces
    h3_texts = list(map(lambda t: t.contents[0].lstrip(), h3_tags))

    # Filter h3 texts -- we only want numbered headings containing "An" and ending with a dot
    regex = re.compile("[0-9]+\. An .+\.")
    h3_texts = list(filter(regex.match, h3_texts))

    # Find and return all indices of letter beginnings
    body_text = str(body.contents)
    beginnings = [body_text.find(h3_text) for h3_text in h3_texts]
    return beginnings


def find_letter_endings(body: bs4.element.Tag) -> [int]:
    '''Find indices where letters end'''
    body_text = str(body.contents)
    endings = [match.start() for match in re.finditer("<hr", body_text)]
    return (endings)


def extract_letters(body: bs4.element.Tag, beginnings: [int], endings: [int]) -> [str]:
    '''Extract the letters from html-body based on indices'''
    # Note that there are some false-positives in the "endings".
    # However, the beginnings are accurate.
    # We thus now match endings to the beginnings,
    # and extract the letters.
    letters = []
    body_text = str(body.contents)
    for beginning in beginnings:
        matched_ending = min([e for e in endings if e > beginning])
        letters.append(body_text[beginning:matched_ending])
    return letters

def final_cosmetics(letter: str) -> str:
    # Remove first line
    _, j = re.search("</h3>\n", letter).span()
    letter = letter[j:]

    # Remove some very few remaining <h3> tags
    letter = letter.replace("<h3>", "")
    letter = letter.replace("</h3>", "")
    letter = letter.replace("<br/>", "")

    # Remove \n at the end
    i, _ = re.search("\n+$", letter).span()
    letter = letter[:i]

    # Replace \n, \t "," with " "
    letter = letter.replace("\n", " ")
    letter = letter.replace("\t", " ")
    
    return letter

def main() -> None:
    # We write everything to one csv file
    f = open("all_letters.csv", "w")
    
    # 14 chapters we scraped
    for nb_chapter in range(1,14):
        # Extract all beginning indices, ending indices, and contents
        filename = "./raw/"+str(nb_chapter)+".html"
        body = clean_html_body(load_html_body(filename))
        beginnings = find_letter_beginnings(body)
        endings = find_letter_endings(body)
        letters = extract_letters(body, beginnings, endings)

        for letter in letters:
            # Extract first line of every letter containing number and receiver
            first_line = letter[0:letter.find("\n")]

            # Extract letter number from first line
            i, j = re.search("^\d+\.", first_line).span()
            letter_number = int(first_line[i:j-1])

            # Extract writer from first line
            i, j = re.search("(Schiller|Goethe)", first_line).span()
            receiver = first_line[i:j]
            if receiver == "Schiller":
                writer = "Goethe"
            elif receiver == "Goethe":
                writer = "Schiller"
            else:
                writer = "NA"

            # Extract main letter text from letter
            main_text = final_cosmetics(letter)

            # Write to file
            print(">>>>>>>>>> ", letter_number, "\t", writer, "\t", main_text)
            f.write(str(letter_number) + '\t' + writer + '\t' + main_text+'\n')

    f.close()        


if __name__ == "__main__":
    main()
