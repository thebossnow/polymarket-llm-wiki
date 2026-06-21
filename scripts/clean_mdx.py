#!/usr/bin/env python3
"""Strip Mintlify MDX/JSX components from the docs mirror, leaving plain Markdown.

The pages fetched from Mintlify's `.md` endpoints embed React/MDX components
(<ResponseField>, <Card>, <Note>, <Steps>, <Tabs>, <CodeGroup>, the JSX landing
page in index.md, ...). Those render on the docs site but are noise for an LLM
knowledge base. This converts them to plain Markdown equivalents.

Fenced code blocks are protected: angle-bracket TypeScript generics such as
`Promise<OrderResponse>` live in code and must never be rewritten.

Usage: clean_mdx.py FILE [FILE ...]   (edits files in place)
"""
import re
import sys


def attr(attrs: str, name: str) -> str:
    m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', attrs)
    if m:
        return m.group(1)
    m = re.search(rf"\b{name}\s*=\s*'([^']*)'", attrs)
    return m.group(1) if m else ""


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# ---- code-block protection ---------------------------------------------------

def split_segments(text):
    """Yield (is_code, segment_text), splitting on ``` fences."""
    segments, buf, in_code = [], [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            buf.append(line)
            if in_code:                       # closing fence
                segments.append((True, "\n".join(buf)))
                buf, in_code = [], False
            else:                             # opening fence
                segments.append((False, "\n".join(buf[:-1])))
                buf, in_code = [line], True
            continue
        buf.append(line)
    segments.append((in_code, "\n".join(buf)))
    return segments


def process_code(block: str) -> str:
    lines = block.split("\n")
    indent = len(lines[0]) - len(lines[0].lstrip())
    if indent:                                # dedent JSX-embedded code blocks
        lines = [l[indent:] if l[:indent].strip() == "" else l.lstrip()
                 for l in lines]
    lines[0] = lines[0].replace(" theme={null}", "").replace("theme={null}", "")
    return "\n".join(lines)


# ---- component conversions (run only on non-code text) -----------------------

def blockquote(label: str, inner: str) -> str:
    body = collapse_ws(strip_tags(inner))
    return f"> **{label}:** {body}" if body else f"> **{label}**"


def img_repl(m):
    a = m.group(1)
    if "hidden dark:block" in a:              # drop dark-mode duplicate image
        return ""
    alt, src = attr(a, "alt"), attr(a, "src")
    return f"![{alt}]({src})" if alt and src else ""   # drop decorative images


def a_repl(m):
    href = attr(m.group(1), "href")
    text = collapse_ws(strip_tags(m.group(2)))
    if href and text:
        return f"[{text}]({href})"
    return text


def card_link(attrs: str) -> str:
    title, href = attr(attrs, "title"), attr(attrs, "href")
    return f"[{title}]({href})" if href and title else (title or "")


def field_open(m):
    a = m.group(1)
    name = (attr(a, "name") or attr(a, "path") or attr(a, "query")
            or attr(a, "body"))
    typ = attr(a, "type")
    parts = []
    if name:
        parts.append(f"**`{name}`**")
    if typ:
        parts.append(f"`{typ}`")
    line = " ".join(parts)
    if re.search(r"\brequired\b", a):
        line += " *(required)*"
    default = attr(a, "default")
    if default:
        line += f" — default `{default}`"
    return line


def transform_mdx(t: str) -> str:
    # JSX component definitions (e.g. `export const IconCard = (...) => {...};`)
    t = re.sub(r"(?ms)^export const \w+\s*=.*?^\};\s*$\n?", "", t)

    # <IconCard ... /> and <Card ... /> self-closing
    t = re.sub(
        r"<IconCard\b([^>]*?)/>",
        lambda m: f"- **{card_link(m.group(1))}**"
        + (f" — {attr(m.group(1), 'description')}"
           if attr(m.group(1), "description") else ""),
        t,
    )
    # <Card ...>desc</Card>
    t = re.sub(
        r"(?s)<Card\b([^>]*)>(.*?)</Card>",
        lambda m: f"- **{card_link(m.group(1))}**"
        + (f" — {collapse_ws(strip_tags(m.group(2)))}"
           if collapse_ws(strip_tags(m.group(2))) else ""),
        t,
    )
    t = re.sub(r"<Card\b([^>]*?)/>",
               lambda m: f"- **{card_link(m.group(1))}**", t)

    # <ResponseField>/<ParamField> -> bold name + type, keep inner content
    t = re.sub(r"<(?:ResponseField|ParamField)\b([^>]*)>", field_open, t)
    t = re.sub(r"</(?:ResponseField|ParamField)>", "", t)

    # Callouts
    for tag, label in [("Note", "Note"), ("Info", "Info"), ("Tip", "Tip"),
                       ("Warning", "Warning"), ("Check", "Check"),
                       ("Danger", "Warning")]:
        t = re.sub(rf"(?s)<{tag}\b[^>]*>(.*?)</{tag}>",
                   lambda m, l=label: blockquote(l, m.group(1)), t)

    # Titled wrappers
    t = re.sub(r"<Step\b([^>]*)>",
               lambda m: f"### {attr(m.group(1), 'title')}"
               if attr(m.group(1), "title") else "", t)
    t = re.sub(r"<(?:Accordion|Expandable)\b([^>]*)>",
               lambda m: f"#### {attr(m.group(1), 'title')}"
               if attr(m.group(1), "title") else "", t)
    t = re.sub(r"<Tab\b([^>]*)>",
               lambda m: f"**{attr(m.group(1), 'title')}**"
               if attr(m.group(1), "title") else "", t)
    t = re.sub(r"</(?:Step|Accordion|Expandable|Tab)>", "", t)

    # Images (inside <Frame> or standalone)
    t = re.sub(r"(?s)<img\b([^>]*?)/?>", img_repl, t)

    # Headings written as HTML (JSX landing page)
    for lvl, tag in [(1, "h1"), (2, "h2"), (3, "h3"), (4, "h4")]:
        t = re.sub(rf"(?s)<{tag}\b[^>]*>(.*?)</{tag}>",
                   lambda m, p="#" * lvl: f"{p} {collapse_ws(strip_tags(m.group(1)))}",
                   t)

    # Anchors -> markdown links
    t = re.sub(r"(?s)<a\b([^>]*)>(.*?)</a>", a_repl, t)

    # Drop inline SVG
    t = re.sub(r"(?s)<svg\b.*?</svg>", "", t)

    # <iframe> embeds -> link to the source (or drop if none)
    t = re.sub(
        r"<iframe\b([^>]*?)/?>(?:\s*</iframe>)?",
        lambda m: (f"[{attr(m.group(1), 'title') or 'Embedded chart'}]"
                   f"({attr(m.group(1), 'src')})")
        if attr(m.group(1), "src") else "",
        t,
    )

    # Unwrap structural wrappers (keep their contents)
    wrappers = ("CardGroup|CodeGroup|Tabs|Steps|AccordionGroup|Columns|Column|"
                "Frame|RequestExample|ResponseExample|div|span|section|"
                "p|ul|li|br|Icon|img")
    t = re.sub(rf"</?(?:{wrappers})\b[^>]*/?>", "", t)

    # Drop leading indentation left behind by unwrapped JSX/MDX containers.
    # (4+ spaces would otherwise be parsed as a Markdown code block.)
    t = "\n".join(l.lstrip() if l.strip() else "" for l in t.split("\n"))

    return t


def clean(text: str) -> str:
    out = []
    for is_code, seg in split_segments(text):
        out.append(process_code(seg) if is_code else transform_mdx(seg))
    text = "\n".join(out)
    text = re.sub(r"[ \t]+\n", "\n", text)        # trailing whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)        # collapse blank runs
    return text.strip("\n") + "\n"


def main(argv):
    for path in argv:
        with open(path, encoding="utf-8") as f:
            original = f.read()
        cleaned = clean(original)
        if cleaned != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"cleaned {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
