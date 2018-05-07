import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import "rxjs/add/operator/map";
import {DetailedDataModel} from "./header/content/search-page/search-results/result/detailed-data-model";

import {Iso639} from "./iso639";

@Injectable()
export class DetailService {
  TMDB_API_KEY = "6d23876cfa1749f6f3ea88a46a1f50df";

  TMDB_ROOT = "https://api.themoviedb.org/3/";

  detailedDataCache: DetailedDataModel;

  detailedDataSource: Subject<DetailedDataModel> = new Subject<DetailedDataModel>();
  detailedData$: Observable<DetailedDataModel> = this.detailedDataSource.asObservable();


  constructor(private http: HttpClient) {
  }

  getDetails(tid: number) {

    let imdbIdFormatted = DetailService.getTidFormatted(tid);

    this.getTmdbID(imdbIdFormatted).subscribe(tmdbID => {

      if (tmdbID != -1) {
        this.getDetailsAndCastByTmdbId(tmdbID).subscribe(details => {
          console.log(details);
          let detailedData = this.processDetailedData(details);
          this.detailedDataCache = detailedData;
          this.detailedDataSource.next(detailedData);
        });
      } else {
        this.detailedDataCache = null;
        this.detailedDataSource.next(null);
      }

    });

  }

  private processDetailedData(details) {

    return new DetailedDataModel(this.processCredits(details['credits']), details['budget'],
      Iso639.iso639ToName[details['original_language']],
      details['production_countries'].map(element => element['name']),
      new Date(details['release_date']), details['poster_path'],
      details['original_title']);
  }

  private processCredits(credits) {
    let creditsProcessed: string[][] = [];

    for (let cast of credits['cast']) {
      creditsProcessed.push([cast['name'], cast['character']]);
    }

    return creditsProcessed;
  }

  private static getTidFormatted(tidAsInt: number) {
    let tidAsString = tidAsInt.toString();
    let numberLeadingZeroes = 7 - tidAsString.length;
    let leadingZeroes = "";
    for (let i = 0; i < numberLeadingZeroes; i++) {
      leadingZeroes += "0";
    }
    return "tt" + leadingZeroes + tidAsString;

  }

  private getTmdbID(tid: string) {
    return this.http.get(
      this.TMDB_ROOT
      + 'find/'
      + tid
      + '?api_key='
      + this.TMDB_API_KEY
      + "&external_source=imdb_id")
      .map(data => {
        if (data['movie_results'].length > 0) {
          return data['movie_results'][0]['id'];
        } else {
          // no movie with this imdb-id found in TMDB
          return -1;
        }
      });
  }

  private getDetailsAndCastByTmdbId(tmdbID: number) {
    return this.http.get(
      this.TMDB_ROOT
      + 'movie/'
      + tmdbID
      + "?api_key="
      + this.TMDB_API_KEY
      + "&append_to_response=credits")
  }

  getCachedDetails() {
    this.detailedDataSource.next(this.detailedDataCache);
  }
}
