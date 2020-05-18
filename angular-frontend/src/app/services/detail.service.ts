import {first, map, take} from 'rxjs/operators';
import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, Subject} from "rxjs";
import "rxjs/add/operator/map";
import {DetailedDataModel} from "../header/content/search-page/search-results/result/detailed-data-model";

import {Iso639} from "../util/iso639";
import {TMDB_API_KEY} from "../tmdb-api-key";
import {CacheService} from "./cache.service";

@Injectable()
export class DetailService {
  TMDB_ROOT = "https://api.themoviedb.org/3/";

  detailedDataSource: Subject<DetailedDataModel> = new Subject<DetailedDataModel>();
  detailedData$: Observable<DetailedDataModel> = this.detailedDataSource.asObservable();

  configData;

  constructor(private http: HttpClient, private cacheService: CacheService) {
    http.get(this.TMDB_ROOT + 'configuration?api_key=' + TMDB_API_KEY).pipe(take(1)).subscribe(configData => {
      this.configData = configData;
    });
  }


  getDetails(IMDB_Id: number): void {
    let cachedDetails = this.cacheService.getDetails(IMDB_Id);
    if (cachedDetails != null) {
      this.detailedDataSource.next(cachedDetails);
      return;
    }

    let IMDB_Id_Formatted = DetailService.formatIMDB_Id(IMDB_Id);

    this.getTMDB_Id(IMDB_Id_Formatted).pipe(first()).subscribe(tmdbID => {
      if (tmdbID == -1) {
        let emptyDetails = DetailedDataModel.createEmptyDetails();
        this.pushDetailsAndCache(emptyDetails, IMDB_Id);
      } else {
        this.getDetailsForTMDB_Id(tmdbID).pipe(first()).subscribe(detailedData => {
          let detailedDataProcessed = this.processDetailedData(detailedData);
          this.pushDetailsAndCache(detailedDataProcessed, IMDB_Id)
        });
      }
    });

  }

  private pushDetailsAndCache(detailedData: DetailedDataModel, IMDB_Id: number): void {
    this.detailedDataSource.next(detailedData);
    this.cacheService.setDetails(IMDB_Id, detailedData)
  }

  private processDetailedData(details: Object): DetailedDataModel {
    return new DetailedDataModel(
      DetailService.processCredits(details['credits']),
      details['budget'],
      Iso639.iso639ToName[details['original_language']],
      details['production_countries'].map(element => element['name']),
      new Date(details['release_date']),
      this.getFullPosterPath(details['poster_path']),
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

  private static formatIMDB_Id(tidAsInt: number): string {
    let tidAsString = tidAsInt.toString();
    let numberLeadingZeroes = 7 - tidAsString.length;
    let leadingZeroes = "";
    for (let i = 0; i < numberLeadingZeroes; i++) {
      leadingZeroes += "0";
    }
    return "tt" + leadingZeroes + tidAsString;

  }

  private getTMDB_Id(tid: string): Observable<number> {
    return this.http.get(
      this.TMDB_ROOT
      + 'find/'
      + tid
      + '?api_key='
      + TMDB_API_KEY
      + "&external_source=imdb_id").pipe(
      map(data => {
        if (data['movie_results'].length > 0) {
          return data['movie_results'][0]['id'];
        } else {
          // no movie with this imdb-id found in TMDB
          return -1;
        }
      }));
  }

  private getDetailsForTMDB_Id(tmdbID: number): Observable<Object> {
    return this.http.get(
      this.TMDB_ROOT
      + 'movie/'
      + tmdbID
      + "?api_key="
      + TMDB_API_KEY
      + "&append_to_response=credits")
  }

  /*
Poster sizes:
 "w92",
 "w154",
 "w185",
 "w342",
 "w500",
 "w780",
 "original"
 */

  private getFullPosterPath(partialPosterPath: string): string {
    if (partialPosterPath == null) {
      return null
    }

    let baseUrl = this.configData['images']['secure_base_url'];
    return baseUrl + 'w342' + partialPosterPath
  }
}
