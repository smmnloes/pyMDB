import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import "rxjs/add/operator/map";
import {DetailedDataModel} from "../header/content/search-page/search-results/result/detailed-data-model";

import {Iso639} from "../util/iso639";
import {TMDB_API_KEY} from "../util/tmdb-api-key";
import {CacheService} from "./cache.service";

@Injectable()
export class DetailService {
  TMDB_ROOT = "https://api.themoviedb.org/3/";

  detailedDataSource: Subject<DetailedDataModel> = new Subject<DetailedDataModel>();
  detailedData$: Observable<DetailedDataModel> = this.detailedDataSource.asObservable();


  constructor(private http: HttpClient, private cacheService: CacheService) {
  }

  getDetails(IMDB_Id: number) {
    let cachedDetails = this.cacheService.getDetails(IMDB_Id);
    if (cachedDetails != null) {
      this.detailedDataSource.next(cachedDetails);
      return;
    }

    let IMDB_Id_Formatted = DetailService.formatIMDB_Id(IMDB_Id);

    this.getTMDB_Id(IMDB_Id_Formatted).subscribe(tmdbID => {
      if (tmdbID == -1) {
        this.detailedDataSource.next(null);
      } else {
        this.getDetailsForTMDB_Id(tmdbID).subscribe(detailedData => {
          let detailedDataProcessed = this.processDetailedData(detailedData);
          this.detailedDataSource.next(detailedDataProcessed);
          this.cacheService.setDetails(IMDB_Id, detailedDataProcessed);
        });
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

  private static formatIMDB_Id(tidAsInt: number) {
    let tidAsString = tidAsInt.toString();
    let numberLeadingZeroes = 7 - tidAsString.length;
    let leadingZeroes = "";
    for (let i = 0; i < numberLeadingZeroes; i++) {
      leadingZeroes += "0";
    }
    return "tt" + leadingZeroes + tidAsString;

  }

  private getTMDB_Id(tid: string) {
    return this.http.get(
      this.TMDB_ROOT
      + 'find/'
      + tid
      + '?api_key='
      + TMDB_API_KEY
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

  private getDetailsForTMDB_Id(tmdbID: number) {
    return this.http.get(
      this.TMDB_ROOT
      + 'movie/'
      + tmdbID
      + "?api_key="
      + TMDB_API_KEY
      + "&append_to_response=credits")
  }
}
