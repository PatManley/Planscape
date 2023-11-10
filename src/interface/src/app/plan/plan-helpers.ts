import area from '@turf/area';
import { FeatureCollection } from 'geojson';
import { ScenarioResult } from '../types';
import {
  ProjectAreaReport,
  ProjectTotalReport,
} from './project-areas/project-areas.component';
import { PROJECT_AREA_COLORS } from '../shared/constants';

export const NOTE_SAVE_INTERVAL = 5000;

export const POLLING_INTERVAL = 3000;

export const STAND_SIZES = ['SMALL', 'MEDIUM', 'LARGE'];

const SQUARE_METERS_PER_ACRE = 0.0002471054;

export function calculateAcres(planningArea: GeoJSON.GeoJSON) {
  const squareMeters = area(planningArea as FeatureCollection);
  const acres = squareMeters * SQUARE_METERS_PER_ACRE;
  return Math.round(acres);
}

export function parseResultsToProjectAreas(
  results: ScenarioResult
): ProjectAreaReport[] {
  return results.result.features.map((featureCollection, i) => {
    const props = featureCollection.properties;
    return {
      id: i + 1,
      acres: props.area_acres,
      percentTotal: props.pct_area,
      estimatedCost: props.total_cost,
      score: props.weightedPriority,
    };
  });
}

export function parseResultsToTotals(
  areaReports: ProjectAreaReport[]
): ProjectTotalReport {
  return areaReports.reduce(
    (acc, value) => {
      acc.acres += value.acres;
      acc.estimatedCost += value.estimatedCost;
      acc.percentTotal += value.percentTotal;
      return acc;
    },
    {
      acres: 0,
      percentTotal: 0,
      estimatedCost: 0,
    }
  );
}

export function getColorForProjectPosition(position: number) {
  const id = position;
  return PROJECT_AREA_COLORS[(id - 1) % PROJECT_AREA_COLORS.length];
}
