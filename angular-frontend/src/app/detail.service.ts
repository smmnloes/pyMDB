import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import "rxjs/add/operator/map";
import {BasicDataModel} from "./header/content/search-page/search-results/result/basic-data-model";
import {DetailedDataModel} from "./header/content/search-page/search-results/result/detailed-data-model";
import {CombinedDataModel} from "./header/content/search-page/search-results/result/combined-data-model";

@Injectable()
export class DetailService {
  TMDB_API_KEY = "6d23876cfa1749f6f3ea88a46a1f50df";

  TMDB_ROOT = "https://api.themoviedb.org/3/";

  combinedDataSource: Subject<CombinedDataModel> = new Subject<CombinedDataModel>();
  combinedData$: Observable<CombinedDataModel>;

  constructor(private http: HttpClient) {
    this.combinedData$ = this.combinedDataSource.asObservable();
  }

  getDetails(movieData: BasicDataModel) {

    let imdbIdFormatted = DetailService.getTidFormatted(movieData.tid);

    this.getTmdbID(imdbIdFormatted).subscribe(tmdbID => {
      let dataCombined = new CombinedDataModel(movieData, null);

      if (tmdbID != -1) {
        this.getDetailsAndCastByTmdbId(tmdbID).subscribe(details => {
          console.log(details);
          dataCombined.detailedData = this.processDetailedData(details);
          this.combinedDataSource.next(dataCombined);
        });
      } else {
        this.combinedDataSource.next(dataCombined);
      }

    });

  }

  private processDetailedData(details) {
    return new DetailedDataModel(this.processCredits(details['credits']), details['budget'], details['original_language'],
      new Date(details['release_date']).toLocaleDateString(), details['poster_path']);
  }


  private processCredits(credits) {
    let creditsProcessed: string[][] = [];

    for (let cast of credits['cast']) {
      creditsProcessed.push([cast['character'], cast['name']]);
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
}
