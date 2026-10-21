import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import (
    add_participant,
    initialize_database,
    load_activities,
    remove_participant,
)


class ActivityPersistenceTests(unittest.TestCase):
    def test_signups_survive_reinitialization_without_reseeding(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "activities.sqlite"
            initialize_database(database_path)

            add_participant("Chess Club", "newstudent@mergington.edu", database_path)
            remove_participant("Chess Club", "michael@mergington.edu", database_path)

            initialize_database(database_path)
            activities = load_activities(database_path)

            self.assertIn(
                "newstudent@mergington.edu",
                activities["Chess Club"]["participants"],
            )
            self.assertNotIn(
                "michael@mergington.edu",
                activities["Chess Club"]["participants"],
            )
            self.assertEqual(len(activities), 9)


if __name__ == "__main__":
    unittest.main()