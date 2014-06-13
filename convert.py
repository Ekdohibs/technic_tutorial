import sys

def flatten(l):
    u = []
    for j in l:
        for i in j:
            u.append(i)
    return u

def closing_tag(tag):
    u = tag.split("<")[1:]
    u.reverse()
    return "</" + "</".join(u)

def make_paragraph(par):
    # Titles
    if len(par) >= 2 and par[1] == "=" * len(par[0]):
        return "<h1>" + par[0] + "</h1>"
    l = [("<p>", [])]
    for line in par:
        if line[:2] == "- ":
            l.append(("<ul><li>", [line[2:]]))
        else:
            l[-1][1].append(line)

    l2 = []
    for (tag, u) in l:
        l2.append(tag)
        l2.append(" ".join(u))
        l2.append(closing_tag(tag))
    return "".join(l2)

def process_format(l):
    ll = [[]]
    for i in l:
        if i == "":
            ll.append([])
        else:
            ll[-1].append(i)

    return [make_paragraph(par) for par in ll]

replacements = [("<...>", "<b>TODO</b>"),
                ("[[", '<img src="'),
                ("]]", '" width=683 heigth=384>')]
def process_line(line):
    for a, b in replacements:
        line = line.replace(a, b)
    return line

def process_content(l):
    return [process_line(line) for line in l]

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, "r") as f:
    l = f.readlines()

l = [i.strip() for i in l]
l = process_format(l)
l = process_content(l)

with open(outfile, "w") as f:
    f.write("<!DOCTYPE html>\n<html><body>\n")
    for line in l:
        f.write(line)
        f.write("\n")
    f.write("</body></html>\n")

