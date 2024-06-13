import unittest
import main
import time


class TestPomodoro(unittest.TestCase):
    def test_countdown_basic(self):
        given    = 3
        expected = 3

        c = main.countdown(given)
        self.assertEqual(c, expected)

    def test_countdown_complete(self):
        given    = 3
        expected = 3

        started_at = time.time()
        _ = main.countdown(given)
        ended_at = time.time()

        difference = round(ended_at - started_at)

        self.assertEqual(difference, expected)

    def test_pomodoro_basic(self):
        session_given, session_time_given, short_rest_given, long_rest_given = 1, 1, 1, 1
        
        expected_sessions = 1
        expected_short_rest = 0
        expected_long_rest = 1

        pomodoro_stats = main.pomodoro(
            sessions=session_given, 
            session_time=session_time_given, 
            short_rest_time=short_rest_given, 
            long_rest_time=long_rest_given
        )
        
        self.assertEqual(len(pomodoro_stats['sessions']), expected_sessions)
        self.assertEqual(len(pomodoro_stats['short_rest_sessions']), expected_short_rest)
        self.assertEqual(len(pomodoro_stats['long_rest_sessions']), expected_long_rest)

if __name__ == '__main__':
    unittest.main()
