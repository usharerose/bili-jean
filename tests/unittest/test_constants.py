"""
Unit test for constants
"""
from unittest import TestCase

from bili_jean.constants import (
    VideoWorkFormatNumberValue,
    VideoWorkQualityNumber
)


class VideoWorkQualityNumberTestCase(TestCase):

    def test_is_login_needed(self):
        self.assertTrue(VideoWorkQualityNumber.P1080.is_login_needed)
        self.assertFalse(VideoWorkQualityNumber.P360.is_login_needed)

    def test_is_vip_needed(self):
        self.assertTrue(VideoWorkQualityNumber.P1080_60.is_vip_needed)
        self.assertFalse(VideoWorkQualityNumber.P360.is_vip_needed)

    def test_from_value(self):
        self.assertEqual(
            VideoWorkQualityNumber.from_value(127),
            VideoWorkQualityNumber.EIGHT_K
        )

    def test_from_value_with_unsupported_number(self):
        with self.assertRaises(ValueError):
            VideoWorkQualityNumber.from_value(0)


class VideoWorkFormatNumberValueTestCase(TestCase):

    def test_full_format(self):
        self.assertEqual(
            VideoWorkFormatNumberValue.full_format(),
            4048  # 111111010000
        )

    def test_get_format_number_value_for_hdr(self):
        self.assertEqual(
            VideoWorkFormatNumberValue.get_format_number_value(
                VideoWorkQualityNumber.HDR.value,
                False
            ),
            208,  # 000011010000
        )

    def test_get_format_number_value_for_dolby_vision_and_audio(self):
        self.assertEqual(
            VideoWorkFormatNumberValue.get_format_number_value(
                VideoWorkQualityNumber.DOLBY.value,
                True
            ),
            912,  # 001110010000
        )
