#!/usr/bin/env python3


import os
import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy.freetype import FreeType, FTFace, ft_tag_to_string
from svgpy.utils import load

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


class FreeTypeTestCase(unittest.TestCase):
    def test_new_memory_face(self):
        path = 'fonts/dejavu/DejaVuSans.ttf'
        data, _ = load(path)
        face = FTFace.new_memory_face(data)

        face.select_charmap(FreeType.FT_ENCODING_UNICODE)
        charmap = face.charmap
        self.assertEqual(FreeType.FT_ENCODING_UNICODE, charmap.encoding)
        self.assertEqual(3, charmap.platform_id)
        self.assertEqual(10, charmap.encoding_id)

        # 12pt = 16px
        face.request_size(FreeType.FT_SIZE_REQUEST_TYPE_NOMINAL,
                          0,
                          12 * 64,
                          0,
                          96)
        index = face.get_char_index('x')
        self.assertTrue(index != 0)
        face.load_glyph(index, FreeType.FT_LOAD_RENDER)

        self.assertEqual(1, face.num_faces)
        self.assertEqual(0, face.face_index)

        self.assertTrue(not face.has_color())
        self.assertTrue(not face.has_fixed_sizes())
        self.assertTrue(face.has_glyph_names())
        self.assertTrue(face.has_horizontal())
        self.assertTrue(face.has_kerning())
        self.assertTrue(not face.has_multiple_masters())
        self.assertTrue(not face.has_vertical())
        self.assertTrue(not face.is_cid_keyed())
        self.assertTrue(not face.is_fixed_width())
        self.assertTrue(face.is_scalable())
        self.assertTrue(face.is_sfnt())
        self.assertTrue(not face.is_tricky())
        face_flags = (FreeType.FT_FACE_FLAG_SCALABLE
                      | FreeType.FT_FACE_FLAG_SFNT
                      | FreeType.FT_FACE_FLAG_HORIZONTAL
                      | FreeType.FT_FACE_FLAG_KERNING
                      | FreeType.FT_FACE_FLAG_GLYPH_NAMES
                      | FreeType.FT_FACE_FLAG_HINTER)
        self.assertEqual(0xa59, face_flags)
        self.assertEqual(0xa59, face.face_flags)

        self.assertEqual(0, face.style_flags)
        self.assertEqual(6253, face.num_glyphs)
        self.assertEqual('DejaVu Sans', face.family_name)
        self.assertEqual('Book', face.style_name)
        self.assertEqual(0, face.num_fixed_sizes)
        self.assertEqual([], face.available_sizes)
        self.assertEqual(5, face.num_charmaps)
        self.assertEqual(5, len(face.charmaps))

        bbox = face.bbox
        self.assertEqual(-33, bbox.x >> 6)
        self.assertEqual(-15, bbox.y >> 6)
        self.assertEqual(90, bbox.width >> 6)
        self.assertEqual(54, bbox.height >> 6)

        self.assertEqual(2048, face.units_per_em)
        self.assertEqual(29, face.ascender >> 6)
        self.assertEqual(-8, face.descender >> 6)
        self.assertEqual(37, face.height >> 6)
        self.assertEqual(59, face.max_advance_width >> 6)
        self.assertEqual(37, face.max_advance_height >> 6)
        self.assertEqual(-3, face.underline_position >> 6)
        self.assertEqual(1, face.underline_thickness >> 6)

        glyph = face.glyph
        self.assertEqual(620544, glyph.linear_hori_advance)
        self.assertEqual(1048576, glyph.linear_vert_advance)
        # self.assertEqual((576, 0), glyph.advance)
        self.assertEqual(1651078259, glyph.format)
        glyph_format = ft_tag_to_string(glyph.format)
        self.assertEqual('bits', glyph_format)
        # self.assertEqual(0, glyph.bitmap_left)
        self.assertEqual(9, glyph.bitmap_top)
        self.assertEqual(0, glyph.lsb_delta)
        self.assertEqual(0, glyph.rsb_delta)

        metrics = glyph.metrics
        # self.assertEqual(576, metrics.width)
        self.assertEqual(576, metrics.height)
        # self.assertEqual(0, metrics.hori_bearing_x)
        self.assertEqual(576, metrics.hori_bearing_y)
        # self.assertEqual(576, metrics.hori_advance)
        # self.assertEqual(-320, metrics.vert_bearing_x)
        self.assertEqual(192, metrics.vert_bearing_y)
        self.assertEqual(1024, metrics.vert_advance)

        bitmap = glyph.bitmap
        # self.assertEqual(9, bitmap.rows)
        # self.assertEqual(9, bitmap.width)
        # self.assertEqual(9, bitmap.pitch)
        self.assertEqual(256, bitmap.num_grays)
        self.assertEqual(2, bitmap.pixel_mode)

        outline = glyph.outline
        self.assertEqual(1, outline.n_contours)
        self.assertEqual(12, outline.n_points)
        points = outline.points
        self.assertIsInstance(points, list)
        self.assertEqual(12, len(points))
        self.assertIsInstance(points[0], tuple)
        self.assertEqual(2, len(points[0]))
        tags = outline.tags
        self.assertIsInstance(tags, list)
        self.assertEqual(12, len(tags))
        self.assertIsInstance(tags[0], int)
        contours = outline.contours
        self.assertIsInstance(contours, list)
        self.assertEqual(1, len(contours))
        self.assertIsInstance(contours[0], int)
        outline_flags = FreeType.FT_OUTLINE_HIGH_PRECISION
        self.assertEqual(0x100, outline_flags)
        self.assertEqual(0x100, outline.flags)

        metrics = face.size.metrics
        self.assertEqual(16, metrics.x_ppem)
        self.assertEqual(16, metrics.y_ppem)
        self.assertEqual(32768, metrics.x_scale)  # / 0x10000
        self.assertEqual(32768, metrics.y_scale)
        self.assertEqual(15, metrics.ascender >> 6)
        self.assertEqual(-4, metrics.descender >> 6)
        self.assertEqual(19, metrics.height >> 6)
        self.assertEqual(30, metrics.max_advance >> 6)

    def test_version(self):
        version = FreeType.library.version
        self.assertIsInstance(version, tuple)
        self.assertEqual(3, len(version))


if __name__ == '__main__':
    unittest.main()
