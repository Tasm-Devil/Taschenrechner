# The MIT License (MIT)
#
# Copyright (c) 2018 Pascal Deneaux <deneaux@mail.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`Taschenrechner.py`
====================================================

Simple calculator made as an example for PyQt4. It uses the power of a
finite state machine to parse every new symbol typed in.

* Author(s): Pascal Deneaux
"""

parse_string = ""
state = 'A'
open_brackets = 0

digits = [chr(x) for x in range(ord('1'), ord('9') + 1)]
operations = ['÷', '×', '+']
alphabet = digits + operations + ['0', '(', ')', ',', '−']

# A dict of string:list of (tuples of (list,string))
fsm_transition_table = {
    # state ,input        , next_state
    'A': [(['('],           'A'),
          (digits,          'B'),
          (['−'],           'C'),
          (['0'],           'D'),
          ],
    'B': [(operations,      'A'),
          (digits + ['0'],  'B'),
          (['−'],           'C'),
          ([','],           'E'),
          ([')'],           'G'),
          ],
    'C': [(['('],           'A'),
          (digits,          'B'),
          (['0'],           'D')
          ],
    'D': [(operations,      'A'),
          (['−'],           'C'),
          ([','],           'E'),
          ([')'],           'G'),
          ],
    'E': [(digits + ['0'],  'F')
          ],
    'F': [(operations,      'A'),
          (['−'],           'C'),
          (digits + ['0'],  'F'),
          ([')'],           'G'),
          ],
    'G': [(operations,      'A'),
          (['−'],           'C'),
          ([')'],           'G'),
          ],
}


def clear_text():
    global parse_string, state, open_brackets
    parse_string = ""
    state = 'A'
    open_brackets = 0
    ui.pTE_display.setPlainText("Eingabe bitte")


def new_symbol(symbol):
    global parse_string, state, alphabet, fsm_transition_table, open_brackets

    if symbol not in alphabet:
        print("Symbol ist nicht Teil des Eingabealphabets: " + symbol + " !")
        return
    if symbol in {')'} and open_brackets < 1:
        print("Eine Klammer bitte immer erst öffnen!")
        return

    # Liste aller möglichen Eingabe-Symbole des aktuellen Zustands
    inputs = [x[0] for x in fsm_transition_table[state]]
    # Liste aller möglichen Zustandsübergänge des aktuellen Zustands
    next_states = [x[1] for x in fsm_transition_table[state]]

    # ist in der Liste 'inputs' einmal das jetzige Eingabe-Symbol vorhanden?
    if True in [symbol in x for x in inputs]:
        if symbol in {'('}:
            open_brackets += 1

        if symbol in {')'}:
            open_brackets -= 1

        # An der Position no in der Liste der Zustandsübergänge des aktuellen
        # Zustands, wurde das aktuelle Eingabe-Symbol gefunden.
        no = [symbol in x for x in inputs].index(True)
        state = next_states[no]
        print("Zustand: " + state)

        parse_string += symbol
        ui.pTE_display.setPlainText(parse_string)
    else:
        print("Das Symbol " + symbol + " ist hier nicht erlaubt!")


def evaluate():
    global parse_string, state, open_brackets
    if parse_string:
        try:
            result = eval(parse_string.replace(",", ".").replace("÷", "/").replace("×", "*").replace("−", "-"))
            parse_string = str(result)
            state = 'G'
            open_brackets = 0
            ui.pTE_display.setPlainText(str(result))
        except ZeroDivisionError:
            clear_text()
            ui.pTE_display.setPlainText("Division durch 0 nicht erlaubt")

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from sys import argv, exit

app = QApplication(argv)
ui = loadUi("form.ui")
ui.pB_ret.clicked.connect(evaluate)
ui.pB_del.clicked.connect(clear_text)
ui.pB_Z0.clicked.connect(lambda: new_symbol("0"))
ui.pB_Z1.clicked.connect(lambda: new_symbol("1"))
ui.pB_Z2.clicked.connect(lambda: new_symbol("2"))
ui.pB_Z3.clicked.connect(lambda: new_symbol("3"))
ui.pB_Z4.clicked.connect(lambda: new_symbol("4"))
ui.pB_Z5.clicked.connect(lambda: new_symbol("5"))
ui.pB_Z6.clicked.connect(lambda: new_symbol("6"))
ui.pB_Z7.clicked.connect(lambda: new_symbol("7"))
ui.pB_Z8.clicked.connect(lambda: new_symbol("8"))
ui.pB_Z9.clicked.connect(lambda: new_symbol("9"))
ui.pB_comma.clicked.connect(lambda: new_symbol(","))
ui.pB_div.clicked.connect(lambda: new_symbol("÷"))
ui.pB_mul.clicked.connect(lambda: new_symbol("×"))
ui.pB_sub.clicked.connect(lambda: new_symbol("−"))
ui.pB_add.clicked.connect(lambda: new_symbol("+"))
ui.pB_ob.clicked.connect(lambda: new_symbol("("))
ui.pB_cb.clicked.connect(lambda: new_symbol(")"))

ui.show()
exit(app.exec_())

