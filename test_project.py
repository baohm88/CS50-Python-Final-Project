from project import validate_status, get_status, registered_before, exists_in_db, showresult


def test_showresult():
    assert showresult(50) == "You have completed 50%"
    assert showresult(100) == "You have completed 100%. Congratulations! Keep it up!"
    assert showresult(0) == "You have completed 0%. Please start studying hard!"

def test_validate_status():
    assert validate_status('1') == True
    assert validate_status('2') == True
    assert validate_status('0') == None


def test_get_status():
    assert get_status('1') == 'Ongoing'
    assert get_status('2') == 'Completed'


def test_registered_before():
    assert registered_before('1') == True
    assert registered_before('9') == False

def test_exists_in_db():
    assert exists_in_db('1') == True
    assert exists_in_db('9') == True
    assert exists_in_db('0') == False


