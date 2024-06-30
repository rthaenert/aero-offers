import unittest
import json

from classifier.classifier import AircraftTypeClassifier


class AircraftTypeClassifierTest(unittest.TestCase):
    def setUp(self):
        self.classifier = AircraftTypeClassifier()

    def test_aircraft_type_is_classified_even_when_model_is_unknown(self):
        with open('classifier_test_data_aircraft_type.json') as json_file:
            data = json.load(json_file)
            for item in data:
                title = item["title"]
                spider = item["spider"]
                if "aircraft_type" in item:
                    expected_type = item["aircraft_type"]
                    aircraft_type = self.classifier.classify(title, spider)
                    self.assertEqual(expected_type, aircraft_type,
                                     "Title: {0} Spider: {1} should have been classified as {2}, but was {3}"
                                     .format(title, spider, expected_type, aircraft_type))
