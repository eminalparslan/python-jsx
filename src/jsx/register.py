import codecs
import traceback
from html.parser import HTMLParser
from typing import Optional, Union


class JSXParser(HTMLParser):
    def __init__(self):
        self.depth = 0
        self.builder = []
        self.start_pos = None
        self.patches = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        if self.depth == 1:
            self.builder = ["f'''"]
            self.start_pos = self.getpos()
        self.builder += [self.get_starttag_text()]
        # print("Encountered a start tag :", tag)
        # if attrs:
        #     print("    With the attributes:  ", attrs)

    def handle_endtag(self, tag):
        self.depth -= 1
        self.builder += [f"</{tag}>"]
        if self.depth == 0:
            self.builder += ["'''"]
            self.patches += [{
                "text": "".join(self.builder),
                "start": self.start_pos,
                "end": (self.getpos()[0], self.getpos()[1] + len(self.builder[-2]))
            }]
        # print("Encountered an end tag  :", tag)

    def handle_data(self, data):
        if self.depth > 0:
            self.builder += [data]
            # print("Encountered some data   :", data)

    def handle_startendtag(self, tag, attrs):
        params = ",".join([f"{attr[0]}='{attr[1]}'" for attr in attrs])
        func = f"{tag}({params})"
        if self.depth == 0:
            # startend tag by itself
            self.patches += [{
                "text": func,
                "start": self.getpos(),
                "end": (self.getpos()[0], self.getpos()[1] + len(self.get_starttag_text()))
            }]
        elif self.depth > 0:
            # startend tag embedded in other tags
            self.builder += ["{" + func + "}"]
        # print("Encountered startend tag:", tag)

def apply_patch(data: str, patches: list[dict[str, Union[str, tuple[int, int]]]]) -> str:
    lines = data.splitlines()
    # reversed since we modify lines as we go
    for patch in reversed(patches):
        sl, el = patch["start"][0] - 1, patch["end"][0] - 1
        sc, ec = patch["start"][1], patch["end"][1]
        lines = lines[:sl] + \
                [lines[sl][:sc] + patch["text"] + lines[el][ec:]] + \
                lines[el+1:]
    return "\n".join(lines)

def preprocessor(data: str) -> str:
    parser = JSXParser()
    parser.feed(data)
    processed = apply_patch(data, parser.patches)
    # print(processed)
    return processed


def decode(data: bytes) -> tuple[str, int]:
    decoded, consumed = codecs.utf_8_decode(data, "strict", True)
    try:
        processed = preprocessor(decoded)
    except Exception:
        traceback.print_exc()
        raise
    return processed, consumed


class Decoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decoder(self, input, errors, final):
        pass

    def decode(self, data, final=False) -> str:
        self.buffer += data

        if self.buffer and final:
            buffer = self.buffer
            self.reset()
            return decode(buffer)[0]

        return ""


def search_function(encoding) -> Optional[codecs.CodecInfo]:
    if encoding == "jsx":
        return codecs.CodecInfo(
            name=encoding,
            encode=codecs.utf_8_encode,
            decode=decode,
            incrementaldecoder=Decoder,
        )


codecs.register(search_function)
