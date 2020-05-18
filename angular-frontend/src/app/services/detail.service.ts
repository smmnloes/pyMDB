import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable, of, throwError} from "rxjs";
import "rxjs/add/operator/map";
import {DetailedDataModel} from "../header/content/search-page/search-results/result/detailed-data-model";

import {Iso639} from "../util/iso639";
import {CacheService} from "./cache.service";
import {catchError, map} from "rxjs/operators";

@Injectable()
export class DetailService {
  TMDB_ROOT = "https://api.themoviedb.org/3/";

  constructor(private http: HttpClient, private cacheService: CacheService) {
  }


  getDetails(IMDB_Id: number): Observable<DetailedDataModel> {
    let cachedDetails = this.cacheService.getDetails(IMDB_Id);
    if (cachedDetails != null) {
      return cachedDetails.hasDetails ? of(cachedDetails) : throwError({status: 404, message: "No detailed data available"});
    }

    let options = {
      headers: {'Content-Type': 'application/json'},
      params: new HttpParams().set("imdbid", IMDB_Id.toString())
    };

    return this.http.get('api/details', options).pipe(
      map(
        result => {
          let detailedDataProcessed = DetailService.processDetailedData(result);
          this.cacheDetailData(detailedDataProcessed, IMDB_Id);
          return detailedDataProcessed;
        }
      ), catchError(error => {
        let emptyDetails = DetailedDataModel.createEmptyDetails();
        this.cacheDetailData(emptyDetails, IMDB_Id);
        return throwError(error);
      })
    );
  }

  private cacheDetailData(detailedData: DetailedDataModel, IMDB_Id: number): void {
    this.cacheService.setDetails(IMDB_Id, detailedData)
  }

  private static processDetailedData(details: Object): DetailedDataModel {
    return new DetailedDataModel(
      DetailService.processCredits(details['credits']),
      details['budget'],
      Iso639.iso639ToName[details['original_language']],
      details['production_countries'].map(element => element['name']),
      new Date(details['release_date']),
      details['poster_path'],
      details['overview'],
      true);
  }

  private static processCredits(credits: Object): string[][] {
    let creditsProcessed: string[][] = [];

    for (let cast of credits['cast']) {
      creditsProcessed.push([cast['name'], cast['character']]);
    }
    return creditsProcessed;
  }
}
