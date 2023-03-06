import numpy as np
from base.condition_types import ConditionLevel
from conditions.models import BaseCondition
from conditions.raster_condition_retrieval_testcase import \
    RasterConditionRetrievalTestCase
from django.contrib.gis.geos import Polygon
from django.http import HttpRequest, QueryDict
from django.test import TestCase
from forsys.forsys_request_params import (
    ForsysGenerationRequestParamsFromUrlWithDefaults,
    ForsysRankingRequestParamsFromUrlWithDefaults)
from forsys.get_forsys_inputs import (
    ForsysGenerationInput, ForsysInputHeaders, ForsysRankingInput)
from planscape import settings


def _assert_dict_almost_equal(self,
                              d1: dict[str, list],
                              d2: dict[str, list]) -> None:
    for k in d1.keys():
        l1 = d1[k]
        if len(l1) > 0 and type(l1[0]) is float:
            np.testing.assert_array_almost_equal(l1, d2[k])
        else:
            self.assertListEqual(l1, d2[k])


class ForsysInputHeadersTest(TestCase):
    def test_sets_priority_headers(self):
        headers = ForsysInputHeaders(["p1", "p2", "p3"])
        self.assertListEqual(headers.priority_headers,
                             ["p_p1", "p_p2", "p_p3"])

    def test_priority(self):
        headers = ForsysInputHeaders([])
        self.assertEqual(headers.get_priority_header("priority"), "p_priority")

    def test_condition(self):
        headers = ForsysInputHeaders([])
        self.assertEqual(
            headers.get_condition_header("condition"),
            "c_condition")


class ForsysRankingInputTest(RasterConditionRetrievalTestCase):
    def setUp(self) -> None:
        RasterConditionRetrievalTestCase.setUp(self)

        foo_raster = RasterConditionRetrievalTestCase._create_raster(
            self, 4, 4, (.01, .02, .03, .04,
                         .05, .06, .07, .08,
                         .09, .10, .11, .12,
                         .13, .14, .15, .16))
        RasterConditionRetrievalTestCase._save_condition_to_db(
            self, "foo", "foo_normalized", foo_raster)
        bar_raster = RasterConditionRetrievalTestCase._create_raster(
            self, 4, 4, (.1, .1, .1, .1,
                         .2, .2, .2, .2,
                         .3, .3, .3, .3,
                         .4, .4, .4, .4))
        RasterConditionRetrievalTestCase._save_condition_to_db(
            self, "bar", "bar_normalized", bar_raster)

    def test_gets_forsys_input(self):
        qd = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysRankingRequestParamsFromUrlWithDefaults(qd)
        params.region = self.region
        params.priorities = ["foo", "bar"]
        params.project_areas.clear()
        params.project_areas[1] = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)
        params.project_areas[2] = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 1, 2, 3)

        headers = ForsysInputHeaders(params.priorities)

        input = ForsysRankingInput(params, headers)
        _assert_dict_almost_equal(self, input.forsys_input, {
            'proj_id': [1, 2],
            'stand_id': [1, 2],
            'area': [0.72, 0.36],
            'cost': [3600000000.0, 1800000000.0],
            'p_foo': [7.64, 3.54],
            'p_bar': [6.8, 2.6],
        })

    def test_missing_base_condition(self):
        qd = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysRankingRequestParamsFromUrlWithDefaults(qd)
        params.region = self.region
        # No base conditions exist for baz.
        params.priorities = ["foo", "bar", "baz"]
        params.project_areas.clear()
        params.project_areas[1] = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        with self.assertRaises(Exception) as context:
            ForsysRankingInput(params, headers)
        self.assertEqual(
            str(context.exception),
            "of 3 priorities, only 2 had base conditions")

    def test_missing_condition(self):
        # A base condition exists for baz, but a condition dosen't.
        BaseCondition.objects.create(
            condition_name="baz", region_name=self.region,
            condition_level=ConditionLevel.METRIC)

        qd = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysRankingRequestParamsFromUrlWithDefaults(qd)
        params.region = self.region
        params.priorities = ["foo", "bar", "baz"]
        params.project_areas.clear()
        params.project_areas[1] = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        with self.assertRaises(Exception) as context:
            ForsysRankingInput(params, headers)
        self.assertEqual(
            str(context.exception),
            "of 3 priorities, only 2 had conditions")

    def test_missing_condition_score(self):
        qd = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysRankingRequestParamsFromUrlWithDefaults(qd)
        params.region = self.region
        params.priorities = ["foo"]
        params.project_areas.clear()
        # project area doesn't intersect with the raster for "foo".
        params.project_areas[1] = RasterConditionRetrievalTestCase._create_geo(
            self, 5, 6, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        with self.assertRaises(Exception) as context:
            ForsysRankingInput(params, headers)
        self.assertEqual(
            str(context.exception),
            "no score was retrieved for condition, foo")


class ForsysGenerationInputTest(RasterConditionRetrievalTestCase):
    def setUp(self) -> None:
        RasterConditionRetrievalTestCase.setUp(self)

        foo_raster = RasterConditionRetrievalTestCase._create_raster(
            self, 4, 4, (.01, .02, .03, .04,
                         .05, .06, .07, .08,
                         .09, .10, .11, .12,
                         .13, .14, .15, .16))
        RasterConditionRetrievalTestCase._save_condition_to_db(
            self, "foo", "foo_normalized", foo_raster)
        bar_raster = RasterConditionRetrievalTestCase._create_raster(
            self, 4, 4, (.1, .1, .1, .1,
                         .2, .2, .2, .2,
                         .3, .3, .3, .3,
                         .4, .4, .4, .4))
        RasterConditionRetrievalTestCase._save_condition_to_db(
            self, "bar", "bar_normalized", bar_raster)

    def test_gets_forsys_input(self):
        dict = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysGenerationRequestParamsFromUrlWithDefaults(dict)
        params.region = self.region
        params.priorities = ["foo", "bar"]
        params.planning_area = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        input = ForsysGenerationInput(params, headers)
        _assert_dict_almost_equal(self, input.forsys_input, {
            'proj_id': [0, 0, 0, 0, 0, 0, 0, 0],
            'stand_id': [0, 1, 2, 3, 4, 5, 6, 7],
            'area': [.09, .09, .09, .09, .09, .09, .09, .09],
            'cost': [450000000, 450000000, 450000000, 450000000,
                     450000000, 450000000, 450000000, 450000000],
            'p_foo': [.99, .95, .98, .94, .97, .93, .96, .92],
            'p_bar': [.9, .8, .9, .8, .9, .8, .9, .8],
            'geo': [self._create_polygon_for_pixel(0, 0).wkt,
                    self._create_polygon_for_pixel(0, 1).wkt,
                    self._create_polygon_for_pixel(1, 0).wkt,
                    self._create_polygon_for_pixel(1, 1).wkt,
                    self._create_polygon_for_pixel(2, 0).wkt,
                    self._create_polygon_for_pixel(2, 1).wkt,
                    self._create_polygon_for_pixel(3, 0).wkt,
                    self._create_polygon_for_pixel(3, 1).wkt]
        })

    def test_gets_forsys_input_ignoring_nan(self):
        baz_raster = RasterConditionRetrievalTestCase._create_raster(
            self, 4, 4, (np.nan, np.nan, np.nan, np.nan,
                         .2, .2, .2, .2,
                         .3, .3, .3, .3,
                         .4, .4, .4, .4))
        RasterConditionRetrievalTestCase._save_condition_to_db(
            self, "baz", "baz_normalized", baz_raster)

        dict = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysGenerationRequestParamsFromUrlWithDefaults(dict)
        params.region = self.region
        params.priorities = ["foo", "baz"]
        params.planning_area = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        input = ForsysGenerationInput(params, headers)
        _assert_dict_almost_equal(self, input.forsys_input, {
            'proj_id': [0, 0, 0, 0],
            'stand_id': [0, 1, 2, 3],
            'area': [.09, .09, .09, .09],
            'cost': [450000000, 450000000, 450000000, 450000000],
            'p_foo': [.95, .94, .93, .92],
            'p_baz': [.8, .8, .8, .8],
            'geo': [self._create_polygon_for_pixel(0, 1).wkt,
                    self._create_polygon_for_pixel(1, 1).wkt,
                    self._create_polygon_for_pixel(2, 1).wkt,
                    self._create_polygon_for_pixel(3, 1).wkt]
        })

    def _create_polygon_for_pixel(self, x, y) -> Polygon:
        xmin = self.xorig + self.xscale * x
        xmax = xmin + self.xscale
        ymin = self.yorig + self.yscale * y
        ymax = ymin + self.yscale

        geo = Polygon(
            ((xmin, ymin),
             (xmin, ymax),
             (xmax, ymax),
             (xmax, ymin),
             (xmin, ymin)))
        geo.srid = settings.CRS_FOR_RASTERS
        return geo

    def test_missing_base_condition(self):
        dict = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysGenerationRequestParamsFromUrlWithDefaults(dict)
        params.region = self.region
        # No base conditions exist for baz.
        params.priorities = ["foo", "bar", "baz"]
        params.planning_area = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        with self.assertRaises(Exception) as context:
            ForsysGenerationInput(params, headers)
        self.assertEqual(
            str(context.exception),
            "of 3 priorities, only 2 had base conditions")

    def test_missing_condition(self):
        # A base condition exists for baz, but a condition dosen't.
        BaseCondition.objects.create(
            condition_name="baz", region_name=self.region,
            condition_level=ConditionLevel.METRIC)

        dict = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysGenerationRequestParamsFromUrlWithDefaults(dict)
        params.region = self.region
        params.priorities = ["foo", "bar", "baz"]
        params.planning_area = RasterConditionRetrievalTestCase._create_geo(
            self, 0, 3, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        with self.assertRaises(Exception) as context:
            ForsysGenerationInput(params, headers)
        self.assertEqual(
            str(context.exception),
            "of 3 priorities, only 2 had conditions")

    def test_no_intersection_between_plan_and_raster(self):
        dict = QueryDict('set_all_params_via_url_with_default_values=1')
        params = ForsysGenerationRequestParamsFromUrlWithDefaults(dict)
        params.region = self.region
        params.priorities = ["foo"]
        # project area doesn't intersect with the raster for "foo".
        params.planning_area = RasterConditionRetrievalTestCase._create_geo(
            self, 5, 6, 0, 1)

        headers = ForsysInputHeaders(params.priorities)

        with self.assertRaises(Exception) as context:
            ForsysGenerationInput(params, headers)
        self.assertEqual(
            str(context.exception),
            "plan has no intersection with condition raster, foo")
