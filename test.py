from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):
    """tests for every view function / feature!"""
    
    
    def setUp(self):
        """setUp for all test"""
        # can add: "self.client = app.test_client()""
        # to replace "with app.test_client() as client:"
        # to be "with self.client: as client"
        
        #can also add this outside def setUp(self):
        app.config['TESTING'] = True

        
    def test_homepage(self):
        """html display correctly?"""
        with app.test_client() as client:
            #make requests to flask via `client`
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            # check contents of html
            self.assertIn('<p>High Score:',html)
            self.assertIn('<button>add word</button>',html)
            # check: session['board'] = board; board = board when render_template
            self.assertIn('board', session)
            # check: highscore = session.get('highsore',0) =>highscore = 0;
            # highscore = highscore when render_template
            self.assertIsNone(session.get('highscore'))
            # check: nplays = session.get('nplays',0) =>highscore = 0;
            # nplays = nplays when render_template
            self.assertIsNone(session.get('nplays'))
            # check that we post data: highscore, score, timer
            self.assertIn(b'<p>High Score', resp.data)
            self.assertIn(b'Score:', resp.data)
            self.assertIn(b'Time left (seconds):', resp.data)
            
    def word_valid(self):
        """test word_exits and valid_word"""
        with app.test_client() as client:
            session['board'] = [["D", "O", "G", "G", "G"],
                                ["D", "O", "G", "G", "G"],
                                ["D", "O", "G", "G", "G"],
                                ["D", "O", "G", "G", "G"],
                                ["D", "O", "G", "G", "G"],]
            # is the correct word search is 'dog'?
            resp = client.get('/check-word?word=dog')
            # is the Boogle function check_valid_word return 'ok'?
            self.assertEqual(resp.json['result'],'ok')
            
    def word_not_on_board(self):
        """test word_exits but not valid_word"""
        with app.test_client() as client:
            resp = client.get('/check-word?word=excitement')
            self.assertEqual(resp.json['result'],'not-on-board')
            
    def not_word(self):
        """test word_not_exits and not valid_word"""
        with app.test_client() as client:
            resp = client.get('/check-word?word=asdfasd')
            self.assertEqual(resp.json['result'],'not-word')
            
    def post_score(self):
        """test post-score"""
        with app.test_client() as client:
            resp = client.post('/post-score')
            
            self.assertEqual(resp.status_code, 200)
            # does score post on html correction?
            self.assertIn(b'<p>High Score', resp.data)
            self.assertIn(b'Score:', resp.data)
            self.assertIn(b'Time left (seconds):', resp.data)
            
            # do we get the updated highscore & nplays which should not be 0?
            self.assertIsNotNone(session.get('highscore'))
            self.assertIsNotNone(session.get('nplays'))
            
    def post_brokeRecord_true(self):
        """test brokeRecord is True when score>highscore"""
        with app.test_client() as client:
            resp = client.post('/post-score', data={'score': 200})
            session['highscore'] = 100
            self.assertEqual(resp.json(),'True')
            
    def post_brokeRecord_false(self):
        """test brokeRecord is False when score<highscore"""
        with app.test_client() as client:
            resp = client.post('/post-score', data={'score': 80})
            session['highscore'] = 100
            self.assertEqual(resp.json(),'False')
            