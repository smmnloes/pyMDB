import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable, of, throwError} from "rxjs";
import "rxjs/add/operator/map";
import {DetailedDataModel} from "../header/content/search-page/search-results/result/detailed-data-model";
import {CacheService} from "./cache.service";
import {catchError, map} from "rxjs/operators";

@Injectable()
export class DetailService {

  constructor(private http: HttpClient, private cacheService: CacheService) {
  }


  hasDetails(IMDB_Id: number): Observable<boolean> {
    return this.http.get('api/has_details', {params: new HttpParams().set("imdbid", IMDB_Id.toString())}).map(result => <boolean>result);
  }


  getDetails(IMDB_Id: number): Observable<DetailedDataModel> {
    let cachedDetails = this.cacheService.getDetails(IMDB_Id);
    if (cachedDetails != null) {
      return cachedDetails.hasDetails ? of(cachedDetails) : throwError({
        status: 404,
        message: "No detailed data available"
      });
    }

    let options = {
      headers: {'Content-Type': 'application/json'},
      params: new HttpParams().set("imdbid", IMDB_Id.toString())
    };

    return this.http.get('api/details', options).pipe(
      map(
        result => {
          let detailedDataProcessed = DetailedDataModel.fromJSON(result);
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
}
