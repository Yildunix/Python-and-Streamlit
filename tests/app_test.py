from streamlit.testing.v1 import AppTest

def test1():
    at = AppTest.from_file("app.py").run(timeout=10)
    assert at.selectbox[0].value == 'year'

def test2():
    at = AppTest.from_file("app.py").run(timeout=10)
    at.selectbox[0].set_value('make').run()
    assert at.selectbox[0].value == 'make'


def test3():
    at = AppTest.from_file("app.py").run(timeout=10)
    at.text_input[0].set_value('Marque du véhicule').run()
    assert at.text_input[0].value == 'Marque du véhicule'

def test4():
    at = AppTest.from_file("app.py").run(timeout=10)
    at.text_input[0].set_value('Modèle du véhicule').run()
    assert at.text_input[0].value == 'Modèle du véhicule'
