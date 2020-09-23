from jishoResult import JishoResult
from lxml import html
import requests

class JishoHelper():

    def __init__(self):
        pass

    def search(self, query: str):
        if query == None or len(query) == 0 or query.isspace():
            raise ValueError(f'query argument is malformed: \"{query}\"')

        print(f'Looking up \"{query}\"...')

        query = query.strip()
        rawResponse = requests.get(f'https://jisho.org/search/{query}')
        htmlTree = html.fromstring(rawResponse.content)

        if htmlTree == None:
            print(f'htmlTree is malformed: {htmlTree}')
            return None

        parentElements = htmlTree.find_class('concept_light-representation')
        if parentElements == None or len(parentElements) != 1:
            print(f'No parent elements')
            return None

        textElements = parentElements[0].find_class('text')
        if textElements == None or len(textElements) != 1:
            print(f'No text elements')
            return None

        word = textElements[0].text_content()
        if word == None or len(word) == 0 or word.isspace():
            print(f'word is malformed: \"{word}\"')
            return None

        word = word.strip()

        definitionElements = htmlTree.find_class('meaning-meaning')
        if definitionElements == None or len(definitionElements) == 0:
            print(f'No definition elements')
            return None

        definitions = list()

        for definitionElement in definitionElements:
            breakUnitElements = definitionElement.find_class('break-unit')
            if breakUnitElements == None or len(breakUnitElements) != 0:
                continue

            definition = definitionElement.text_content()
            if definition == None or len(definition) == 0 or definition.isspace():
                continue

            definitions.append(definition.strip())

        if len(definitions) == 0:
            print(f'Found no definitions')
            return None

        furiganaElement = htmlTree.find_class('kanji-1-up')
        if furiganaElement != None and len(furiganaElement) == 1:
            furigana = furiganaElement[0].text_content()

            if furigana == None or len(furigana) == 0:
                furigana = None
            else:
                furigana = furigana.strip()

        return JishoResult(
            definitions = definitions,
            furigana = furigana,
            word = word
        )
