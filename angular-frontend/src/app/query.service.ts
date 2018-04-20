import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs/Observable";
import {SearchModel} from "./content/search-page/search-form/search-model";
import {Observer} from "rxjs/Observer";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {
  results$: Observable<any[]>;
  resultsObserver: Observer<any[]>;

  newQuery: Observable<boolean>;
  newQueryObserver: Observer<boolean>;

  resultCount$: Observable<number>;
  resultCountObserver: Observer<number>;

  lastQuery: SearchModel = null;

  PAGE_SIZE = 20;


  constructor(private http: HttpClient) {
    this.results$ = new Observable((observer) => {
      this.resultsObserver = observer;
    });
    this.newQuery = new Observable((observer) => {
      this.newQueryObserver = observer;
    });
    this.resultCount$ = new Observable((observer) => {
      this.resultCountObserver = observer;
    })
  }


  makeQuery(queryData: SearchModel, new_query: boolean) {
    queryData.page_size = this.PAGE_SIZE;
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        this.resultsObserver.next(<any[]>data);
        this.newQueryObserver.next(new_query);
      }
    );

    if (new_query) {
      this.http.post('api/result_count', queryData, httpOptions).subscribe(resultCount => {
        this.resultCountObserver.next(<number>resultCount);
        console.log(resultCount)
      })
    }


  }

  loadPage(page: number) {
    this.lastQuery.currentPage = page;
    this.makeQuery(this.lastQuery, false);
  }



}

