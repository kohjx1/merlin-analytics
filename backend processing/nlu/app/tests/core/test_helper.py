from app.core import helper

def test_get_numeric_answer():
    assert helper.get_numeric_answer("I am handsome") == (None, [])
    assert helper.get_numeric_answer("twenty three") == ("23", ["twenty three"])
    assert helper.get_numeric_answer("one thousand two hundred and thirty five") == ("1235", ["one thousand two hundred thirty five"])
    assert helper.get_numeric_answer("two hundred and thirty thousand, four hundred and seventy six apples") == ("230476", ["two hundred thirty thousand four hundred seventy six"])
    assert helper.get_numeric_answer("he is born in nineteen sixty six but") == ("1966", ["nineteen sixty six"])
    assert helper.get_numeric_answer("twenty nineteen") == ("2019", ["twenty nineteen"])
    assert helper.get_numeric_answer("three thousand") == ("3000", ["three thousand"])


def test_pre_process_text():
    sample_text = "The quick brown fox jumped over the fence"
    assert helper.pre_process_text(sample_text, stop=True) == ['quick', 'brown', 'fox', 'jumped', 'fence']
    assert helper.pre_process_text(sample_text, stop=True, lemma=True) == ['quick', 'brown', 'fox', 'jumped', 'fence']
    assert helper.pre_process_text(sample_text, stop=True, stem=True) == ['quick', 'brown', 'fox', 'jump', 'fenc']


def test_is_subsequence():
    assert helper.is_subsequence(["little", "tree"], ["I", "am", "a", "happy", "little", "tree"]) == True
    assert helper.is_subsequence(["happy", "tree"], ["I", "am", "a", "happy", "little", "tree"]) == False
    assert helper.is_subsequence(["tree"], ["I", "am", "a", "happy", "little", "tree"]) == True
    assert helper.is_subsequence(["lit"], ["I", "am", "a", "happy", "little", "tree"]) == False