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
  result$: Observable<any[]>;
  result_observer: Observer<any[]>;
  new_query$: Observable<boolean>;
  new_query_observer: Observer<boolean>;
  nr_results$: Observable<number>;
  nr_results_observer: Observer<number>;
  lastQuery: SearchModel = null;

  PAGE_SIZE = 20;


  constructor(private http: HttpClient) {
    this.result$ = new Observable((observer) => {
      this.result_observer = observer;
    });
    this.new_query$ = new Observable((observer) => {
      this.new_query_observer = observer;
    });
    this.nr_results$ = new Observable((observer) => {
      this.nr_results_observer = observer;
    })
  }


  makeQuery(queryData: SearchModel, new_query: boolean) {
    queryData.page_size = this.PAGE_SIZE;
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        this.result_observer.next(<any[]>data);
        this.new_query_observer.next(new_query);
      }
    );

    if (new_query) {
      this.http.post('api/nr_of_results', queryData, httpOptions).subscribe(nr_of_results => {
        this.nr_results_observer.next(<number>nr_of_results);
        console.log(nr_of_results)
      })
    }


  }

  loadPage(page: number) {
    this.lastQuery.current_page = page;
    this.makeQuery(this.lastQuery, false);
  }
}
