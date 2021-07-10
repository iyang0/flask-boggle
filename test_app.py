from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('''<input
        name="word"
        id="wordInput"
        class="word-input"
        autofocus aria-label="Word">''', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            # data = response.get_data(as_text=True)
            data = response.get_json()
            
            #test if the data coming back is JSON and if it contains gameId and Board
            self.assertIsInstance(data, dict)
            self.assertIn("gameId",data)
            self.assertIsInstance(data["gameId"], str)
            self.assertIn("board",data)
            self.assertIsInstance(data["board"], list)
            
            #test if the game ID coming back is in the dictionary on the server.
            self.assertIn(data["gameId"], games)
            # write a test for this route

    def test_api_score_word(self):
        """test scoring a word"""
        with self.client as client:
            
            # make a test game and then change the board to a set test board
            test_board = [
                ["A", "C", "A", "R", "I"], 
                ["A", "C", "E", "C", "G"],
                ["T", "U", "E", "B", "R"], 
                ["Z", "I", "X", "S", "R"], 
                ["S", "H", "M", "C", "E"]] 
            create_response = client.get('/api/new-game')
            created_game = create_response.get_json()
            test_id = created_game["gameId"]
            
            # print("THIS IS THE TEST ID = "+test_id)
            games[test_id].board = test_board
            # print(games[test_id].board)
            
            #test word that should be on board and is in dictionary
            response = client.post('/api/score-word',
                json = {
                    "gameId" : test_id,
                    "word" : "ACARI"
                    })
            
            data = response.get_json()
            
            self.assertTrue(data["result"] == "ok")
            self.assertEqual(data, {"result": "ok"})
            
            #test response of non-words
            response = client.post('/api/score-word',
                json = {
                    "gameId" : test_id,
                    "word" : "fdsaf"
                    })
            
            data = response.get_json()
            
            self.assertTrue(data["result"] == "not-word")
            
            #test response of words that are not on board
            response = client.post('/api/score-word',
                json = {
                    "gameId" : test_id,
                    "word" : "lettuce"
                    })
            
            data = response.get_json()
            
            self.assertTrue(data["result"] == "not-on-board")