import unittest
from pyvisgrap


def retunr_LiteGraphJson():
    return {


    }


class OcrTest(unittest.TestCase):

    def test_ocr_load_and_json(self):
        ocr = Ocr.load(ocr_data)
        assert isinstance(ocr, Ocr)
        assert isinstance(ocr.detection_map, DetectionMap)
        assert isinstance(ocr.position, Position)

        assert

        self.assertEqual(ocr.latex, ocr_data['latex'])
        self.assertEqual(ocr.latex_confidence, ocr_data['latex_confidence'])
        self.assertEqual(ocr.detection_map.is_inverted, ocr_data['detection_map']['is_inverted'])

        self.assertEqual(ocr.__json__().keys(), ocr_data.keys())

    def test_position_load_and_json(self):
        position = Position.load(position_data)
        assert isinstance(position, Position)
        self.assertEqual(position.width, position_data['width'])
        self.assertEqual(position.top_left_y, position_data['top_left_y'])
        self.assertEqual(position.top_left_x, position_data['top_left_x'])
        self.assertEqual(position.height, position_data['height'])
        self.assertEqual(position.__json__().keys(), position_data.keys())