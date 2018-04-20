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
  query_observer: Observer<boolean>;
  lastQuery: SearchModel = null;


  constructor(private http: HttpClient) {
    this.result$ = new Observable((observer) => {
      this.result_observer = observer;
    });
    this.new_query$ = new Observable((observer) => {
      this.query_observer = observer;
    })
  }


  makeQuery(queryData: SearchModel, new_query:boolean) {
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        this.result_observer.next(<any[]>data);
        this.query_observer.next(new_query);
      }
    );
  }

  loadPage(page: number) {
    this.lastQuery.current_page = page;
    this.makeQuery(this.lastQuery, false);
  }
}
