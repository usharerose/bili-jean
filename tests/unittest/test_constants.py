"""
Unit test for constants
"""
from unittest import TestCase

from bili_jean.constants import (
    AudioBitRateID,
    FormatNumberValue,
    QualityNumber,
    VideoCodecID
)


class QualityNumberTestCase(TestCase):

    def test_is_login_needed(self):
        self.assertTrue(QualityNumber.P1080.is_login_needed)
        self.assertFalse(QualityNumber.P360.is_login_needed)

    def test_is_vip_needed(self):
        self.assertTrue(QualityNumber.P1080_60.is_vip_needed)
        self.assertFalse(QualityNumber.P360.is_vip_needed)

    def test_from_value(self):
        self.assertEqual(
            QualityNumber.from_value(127),
            QualityNumber.EIGHT_K
        )

    def test_from_value_with_unsupported_number(self):
        with self.assertRaises(ValueError):
            QualityNumber.from_value(0)


class FormatNumberValueTestCase(TestCase):

    def test_full_format(self):
        self.assertEqual(
            FormatNumberValue.full_format(),
            4048  # 111111010000
        )

    def test_get_format_number_value_for_hdr(self):
        self.assertEqual(
            FormatNumberValue.get_format_number_value(
                QualityNumber.HDR.value,
                False
            ),
            208,  # 000011010000
        )

    def test_get_format_number_value_for_dolby_vision_and_audio(self):
        self.assertEqual(
            FormatNumberValue.get_format_number_value(
                QualityNumber.DOLBY.value,
                True
            ),
            912,  # 001110010000
        )

    def test_get_format_number_value_for_eight_k(self):
        self.assertEqual(
            FormatNumberValue.get_format_number_value(
                QualityNumber.EIGHT_K.value,
                False
            ),
            1168,  # 010010010000
        )


class AudioBitRateIDTestCase(TestCase):

    def test_from_value(self):
        self.assertEqual(
            AudioBitRateID.from_value(30280),
            AudioBitRateID.BPS_192K
        )

    def test_from_value_with_unsupported_number(self):
        with self.assertRaises(ValueError):
            AudioBitRateID.from_value(0)


class VideoCodecIDTestCase(TestCase):

    def test_from_value(self):
        self.assertEqual(
            VideoCodecID.from_value(13),
            VideoCodecID.AV1
        )

    def test_from_value_with_unsupported_number(self):
        with self.assertRaises(ValueError):
            VideoCodecID.from_value(0)
