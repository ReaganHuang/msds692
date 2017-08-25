import graphviz

def listviz(elems, showassoc=True):
    s = """
    digraph G {
        nodesep=.05;
        node [shape=record,width=.1,height=.1];
    """
    if type(elems)==dict:
        elems = elems.items()
    labels = []
    for i in range(len(elems)):
        el = elems[i]
        if not el:
            labels.append(str(i))
        else:
            labels.append(idx_elviz(i,el,showassoc))
    s += '    mainlist [space="0.0", margin="0.01", fontcolor="#444443", fontname="Helvetica", label=<'+'|'.join(labels)+'>];\n'

    s += "}\n"
    print s
    return graphviz.Source(s)


def lolviz(table, showassoc=True):
    """
    Given a list of lists such as:

      [ [('a','3')], [], [('b',230), ('c',21)] ]

    return the dot/graphviz to display as a two-dimensional
    structure.

    If showassoc, display 2-tuples (x,y) as x->y.
    """
    def islol(table):
        for x in table:
            if type(x)==list or type(x)==tuple:
                return True
        return False

    s = """
    digraph G {
        nodesep=.05;
        rankdir=LR;
        node [shape=record,width=.1,height=.1];
    """
    # Make outer list as vertical
    labels = []
    for i in range(len(table)):
        bucket = table[i]
        if (type(bucket)==list or type(bucket)==tuple) and len(bucket) == 0:
            labels.append(str(i))
        else:
            labels.append("<f%d> %d" % (i, i))

    s += '    mainlist [color="#444443", fontsize="9", fontcolor="#444443", fontname="Helvetica", style=filled, fillcolor="#D9E6F5", label = "'+'|'.join(labels)+'"];\n'

    # define inner lists
    for i in range(len(table)):
        bucket = table[i]
        if not bucket or ((type(bucket)==list or type(bucket)==tuple) and len(bucket)==0):
            continue
        elements = []
        if type(bucket)==list or type(bucket)==tuple:
            for j, el in enumerate(bucket):
                elements.append(idx_elviz(j, el, showassoc))
        else:
            elements.append(elviz(bucket, showassoc))
        s += 'node%d [color="#444443", fontname="Helvetica", margin="0.01", space="0.0", shape=record label=<{%s}>];\n' % (i, '|'.join(elements))

    # Do edges
    for i in range(len(table)):
        bucket = table[i]
        if not bucket or ((type(bucket)==list or type(bucket)==tuple) and len(bucket)==0):
            continue
        s += 'mainlist:f%d -> node%d [arrowsize=.5]\n' % (i,i)
    s += "}\n"
    # print s
    return graphviz.Source(s)


def elviz(el, showassoc):
    if showassoc and type(el) == tuple and len(el) == 2:
        els = "%s&rarr;%s" % el
    else:
        els = str(el)
    els = els.replace('{', '&#123;')
    els = els.replace('}', '&#125;')
    return els


def idx_elviz(idx, el, showassoc):
    return \
        """
        <table BORDER="0" CELLBORDER="1" CELLSPACING="0">
          <tr>
            <td cellspacing="0" bgcolor="#FBFEB0" border="1" sides="b" valign="top">
              <font color="#444443" point-size="9">%d</font>
            </td>
          </tr>
          <tr>
            <td bgcolor="#FBFEB0" border="0" align="center">
              <font point-size="11">%s</font>
            </td>
          </tr>
        </table>
        """ % (idx, elviz(el,showassoc))

x = [ [('a','3')], [], [('b',230), ('c',21)] ]
x = [('the',4), ('cat',1), ('sat',1), ('hat',1)]
x = [('a',4),[2],"hi",99]
x = {'the':4, 'hi':4}
x = ["hi",'mom']
dot = listviz(x, showassoc=True)
dot.render(view=True)