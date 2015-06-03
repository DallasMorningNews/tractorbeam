#!/usr/bin/env python
import unittest
import tractorbeam
from PIL import Image
import six

class TractorBeamTestCase(unittest.TestCase):

    def setUp(self):
    	tractorbeam.app.config['TESTING'] = True
        self.app = tractorbeam.app.test_client()

    def tearDown(self):
        pass


    def test_serves_landing_page(self):
    	req = self.app.get("/")
    	assert req.status_code == 200

    def test_accepts_valid_image_requests(self):
    	form = {'url': 'http://www.google.com', 'selector': 'body'}
    	req = self.app.get("/image", query_string=form)
    	assert req.status_code == 200

    def test_rejects_invalid_valid_image_requests(self):
		form = {'monkey':'bars', 'happy':'clown'}
		req = self.app.get("/image", data=form)
		assert req.status_code == 400

    def test_generates_correct_image(self):
        form = {'selector':'p', 'url': 'http://www.w3.org/History/19921103-hypertext/hypertext/WWW/TheProject.html'}
        req = self.app.get("/image", query_string=form)
        result_image = Image.open(six.BytesIO(req.get_data()))
        test_image_file =  Image.open("test/test_result_image.png")
        assert result_image.tostring() == test_image_file.tostring()

    def test_rejects_invalid_url(self):
		form = {'selector':'p', 'url': 'file:///www.w3.org/History/19921103-hypertext/hypertext/WWW/TheProject.html'}
		req = self.app.get("/image", query_string=form)
		assert req.status_code == 403

    def test_tractorbeam_redirectes_to_correct_image_when_trailing_slash(self):
        form = {'selector':'p', 'url': 'http://www.w3.org/History/19921103-hypertext/hypertext/WWW/TheProject.html'}
        req = self.app.get("/image/", query_string=form, follow_redirects=True)
        result_image = Image.open(six.BytesIO(req.get_data()))
        test_image_file =  Image.open("test/test_result_image.png")
        assert result_image.tostring() == test_image_file.tostring()



if __name__ == '__main__':
    unittest.main()
