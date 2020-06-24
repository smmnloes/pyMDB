import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable, throwError} from "rxjs";
import "rxjs/add/operator/map";
import {DetailedDataModel} from "../header/content/search-page/search-results/result/detailed-data-model";
import {catchError, map} from "rxjs/operators";

@Injectable()
export class DetailService {

  constructor(private http: HttpClient) {
  }


  hasDetails(IMDB_Id: number): Observable<boolean> {
    return this.http.get('api/movies/has_details', {params: new HttpParams().set("imdbid", IMDB_Id.toString())}).map(result => <boolean>result);
  }


  getDetails(IMDB_Id: number): Observable<DetailedDataModel> {

    let options = {
      headers: {'Content-Type': 'application/json'},
      params: new HttpParams().set("imdbid", IMDB_Id.toString())
    };

    return this.http.get('api/movies/details', options).pipe(
      map(
        result => {
          return DetailedDataModel.fromJSON(result);
        }
      ), catchError(error => {
        let emptyDetails = DetailedDataModel.createEmptyDetails();
        return throwError(error);
      })
    );
  }

}
