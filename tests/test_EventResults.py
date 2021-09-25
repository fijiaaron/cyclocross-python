import pytest
import conftest 
from uci.EventResults import EventResultsFrame

@pytest.fixture
def page(driver):   
    page:EventResultsFrame = EventResultsFrame(driver)
    page.open("https://dataride.uci.org/iframe/EventResults/253649?competitionId=65009&disciplineId=3")

    yield page

# def test_get_table_headers(page:EventResultsFrame):
#     headers = page.get_table_headers()
#     print(headers)

#     assert len(headers) == 9
#     assert headers == ['Rank', 'BIB', 'Rider', 'Nation', 'Team', 'Age', 'Result', 'IRM', 'Points']
    
# def test_get_table_data(page:EventResultsFrame):
#     data = page.get_table_data()
#     print(data)

#     assert data is not ""   

def test_get_table_row_data(page:EventResultsFrame):
    rows = page.get_table_row_data()
    print(rows)

    assert len(rows) == 21  
    assert rows != None   
