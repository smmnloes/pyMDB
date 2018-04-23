import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import "rxjs/add/operator/map";

@Injectable()
export class DetailService {
  TMDB_API_KEY = "6d23876cfa1749f6f3ea88a46a1f50df";

  TMDB_ROOT = "https://api.themoviedb.org/3/";

  currentDetailsSource: Subject<Object> = new Subject<Object>();
  currentDetails$: Observable<Object>;

  constructor(private http: HttpClient) {
    this.currentDetails$ = this.currentDetailsSource.asObservable();
  }

  getDetailsByImdbId(tidAsInt: number) {

    let imdbIdFormatted = this.getTidFormatted(tidAsInt);

    this.getTmdbID(imdbIdFormatted).subscribe(tmdbID => {
      if (tmdbID != -1) {
        this.getDetailsByTmdbId(tmdbID).subscribe(details => {
          this.currentDetailsSource.next(details)
        })
      } else {
        this.currentDetailsSource.next(null);
      }

    });

  }

  private getTidFormatted(tidAsInt: number) {
    let tidAsString = tidAsInt.toString();
    let numberLeadingZeroes = 7 - tidAsString.length;
    let leadingZeroes = "";
    for (let i = 0; i < numberLeadingZeroes; i++) {
      leadingZeroes += "0";
    }
    return "tt" + leadingZeroes + tidAsString;

  }

  private getTmdbID(tid: string) {
    return this.http.get(this.TMDB_ROOT + 'find/' + tid + '?api_key='
      + this.TMDB_API_KEY + "&external_source=imdb_id").map(data => {
      if (data['movie_results'].length > 0) {
        return data['movie_results'][0]['id'];
      } else {
        // no movie with this imdb-id found in TMDB
        return -1;
      }
    });
  }

  private getDetailsByTmdbId(tmdbID: number) {
    return this.http.get(this.TMDB_ROOT + 'movie/' + tmdbID + "?api_key=" + this.TMDB_API_KEY)
  }
}
