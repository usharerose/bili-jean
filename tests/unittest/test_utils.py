"""
Unit test for utils
"""
from unittest import TestCase

from bili_jean.utils import parse_aid, parse_bvid


class UtilsTestCase(TestCase):

    def test_parse_aid(self):
        sample_aid = 2271112
        sample_url = f'https://www.bilibili.com/video/av{sample_aid}/'
        aid = parse_aid(sample_url)
        self.assertEqual(aid, sample_aid)

    def test_parse_aid_with_query_parameters(self):
        sample_aid = 2271112
        sample_url = f'https://www.bilibili.com/video/av{sample_aid}/?vd_source=eab9f46166d54e0b07ace25e908097ae'
        aid = parse_aid(sample_url)
        self.assertEqual(aid, sample_aid)

    def test_parse_aid_without_slash(self):
        sample_aid = 2271112
        sample_url = f'https://www.bilibili.com/video/av{sample_aid}'
        aid = parse_aid(sample_url)
        self.assertEqual(aid, sample_aid)

    def test_parse_aid_with_invalid_pattern(self):
        sample_aid = 2271112
        sample_url = f'https://www.bilibili.com/video/a{sample_aid}/'
        with self.assertRaises(ValueError):
            parse_aid(sample_url)

    def test_parse_aid_with_invalid_characters(self):
        sample_aid = '22h1112'
        sample_url = f'https://www.bilibili.com/video/av{sample_aid}/'
        aid = parse_aid(sample_url)
        self.assertEqual(aid, int(sample_aid[:2]))

    def test_parse_aid_with_invalid_length(self):
        sample_aid = 2251799813685249
        sample_url = f'https://www.bilibili.com/video/av{sample_aid}'
        with self.assertRaises(ValueError):
            parse_aid(sample_url)

    def test_parse_bvid(self):
        sample_bvid = 'BV1x54y1e7zf'
        sample_url = f'https://www.bilibili.com/video/{sample_bvid}/'
        bvid = parse_bvid(sample_url)
        self.assertEqual(bvid, sample_bvid)

    def test_parse_bvid_with_query_parameters(self):
        sample_bvid = 'BV1x54y1e7zf'
        sample_url = f'https://www.bilibili.com/video/{sample_bvid}/?vd_source=eab9f46166d54e0b07ace25e908097ae'
        bvid = parse_bvid(sample_url)
        self.assertEqual(bvid, sample_bvid)

    def test_parse_bvid_without_slash(self):
        sample_bvid = 'BV1x54y1e7zf'
        sample_url = f'https://www.bilibili.com/video/{sample_bvid}'
        bvid = parse_bvid(sample_url)
        self.assertEqual(bvid, sample_bvid)

    def test_parse_bvid_with_invalid_pattern(self):
        sample_bvid = 'BVx54y1e7zf'
        sample_url = f'https://www.bilibili.com/video/{sample_bvid}/'
        with self.assertRaises(ValueError):
            parse_bvid(sample_url)

    def test_parse_bvid_with_invalid_characters(self):
        sample_bvid = 'BV1x54y=e7zf'
        sample_url = f'https://www.bilibili.com/video/{sample_bvid}/'
        with self.assertRaises(ValueError):
            parse_bvid(sample_url)

    def test_parse_bvid_with_invalid_length(self):
        sample_bvid = 'BV1x54y1e7zf6'
        sample_url = f'https://www.bilibili.com/video/{sample_bvid}'
        bvid = parse_bvid(sample_url)
        self.assertEqual(bvid, sample_bvid[:3 + 9])
