import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BackendConstants } from '../backend-constants';
import {
  BehaviorSubject,
  catchError,
  map,
  Observable,
  of,
  take,
  tap,
} from 'rxjs';

import { BasePlan, Plan, Region } from '../types';

export interface PlanState {
  all: {
    [planId: string]: Plan;
  };
  currentPlanId: Plan['id'] | null;
}

export interface BackendPlan {
  id?: number;
  name: string;
  owner?: number;
  region: Region;
  geometry: GeoJSON.GeoJSON;
}

@Injectable({
  providedIn: 'root',
})
export class PlanService {
  // Warning: do not mutate state!
  readonly planState$ = new BehaviorSubject<PlanState>({
    all: {}, // All plans indexed by id
    currentPlanId: null,
  });

  constructor(private http: HttpClient) {}

  /** Makes a request to the backend to create a plan and updates state. */
  createPlan(
    basePlan: BasePlan
  ): Observable<{ success: boolean; result?: Plan }> {
    return this.createPlanApi(basePlan).pipe(
      take(1),
      map((createdPlan) => {
        return {
          success: true,
          result: createdPlan,
        };
      }),
      tap(({ result: createdPlan }) => {
        this.addPlanToState(createdPlan);
      }),
      catchError((e: HttpErrorResponse) => {
        return of({
          success: false,
        });
      })
    );
  }

  /** Makes a request to the backend to fetch a plan with the given ID. */
  getPlan(planId: string): Observable<Plan> {
    return this.http
      .get<BackendPlan>(
        BackendConstants.END_POINT.concat('/plan/get_plan/?id=', planId),
        {
          withCredentials: true,
        }
      )
      .pipe(
        take(1),
        map((dbPlan) => this.convertToPlan(dbPlan))
      );
  }

  private convertToPlan(plan: BackendPlan): Plan {
    return {
      id: String(plan.id),
      ownerId: String(plan.owner),
      name: plan.name,
      region: plan.region,
      planningArea: plan.geometry,
    };
  }

  private convertToDbPlan(plan: BasePlan): BackendPlan {
    return {
      owner: Number(plan.ownerId),
      name: plan.name,
      region: plan.region,
      geometry: plan.planningArea,
    };
  }

  private addPlanToState(plan: Plan) {
    // Object.freeze() enforces shallow runtime immutability
    const currentState = Object.freeze(this.planState$.value);
    const updatedState = Object.freeze({
      ...currentState,
      all: {
        ...currentState.all,
        [plan.id]: plan,
      },
    });

    this.planState$.next(updatedState);
  }

  private createPlanApi(plan: BasePlan): Observable<Plan> {
    const createPlanRequest = this.convertToDbPlan(plan);
    return this.http
      .post(BackendConstants.END_POINT + '/plan/create/', createPlanRequest, {
        withCredentials: true,
      })
      .pipe(
        take(1),
        map((result) => {
          return {
            ...plan,
            id: result.toString(),
          };
        })
      );
  }
}
