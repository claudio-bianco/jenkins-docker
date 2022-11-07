import script

def test_hello_world(capsys):
    script.hello_world()
    out, err = capsys.readouterr()

    assert out == 'hello world\n'
    assert err == ''
